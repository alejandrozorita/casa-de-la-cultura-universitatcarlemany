from flask import Flask, render_template, request, abort
from models import init_db, list_books, get_book

app = Flask(__name__)

# Inicializo la base de datos
init_db(app)

@app.route('/')
def home():
    """Página principal: lista todos los libros"""
    books = list_books()
    return render_template('home.html', books=books)

@app.route('/search')
def search():
    """Búsqueda de libros por título o autor"""
    q = request.args.get('q', '')
    books = list_books(q=q)
    return render_template('home.html', books=books, search_query=q)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Detalle de un libro específico"""
    book = get_book(book_id)
    
    if not book:
        abort(404)
    
    return render_template('detail.html', book=book)

@app.errorhandler(404)
def not_found(error):
    """Manejo simple de error 404"""
    return '<h1>404 - Libro no encontrado</h1><a href="/">Volver al inicio</a>', 404

if __name__ == '__main__':
    print("Iniciando La Casa de la Cultura...")
    print("Accede a: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

