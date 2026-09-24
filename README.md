# 🛍️ Sistema de Compra y Venta (MVC - FastAPI, PostgreSQL, Tailwind, Alpine.js & Chart.js)

Sistema web Full-Stack de **Compra y Venta de Productos** desarrollado bajo el patrón arquitectónico **MVC (Modelo-Vista-Controlador)** utilizando **Python (FastAPI)**, **PostgreSQL**, **Jinja2**, **Tailwind CSS**, **Alpine.js** y **Chart.js**.

---

## 👥 Roles y Permisos del Sistema

1. **🌐 Visitante / Cliente General (Sin registro obligatorio)**:
   - Puede explorar el catálogo público de productos con imágenes, precios, descripciones e indicadores de stock en tiempo real.
   - Puede realizar compras instantáneamente ingresando su nombre en el modal de compra.
2. **🛒 Usuario / Cliente (Registrado)**:
   - Puede registrarse (`/register`) e iniciar sesión (`/login`).
   - Al comprar, el sistema asocia automáticamente la orden a su cuenta y le permite visualizar su **Historial de Mis Compras** personal.
3. **⚙️ Administrador**:
   - **Email**: `admin@tienda.com`
   - **Contraseña**: `admin123`
   - **Dashboard con Chart.js**: Gráficos interactivos de barra (stock por producto) y dona (ingresos totales por ventas).
   - **CRUD Completo de Productos**: Crear, editar y eliminar productos del inventario.
   - **Supervisión de Ventas**: Registro global de todas las órdenes de compra de la tienda.

---

## 🏛️ Estructura del Patrón MVC

```text
CRUD/
├── app/
│   ├── models/                 # [M] MODELOS (SQLAlchemy ORM)
│   │   ├── __init__.py
│   │   ├── product.py          # Definición de Productos e Inventario
│   │   ├── order.py            # Definición de Órdenes y Ventas
│   │   └── user.py             # Definición de Usuarios, Contraseñas y Roles
│   ├── views/                  # [V] VISTAS (Plantillas Jinja2 + UI)
│   │   └── templates/
│   │       ├── base.html       # Layout principal (Tailwind, Alpine.js, Chart.js)
│   │       ├── login.html      # Inicio de sesión
│   │       ├── register.html   # Registro de clientes
│   │       ├── user_store.html      # Tienda virtual, catálogo e historial
│   │       └── admin_dashboard.html # Dashboard analítico y CRUD de productos
│   ├── controllers/            # [C] CONTROLADORES (FastAPI Routers)
│   │   ├── __init__.py
│   │   ├── auth_controller.py  # Rutas de Autenticación, Hashing y Sesiones
│   │   └── store_controller.py # Lógica de tienda, compras y métricas de Chart.js
│   ├── database.py             # Configuración de la conexión a PostgreSQL
│   └── main.py                 # Punto de entrada de FastAPI y seeding de Admin
├── docker-compose.yml          # Orquestador de contenedores (Web + Postgres)
├── Dockerfile                  # Configuración de la imagen Python
├── requirements.txt            # Dependencias del proyecto (FastAPI, SQLAlchemy, Passlib, etc.)
└── README.md                   # Documentación oficial del sistema
```

---

## 🛠️ Tecnologías del Sistema

- **Backend**: FastAPI, Uvicorn, SQLAlchemy, Pydantic, Passlib (Bcrypt).
- **Base de Datos**: PostgreSQL 15 (con volumen persistente en Docker).
- **Frontend**: Jinja2 Templates, Tailwind CSS (CDN), Alpine.js (CDN), Chart.js (CDN).
- **Despliegue**: Docker & Docker Compose.

---

## ⚙️ Cómo Ejecutar el Sistema

1. Asegúrate de tener Docker y Docker Compose instalados en tu computadora.
2. Abre tu terminal en la carpeta raíz del proyecto y ejecuta:
   ```bash
   docker compose up -d --build
   ```
3. Abre tu navegador web en el puerto `8080`:
   👉 **[http://localhost:8080](http://localhost:8080)**
