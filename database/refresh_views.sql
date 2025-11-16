-- Script para refrescar las vistas materializadas
-- Ejecutar cuando se añadan nuevas valoraciones o libros

-- Refresca la vista de libros más valorados
REFRESH MATERIALIZED VIEW mv_top_rated_books;

-- Muestra estadísticas actualizadas
SELECT 
    'Vista actualizada' as status,
    COUNT(*) as total_libros,
    MAX(avg_rating) as max_rating,
    MIN(avg_rating) as min_rating
FROM mv_top_rated_books;

