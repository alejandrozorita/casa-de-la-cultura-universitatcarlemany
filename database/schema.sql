-- Schema para PostgreSQL - ADAPTADO PARA CSVs
-- Base de datos: La Casa de la Cultura
-- Adaptado para coincidir con: books.csv, copies(ejemplares).csv, ratings.csv, user_info.csv

-- ============================================================================
-- TABLA: books
-- Fuente: books.csv (10,000 registros)
-- Columnas CSV: isbn, authors, original_publication_year, original_title,
--               title, language_code, book_id, image_url
-- ============================================================================
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,                    -- PK del CSV (no SERIAL)
    isbn VARCHAR(20),                               -- Puede ser NULL (7% vacío)
    authors TEXT NOT NULL,                          -- Plural, siempre tiene valor
    original_publication_year INTEGER,              -- Puede ser NULL (0.2% vacío)
    original_title TEXT,                            -- Puede ser NULL (5.9% vacío)
    title TEXT NOT NULL,                            -- Siempre tiene valor
    language_code VARCHAR(10),                      -- Puede ser NULL (10.8% vacío)
    image_url TEXT                                  -- Siempre tiene valor
);

-- ============================================================================
-- TABLA: users
-- Fuente: user_info.csv (501 registros)
-- Columnas CSV: user_id, sexo, comentario, fecha_nacimiento
-- NOTA: ratings.csv referencia 53,424 users, pero solo 501 tienen info completa
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,                    -- PK del CSV (no SERIAL)
    sexo VARCHAR(50),                               -- "Mujer", "Hombre", "Prefiere no responder"
    comentario TEXT,                                -- Descripción de preferencias
    fecha_nacimiento DATE                           -- Formato: DD/MM/YYYY en CSV
);

-- ============================================================================
-- TABLA: copies (ejemplares)
-- Fuente: copies(ejemplares).csv (55,327 registros)
-- Columnas CSV: copy_id, book_id
-- Un libro puede tener múltiples ejemplares físicos
-- ============================================================================
CREATE TABLE IF NOT EXISTS copies (
    copy_id INTEGER PRIMARY KEY,                    -- PK del CSV (no SERIAL)
    book_id INTEGER NOT NULL,                       -- FK a books
    status VARCHAR(50) DEFAULT 'available',         -- Estado del ejemplar (no en CSV, valor por defecto)

    CONSTRAINT fk_copies_book
        FOREIGN KEY (book_id)
        REFERENCES books(book_id)
        ON DELETE CASCADE
);

-- ============================================================================
-- TABLA: ratings (valoraciones)
-- Fuente: ratings.csv (5,976,479 registros)
-- Columnas CSV: user_id, copy_id, rating
-- IMPORTANTE: Las valoraciones están por ejemplar (copy_id), no por libro
-- ============================================================================
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,                          -- Auto-incremental (no en CSV)
    user_id INTEGER NOT NULL,                       -- FK a users (puede no existir en users)
    copy_id INTEGER NOT NULL,                       -- FK a copies (valoración por ejemplar)
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),  -- Validación 1-5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp automático (no en CSV)

    -- Un usuario puede valorar el mismo ejemplar solo una vez
    CONSTRAINT unique_user_copy UNIQUE(user_id, copy_id),

    -- Foreign Keys
    CONSTRAINT fk_ratings_copy
        FOREIGN KEY (copy_id)
        REFERENCES copies(copy_id)
        ON DELETE CASCADE

    -- NOTA: NO hay FK a users porque 99.1% de user_ids en ratings.csv
    -- no existen en user_info.csv. Esto es intencional para permitir la carga.
    -- Si quieres integridad estricta, necesitarás limpiar los datos primero.
);

-- ============================================================================
-- ÍNDICES para mejorar rendimiento de consultas
-- ============================================================================

-- Índices en books
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_authors ON books(authors);
CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
CREATE INDEX IF NOT EXISTS idx_books_language ON books(language_code);

-- Índices en users
CREATE INDEX IF NOT EXISTS idx_users_sexo ON users(sexo);

-- Índices en copies
CREATE INDEX IF NOT EXISTS idx_copies_book_id ON copies(book_id);
CREATE INDEX IF NOT EXISTS idx_copies_status ON copies(status);

-- Índices en ratings (IMPORTANTES para consultas de búsqueda)
CREATE INDEX IF NOT EXISTS idx_ratings_user_id ON ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_ratings_copy_id ON ratings(copy_id);
CREATE INDEX IF NOT EXISTS idx_ratings_rating ON ratings(rating);
CREATE INDEX IF NOT EXISTS idx_ratings_created_at ON ratings(created_at);

-- ============================================================================
-- COMENTARIOS ADICIONALES
-- ============================================================================

COMMENT ON TABLE books IS 'Catálogo de libros. 10,000 títulos únicos.';
COMMENT ON TABLE users IS 'Información de usuarios. Solo 501 usuarios tienen info completa (1% del total de usuarios que han hecho ratings).';
COMMENT ON TABLE copies IS 'Ejemplares físicos de libros. Un libro puede tener múltiples copias. 55,327 ejemplares.';
COMMENT ON TABLE ratings IS 'Valoraciones de usuarios sobre ejemplares específicos. 5,976,479 valoraciones.';

COMMENT ON COLUMN ratings.user_id IS 'ADVERTENCIA: La mayoría de user_ids (99.1%) no tienen registro en la tabla users. No hay FK para permitir carga de datos.';

-- ============================================================================
-- VISTAS ÚTILES (OPCIONAL)
-- ============================================================================

-- Vista para obtener valoraciones con información del libro
CREATE OR REPLACE VIEW v_ratings_with_books AS
SELECT
    r.id,
    r.user_id,
    r.copy_id,
    r.rating,
    r.created_at,
    c.book_id,
    b.title,
    b.authors,
    b.isbn
FROM ratings r
JOIN copies c ON r.copy_id = c.copy_id
JOIN books b ON c.book_id = b.book_id;

-- Vista para obtener valoración promedio por libro
CREATE OR REPLACE VIEW v_book_ratings AS
SELECT
    b.book_id,
    b.title,
    b.authors,
    COUNT(DISTINCT r.id) as total_ratings,
    AVG(r.rating) as avg_rating,
    MIN(r.rating) as min_rating,
    MAX(r.rating) as max_rating
FROM books b
LEFT JOIN copies c ON b.book_id = c.book_id
LEFT JOIN ratings r ON c.copy_id = r.copy_id
GROUP BY b.book_id, b.title, b.authors;

-- ============================================================================
-- FIN DEL SCHEMA
-- ============================================================================
