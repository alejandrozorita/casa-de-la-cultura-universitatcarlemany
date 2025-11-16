from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializo la conexión a la base de datos PostgreSQL"""
    # Configuración hardcodeada de la base de datos
    database_url = "postgresql+psycopg2://library_user:library_pass@host.docker.internal:5432/library"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    print(f"✅ Base de datos PostgreSQL configurada: host.docker.internal:5432/library")

def list_books(q=None, page=1, per_page=20):
    """
    Devuelvo una lista de libros con paginación
    """
    try:
        offset = (page - 1) * per_page
        
        if q:
            query = """
                SELECT book_id, title, authors, language_code 
                FROM books 
                WHERE title ILIKE :title OR authors ILIKE :authors
                ORDER BY book_id
                LIMIT :limit OFFSET :offset
            """
            params = {'title': f'%{q}%', 'authors': f'%{q}%', 'limit': per_page, 'offset': offset}
            result = db.session.execute(db.text(query), params)
            
            count_query = "SELECT COUNT(*) FROM books WHERE title ILIKE :title OR authors ILIKE :authors"
            count_result = db.session.execute(db.text(count_query), {'title': f'%{q}%', 'authors': f'%{q}%'})
            total = count_result.fetchone()[0]
        else:
            query = """
                SELECT book_id, title, authors, language_code 
                FROM books 
                ORDER BY book_id
                LIMIT :limit OFFSET :offset
            """
            result = db.session.execute(db.text(query), {'limit': per_page, 'offset': offset})
            
            count_query = "SELECT COUNT(*) FROM books"
            count_result = db.session.execute(db.text(count_query))
            total = count_result.fetchone()[0]
        
        books = []
        for row in result:
            books.append({
                'id': row[0],
                'title': row[1] or 'Sin título',
                'author': row[2] or 'Desconocido',
                'category': row[3] or 'N/A'
            })
        
        total_pages = (total + per_page - 1) // per_page
        
        return {
            'books': books,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
    
    except Exception as e:
        print(f"Error al listar libros: {e}", flush=True)
        return {'books': [], 'page': 1, 'per_page': per_page, 'total': 0, 'total_pages': 0, 'has_prev': False, 'has_next': False}

def get_book(book_id):
    """
    Devuelvo los detalles de un libro específico con toda la info
    """
    try:
        # Info básica del libro
        query = """
            SELECT book_id, title, authors, language_code, 
                   original_publication_year, isbn, image_url 
            FROM books 
            WHERE book_id = :id
        """
        result = db.session.execute(db.text(query), {'id': book_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        book = {
            'id': row[0],
            'title': row[1] or 'Sin título',
            'author': row[2] or 'Desconocido',
            'language': row[3] or 'N/A',
            'year': row[4],
            'isbn': row[5] or 'N/A',
            'image_url': row[6]
        }
        
        # Info de ejemplares con ubicación simulada
        try:
            copies_query = """
                SELECT copy_id, status 
                FROM copies 
                WHERE book_id = :book_id 
                LIMIT 10
            """
            copies_result = db.session.execute(db.text(copies_query), {'book_id': book_id})
            copies = []
            for i, copy in enumerate(copies_result, 1):
                # Simulo ubicaciones
                sala = f"Sala {(i % 3) + 1}"
                estanteria = f"{chr(65 + (i % 5))}-{(i % 20) + 1}"
                copies.append({
                    'id': copy[0],
                    'status': copy[1] or 'disponible',
                    'location': f"{sala}, Estantería {estanteria}"
                })
            book['copies'] = copies
            book['copies_count'] = len(copies)
        except:
            book['copies'] = []
            book['copies_count'] = 0
        
        # Valoración media
        try:
            rating_query = """
                SELECT AVG(r.rating), COUNT(r.rating)
                FROM ratings r
                JOIN copies c ON r.copy_id = c.copy_id
                WHERE c.book_id = :book_id
            """
            rating_result = db.session.execute(db.text(rating_query), {'book_id': book_id})
            avg_rating, count = rating_result.fetchone()
            book['avg_rating'] = round(avg_rating, 1) if avg_rating else None
            book['rating_count'] = count or 0
        except:
            book['avg_rating'] = None
            book['rating_count'] = 0
        
        return book
    
    except Exception as e:
        print(f"Error al obtener libro {book_id}: {e}", flush=True)
        return None

def get_recommendations(book_id, limit=5):
    """
    Recomendaciones simples basadas en libros del mismo autor o idioma
    """
    try:
        query = """
            SELECT DISTINCT b2.book_id, b2.title, b2.authors
            FROM books b1
            JOIN books b2 ON (b1.authors = b2.authors OR b1.language_code = b2.language_code)
            WHERE b1.book_id = :book_id 
            AND b2.book_id != :book_id
            LIMIT :limit
        """
        result = db.session.execute(db.text(query), {'book_id': book_id, 'limit': limit})
        
        recommendations = []
        for row in result:
            recommendations.append({
                'id': row[0],
                'title': row[1],
                'author': row[2]
            })
        
        return recommendations
    except Exception as e:
        print(f"Error en recomendaciones: {e}", flush=True)
        return []

def get_recent_books(page=1, per_page=20):
    """
    Libros ordenados por ID descendente (más recientes primero)
    """
    try:
        offset = (page - 1) * per_page
        
        query = """
            SELECT book_id, title, authors, language_code 
            FROM books 
            ORDER BY book_id DESC
            LIMIT :limit OFFSET :offset
        """
        result = db.session.execute(db.text(query), {'limit': per_page, 'offset': offset})
        
        count_query = "SELECT COUNT(*) FROM books"
        count_result = db.session.execute(db.text(count_query))
        total = count_result.fetchone()[0]
        
        books = []
        for row in result:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'category': row[3] or 'N/A'
            })
        
        total_pages = (total + per_page - 1) // per_page
        
        return {
            'books': books,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
    except Exception as e:
        print(f"Error en libros recientes: {e}", flush=True)
        return {'books': [], 'page': 1, 'per_page': per_page, 'total': 0, 'total_pages': 0, 'has_prev': False, 'has_next': False}

def get_top_rated(page=1, per_page=20):
    """
    Libros más valorados usando vista materializada (instantáneo)
    """
    try:
        offset = (page - 1) * per_page
        
        # Query súper rápida usando la vista materializada
        query = """
            SELECT book_id, title, authors, avg_rating, num_ratings
            FROM mv_top_rated_books
            LIMIT :limit OFFSET :offset
        """
        result = db.session.execute(db.text(query), {'limit': per_page, 'offset': offset})
        
        books = []
        for row in result:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'category': f"⭐ {round(row[3], 1)}/5",
                'rating_count': row[4]
            })
        
        # Cuento el total (también rápido porque lee de la vista)
        count_query = "SELECT COUNT(*) FROM mv_top_rated_books"
        count_result = db.session.execute(db.text(count_query))
        total = count_result.fetchone()[0]
        
        total_pages = (total + per_page - 1) // per_page
        
        return {
            'books': books,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
    except Exception as e:
        print(f"Error en top rated: {e}", flush=True)
        return {'books': [], 'page': 1, 'per_page': per_page, 'total': 0, 'total_pages': 0, 'has_prev': False, 'has_next': False}

def get_categories():
    """
    Obtengo las categorías (idiomas) disponibles
    """
    try:
        query = """
            SELECT DISTINCT language_code 
            FROM books 
            WHERE language_code IS NOT NULL
            ORDER BY language_code
            LIMIT 20
        """
        result = db.session.execute(db.text(query))
        return [row[0] for row in result]
    except:
        return []

