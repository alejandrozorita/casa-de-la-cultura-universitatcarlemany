import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import os

# Rutas a los archivos CSV
BASE_DIR = os.path.dirname(__file__)
RATINGS_FILE = os.path.join(BASE_DIR, '..', 'database', 'ratings.csv')
BOOKS_FILE = os.path.join(BASE_DIR, '..', 'database', 'books.csv')
USER_INFO_FILE = os.path.join(BASE_DIR, '..', 'database', 'user_info.csv')

def load_data():
    """
    Cargo los datos desde los archivos CSV.
    Devuelvo tres DataFrames: ratings, books y user_info.
    """
    try:
        ratings = pd.read_csv(RATINGS_FILE)
        books = pd.read_csv(BOOKS_FILE)
        user_info = pd.read_csv(USER_INFO_FILE)
        
        print(f"Datos cargados: {len(ratings)} valoraciones, {len(books)} libros, {len(user_info)} usuarios")
        return ratings, books, user_info
    
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo CSV. {e}")
        return None, None, None

def create_user_book_matrix(ratings_df):
    """
    Creo una matriz usuario-libro con valores binarios.
    Si rating >= 4, marco 1 (el usuario recomienda el libro).
    Si rating < 4, marco 0.
    """
    # Filtro solo ratings >= 4 (recomendaciones positivas)
    recommendations = ratings_df[ratings_df['rating'] >= 4].copy()
    
    # Creo una columna auxiliar con valor 1
    recommendations['recommended'] = 1
    
    # Genero la matriz pivotada: filas=usuarios, columnas=libros, valores=1 o 0
    user_book_matrix = recommendations.pivot_table(
        index='user_id',
        columns='book_id',
        values='recommended',
        fill_value=0
    )
    
    # Convierto a tipo booleano (True/False) para Apriori
    user_book_matrix = user_book_matrix.astype(bool)
    
    print(f"Matriz usuario-libro creada: {user_book_matrix.shape[0]} usuarios x {user_book_matrix.shape[1]} libros")
    return user_book_matrix

def apply_apriori(user_book_matrix, min_support=0.05):
    """
    Aplico el algoritmo Apriori para encontrar conjuntos frecuentes de libros.
    min_support: soporte mínimo (por defecto 5% de usuarios)
    """
    print(f"Aplicando Apriori con soporte mínimo de {min_support}...")
    
    # Encuentro los conjuntos frecuentes de libros
    frequent_itemsets = apriori(user_book_matrix, min_support=min_support, use_colnames=True)
    
    print(f"Se encontraron {len(frequent_itemsets)} conjuntos frecuentes")
    return frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence=0.6):
    """
    Genero reglas de asociación a partir de los conjuntos frecuentes.
    Uso la métrica de confianza con un umbral mínimo de 0.6.
    """
    if len(frequent_itemsets) == 0:
        print("No hay conjuntos frecuentes para generar reglas")
        return pd.DataFrame()
    
    print(f"Generando reglas de asociación con confianza mínima de {min_confidence}...")
    
    # Genero las reglas
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    
    print(f"Se generaron {len(rules)} reglas de asociación")
    return rules

def get_recommendations(book_title, books_df, rules_df, top_n=3):
    """
    Obtengo recomendaciones de libros basadas en el título dado.
    
    Parámetros:
    - book_title: título del libro para el cual buscar recomendaciones
    - books_df: DataFrame con información de libros (id, title)
    - rules_df: DataFrame con reglas de asociación
    - top_n: número de recomendaciones a devolver
    
    Devuelvo: lista de tuplas (título, confianza)
    """
    # Busco el book_id del título dado
    book_match = books_df[books_df['title'].str.lower() == book_title.lower()]
    
    if book_match.empty:
        print(f"No se encontró el libro '{book_title}'")
        return []
    
    book_id = book_match.iloc[0]['id']
    
    # Busco reglas donde el libro aparezca en el antecedente
    # Las reglas tienen formato: {libro_base} -> {libro_recomendado}
    relevant_rules = rules_df[rules_df['antecedents'].apply(lambda x: book_id in x)]
    
    if relevant_rules.empty:
        print(f"No hay recomendaciones disponibles para '{book_title}'")
        return []
    
    # Ordeno por confianza descendente
    relevant_rules = relevant_rules.sort_values('confidence', ascending=False)
    
    # Extraigo las recomendaciones
    recommendations = []
    for _, row in relevant_rules.head(top_n).iterrows():
        # Obtengo el libro recomendado del consecuente
        recommended_book_id = list(row['consequents'])[0]
        
        # Busco el título del libro
        book_info = books_df[books_df['id'] == recommended_book_id]
        if not book_info.empty:
            book_title_rec = book_info.iloc[0]['title']
            confidence = row['confidence']
            recommendations.append((book_title_rec, confidence))
    
    return recommendations

def main():
    """
    Función principal para demostrar el sistema de recomendación.
    """
    print("=" * 60)
    print("SISTEMA DE RECOMENDACIÓN DE LIBROS - ALGORITMO APRIORI")
    print("=" * 60)
    print()
    
    # Cargo los datos
    ratings_df, books_df, user_info_df = load_data()
    
    if ratings_df is None:
        print("Error al cargar los datos. Verifica que los archivos CSV existan.")
        return
    
    print()
    
    # Creo la matriz usuario-libro
    user_book_matrix = create_user_book_matrix(ratings_df)
    print()
    
    # Aplico el algoritmo Apriori
    frequent_itemsets = apply_apriori(user_book_matrix, min_support=0.05)
    print()
    
    # Genero las reglas de asociación
    rules = generate_rules(frequent_itemsets, min_confidence=0.6)
    print()
    
    if rules.empty:
        print("No se pudieron generar reglas. Intenta reducir el umbral de confianza.")
        return
    
    # Ejemplo: buscar recomendaciones para un libro
    print("=" * 60)
    print("EJEMPLO DE RECOMENDACIONES")
    print("=" * 60)
    
    # Busco un libro de ejemplo (puedes cambiarlo)
    example_book = "El Quijote"
    
    # Si no existe ese libro, uso el primero disponible
    if example_book not in books_df['title'].values:
        example_book = books_df.iloc[0]['title']
        print(f"(Usando '{example_book}' como ejemplo)")
    
    print(f"\nRecomendaciones para '{example_book}':")
    recommendations = get_recommendations(example_book, books_df, rules, top_n=3)
    
    if recommendations:
        for i, (title, confidence) in enumerate(recommendations, 1):
            print(f"  {i}. {title} (confianza: {confidence:.2f})")
    else:
        print("  No hay recomendaciones disponibles para este libro.")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()

