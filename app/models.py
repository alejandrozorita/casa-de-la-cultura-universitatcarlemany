import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializo la conexión a la base de datos PostgreSQL"""
    # Obtengo la URL de la base de datos desde variable de entorno
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        raise ValueError(
            "ERROR: Variable DATABASE_URL no configurada.\n"
            "Debes configurar la URL de PostgreSQL en las variables de entorno.\n"
            "Ejemplo: DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/library"
        )
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Muestro solo la parte relevante de la URL (sin credenciales)
    db_info = database_url.split('@')[-1] if '@' in database_url else 'PostgreSQL'
    print(f"✅ Base de datos PostgreSQL configurada: {db_info}")

def list_books(q=None, limit=50):
    """
    Devuelvo una lista de libros. Si q viene, filtro por título o autor.
    Uso SQL directo para ser flexible con el esquema.
    """
    try:
        if q:
            # Busco en título o autor (ILIKE es case-insensitive en PostgreSQL)
            query = """
                SELECT id, title, author, category 
                FROM books 
                WHERE title ILIKE :title OR author ILIKE :author
                LIMIT :limit
            """
            result = db.session.execute(
                db.text(query), 
                {'title': f'%{q}%', 'author': f'%{q}%', 'limit': limit}
            )
        else:
            # Devuelvo todos los libros
            query = "SELECT id, title, author, category FROM books LIMIT :limit"
            result = db.session.execute(db.text(query), {'limit': limit})
        
        books = []
        for row in result:
            books.append({
                'id': row[0],
                'title': row[1] if len(row) > 1 else 'Sin título',
                'author': row[2] if len(row) > 2 else 'Desconocido',
                'category': row[3] if len(row) > 3 else 'Sin categoría'
            })
        
        return books
    
    except Exception as e:
        print(f"Error al listar libros: {e}")
        return []

def get_book(book_id):
    """
    Devuelvo los detalles de un libro específico.
    Intento obtener info de copias y valoraciones.
    """
    try:
        # Obtengo info básica del libro
        query = "SELECT id, title, author, category FROM books WHERE id = :id"
        result = db.session.execute(db.text(query), {'id': book_id})
        row = result.fetchone()
        
        if not row:
            return None
        
        book = {
            'id': row[0],
            'title': row[1] if len(row) > 1 else 'Sin título',
            'author': row[2] if len(row) > 2 else 'Desconocido',
            'category': row[3] if len(row) > 3 else 'Sin categoría'
        }
        
        # Intento contar copias
        try:
            count_query = "SELECT COUNT(*) FROM copies WHERE book_id = :book_id"
            count_result = db.session.execute(db.text(count_query), {'book_id': book_id})
            book['copies_count'] = count_result.fetchone()[0]
        except:
            book['copies_count'] = 0
        
        # Intento calcular valoración media
        try:
            rating_query = "SELECT AVG(rating) FROM ratings WHERE book_id = :book_id"
            rating_result = db.session.execute(db.text(rating_query), {'book_id': book_id})
            avg_rating = rating_result.fetchone()[0]
            book['avg_rating'] = round(avg_rating, 1) if avg_rating else None
        except:
            book['avg_rating'] = None
        
        return book
    
    except Exception as e:
        print(f"Error al obtener libro {book_id}: {e}")
        return None

