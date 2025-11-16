-- Script para crear las vistas materializadas
-- Ejecutar SOLO LA PRIMERA VEZ o si se borra la base de datos

-- Borra la vista si ya existe (para recrearla)
DROP MATERIALIZED VIEW IF EXISTS mv_top_rated_books CASCADE;

-- Crea la vista materializada de libros más valorados
-- Esto tarda ~30-40 segundos pero solo se ejecuta una vez
CREATE MATERIALIZED VIEW mv_top_rated_books AS
SELECT 
    b.book_id, 
    b.title, 
    b.authors, 
    AVG(r.rating) as avg_rating,
    COUNT(r.rating) as num_ratings
FROM books b
JOIN copies c ON b.book_id = c.book_id
JOIN ratings r ON c.copy_id = r.copy_id
GROUP BY b.book_id, b.title, b.authors
HAVING COUNT(r.rating) > 10
ORDER BY avg_rating DESC, num_ratings DESC;

-- Crea índice para optimizar consultas
CREATE INDEX idx_mv_top_rated_avg ON mv_top_rated_books(avg_rating DESC, num_ratings DESC);

-- Muestra estadísticas
SELECT 
    'Vista creada exitosamente' as status,
    COUNT(*) as total_libros,
    MAX(avg_rating) as max_rating,
    MIN(avg_rating) as min_rating
FROM mv_top_rated_books;

