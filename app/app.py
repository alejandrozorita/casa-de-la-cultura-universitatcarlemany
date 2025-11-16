from flask import Flask, render_template, request, abort
from models import init_db, list_books, get_book, get_recommendations, get_top_rated, get_categories, get_recent_books

app = Flask(__name__)

# Inicializo la base de datos
init_db(app)

@app.route('/')
def home():
    """Página principal: libros más recientes"""
    page = request.args.get('page', 1, type=int)
    result = get_recent_books(page=page, per_page=20)
    categories = get_categories()
    return render_template('home.html', 
                         books=result['books'], 
                         pagination=result,
                         categories=categories, 
                         page_title="Libros recientes",
                         current_route='home')

@app.route('/search')
def search():
    """Búsqueda de libros por título o autor"""
    q = request.args.get('q', '')
    category = request.args.get('category', '')
    page = request.args.get('page', 1, type=int)
    
    if category:
        result = list_books(page=page, per_page=20)
        result['books'] = [b for b in result['books'] if b.get('category') == category]
        page_title = f"Libros en {category}"
    elif q:
        result = list_books(q=q, page=page, per_page=20)
        page_title = f"Resultados para: {q}"
    else:
        result = list_books(page=page, per_page=20)
        page_title = "Todos los libros"
    
    categories = get_categories()
    return render_template('home.html', 
                         books=result['books'], 
                         pagination=result,
                         search_query=q, 
                         selected_category=category, 
                         categories=categories, 
                         page_title=page_title,
                         current_route='search')

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Detalle de un libro específico con recomendaciones"""
    book = get_book(book_id)
    
    if not book:
        abort(404)
    
    recommendations = get_recommendations(book_id)
    
    return render_template('detail.html', book=book, recommendations=recommendations)

@app.route('/top-rated')
def top_rated():
    """Página de libros más valorados"""
    page = request.args.get('page', 1, type=int)
    result = get_top_rated(page=page, per_page=20)
    categories = get_categories()
    return render_template('home.html', 
                         books=result['books'], 
                         pagination=result,
                         categories=categories, 
                         page_title="Libros más valorados",
                         current_route='top_rated')

@app.errorhandler(404)
def not_found(error):
    """Manejo simple de error 404"""
    return '<h1>404 - Libro no encontrado</h1><a href="/">Volver al inicio</a>', 404

if __name__ == '__main__':
    import os
    
    # Leo el modo debug desde variable de entorno (por defecto False en producción)
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("Iniciando La Casa de la Cultura...")
    print(f"Modo debug: {'activado' if debug_mode else 'desactivado'}")
    print("Accede a: http://127.0.0.1:5000")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

