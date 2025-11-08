# 📚 La Casa de la Cultura - Aplicación Web

Aplicación web simple en Flask para consultar el catálogo de libros de la Casa de la Cultura.

## 🎯 Requisitos

- Python 3.8 o superior
- Base de datos `library.db` (SQLite)

## 📦 Instalación

1. Clona el repositorio y navega a la carpeta del proyecto:

```bash
cd casa-de-la-cultura-universitatcarlemany
```

2. Crea un entorno virtual (recomendado):

```bash
python -m venv venv
```

3. Activa el entorno virtual:

- En Windows:
```bash
venv\Scripts\activate
```

- En macOS/Linux:
```bash
source venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🗃️ Base de datos

El proyecto soporta dos tipos de bases de datos:

### PostgreSQL (Recomendado para producción)
- Usa Docker Compose para levantar PostgreSQL automáticamente
- El esquema está en `database/schema.sql`

### SQLite (Para desarrollo local)
- Si no se configura `DATABASE_URL`, usa SQLite por defecto
- El archivo `library.db` debe estar en la raíz del proyecto

**Estructura de tablas requeridas:**
- `books` (id, title, author, category)
- `users` (id, name, email) - opcional
- `copies` (id, book_id, status) - opcional
- `ratings` (id, user_id, book_id, rating) - opcional

## ▶️ Ejecución

### Opción 1: Ejecución local

1. Asegúrate de que el entorno virtual está activado.

2. Ejecuta la aplicación:

```bash
python app/app.py
```

3. Abre tu navegador en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Opción 2: Ejecución con Docker Compose (Recomendado)

1. Levanta todos los servicios (PostgreSQL + App):

```bash
docker-compose up -d
```

2. Crea el esquema de base de datos:

```bash
docker exec -i casa-cultura-db psql -U library_user -d library < database/schema.sql
```

3. Abre tu navegador en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

**Comandos útiles:**
```bash
# Ver logs
docker-compose logs -f web

# Parar los servicios
docker-compose down

# Parar y eliminar volúmenes (borra la BD)
docker-compose down -v

# Acceder a PostgreSQL
docker exec -it casa-cultura-db psql -U library_user -d library
```

### Opción 3: Ejecución con Docker (sin Compose)

1. Construye la imagen:

```bash
docker build -t casa-cultura .
```

2. Ejecuta el contenedor con SQLite:

```bash
docker run -p 5000:5000 -v $(pwd)/library.db:/app/library.db casa-cultura
```

## 🔍 Funcionalidades

### Aplicación Web
- **Página principal (/)**: Lista todos los libros del catálogo
- **Búsqueda (/search?q=...)**: Busca libros por título o autor
- **Detalle (/book/id)**: Muestra información detallada de un libro

### Sistema de Recomendación (Algoritmo Apriori)

El proyecto incluye un módulo de recomendación de libros basado en el algoritmo Apriori que analiza patrones de valoraciones de usuarios.

**Requisitos:**
- Archivos CSV en la carpeta `database/`:
  - `ratings.csv` (user_id, book_id, rating)
  - `books.csv` (id, title)
  - `user_info.csv` (id, nombre)

**Ejecución:**
```bash
python app/recommendation.py
```

El sistema:
1. Carga las valoraciones de usuarios
2. Crea una matriz binaria (rating >= 4 = recomendación positiva)
3. Aplica el algoritmo Apriori para encontrar libros frecuentemente valorados juntos
4. Genera reglas de asociación con confianza mínima del 60%
5. Recomienda libros basándose en estas asociaciones

## 🛠️ Solución de problemas

### "No se encontraron libros"
- Verifica que `library.db` está en la raíz del proyecto
- Asegúrate de que la base de datos tiene la tabla `books` con datos

### Error al iniciar la aplicación
- Comprueba que las dependencias están instaladas: `pip list`
- Verifica que estás ejecutando desde la carpeta correcta

### Columnas faltantes
Si algunas columnas no existen en tu base de datos, la aplicación seguirá funcionando mostrando valores por defecto ("Sin título", "Desconocido", etc.).

## 📁 Estructura del proyecto

```
casa-de-la-cultura-universitatcarlemany/
├── app/
│   ├── __init__.py
│   ├── app.py              # Aplicación Flask y rutas
│   ├── models.py           # Conexión y consultas a la BD
│   ├── recommendation.py   # Sistema de recomendación (Apriori)
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html
│   │   ├── home.html
│   │   └── detail.html
│   └── static/             # Archivos estáticos (vacío)
├── database/               # Archivos CSV y esquemas
│   └── schema.sql          # Esquema PostgreSQL
├── Dockerfile              # Configuración Docker
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore           # Archivos excluidos de Docker
├── library.db              # Base de datos SQLite (opcional)
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## 👥 Equipo

- Gustavo Adolfo Aguilar Ruiz
- María de la Concepción Marcos Ramos
- Alfred Segués Oliva
- Alejandro Zorita
