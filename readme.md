# 📚 Proyecto: La Casa de la Cultura

Este proyecto busca digitalizar el catálogo de libros de la Casa de la Cultura.  
La idea es crear una herramienta sencilla para registrar, consultar y gestionar libros, usuarios y valoraciones.

---

## 📁 Estructura del repositorio

proyecto-cultura/
├── database/         → Base de datos, CSV y scripts de carga
├── app/              → Aplicación principal (Flask o similar)
├── etl/              → Flujos o scripts para procesar y cargar los datos (KNIME o Python)
└── README.md         → Este archivo


---

## 🧩 Qué hace cada parte

- **database/**  
  Aquí guardamos los archivos `.csv` (libros, usuarios, ejemplares, valoraciones) y los scripts de carga.  
  Puede incluir el `schema.sql` con la estructura de tablas o un flujo de KNIME si se hace el ETL visual.

- **app/**  
  Contiene la aplicación. Por ahora puede ser un prototipo en Flask o el entorno que elijamos.  
  Aquí estarán los archivos principales, las vistas (HTML) y la lógica básica.

- **etl/**  
  Contiene el flujo ETL (Extract, Transform, Load).  
  Aquí van los ficheros de KNIME o los scripts en Python que preparan los datos antes de cargarlos a la base de datos.  
  La idea es que todos puedan entender cómo se procesan los CSV y cómo llegan limpios a las tablas.


---

## ⚙️ Cómo trabajaremos

1. Cada persona puede montar el entorno localmente (Python o KNIME).  
2. Los CSV se mantienen en `/database`.  
3. Los flujos o scripts ETL se guardan en `/etl`.  
4. El documento técnico y los avances se guardan en `/docs`.  
5. Los cambios importantes se suben al repositorio con un mensaje claro en el commit.

---

## 💡 Objetivo del repositorio

Dejar una base clara y ordenada del proyecto:  
- Datos → `/database`  
- ETL → `/etl`  
- Aplicación → `/app`  
- Documentación → `/docs`  

Así todos podemos trabajar de forma sincronizada y sin duplicar esfuerzos.
  
---

## 👥 Equipo de trabajo

- Gustavo Adolfo Aguilar Ruiz  
- María de la Concepción Marcos Ramos  
- Alfred Segués Oliva  
- Alejandro Zorita  

---
