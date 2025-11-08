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

**IMPORTANTE:** Este proyecto NO genera la base de datos. Necesitas colocar el archivo `library.db` en la raíz del proyecto.

```
casa-de-la-cultura-universitatcarlemany/
├── app/
├── library.db  ← Debe estar aquí
├── requirements.txt
└── README.md
```

La base de datos se genera desde un proceso ETL externo (KNIME). Debe contener al menos la tabla `books` con las columnas:
- `id`
- `title`
- `author`
- `category`

Opcionalmente puede tener las tablas `copies` y `ratings` para mostrar información adicional.

## ▶️ Ejecución

1. Asegúrate de que el entorno virtual está activado.

2. Ejecuta la aplicación:

```bash
python app/app.py
```

3. Abre tu navegador en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔍 Funcionalidades

- **Página principal (/)**: Lista todos los libros del catálogo
- **Búsqueda (/search?q=...)**: Busca libros por título o autor
- **Detalle (/book/id)**: Muestra información detallada de un libro

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
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html
│   │   ├── home.html
│   │   └── detail.html
│   └── static/             # Archivos estáticos (vacío)
├── library.db              # Base de datos (no incluida)
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 👥 Equipo

- Gustavo Adolfo Aguilar Ruiz
- María de la Concepción Marcos Ramos
- Alfred Segués Oliva
- Alejandro Zorita
