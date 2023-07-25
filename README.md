# ![image](https://github.com/Zauler/OFO/assets/134193754/3cab8315-f0c9-42b1-bada-95fdbeee35b8)


## Descripción
El proyecto OFO (Order Flow Optimizer) es una aplicación web de control financiero y gestión de clientes desarrollada con **Python, Flask y SQLite**, que proporciona una interfaz de usuario intuitiva y funcional. Permite a los usuarios visualizar y explorar resultados financieros, así como integrar datos con otras herramientas y sistemas, lo que facilita la toma de decisiones basadas en información relevante y oportuna.

_La aplicación se ha integrado con una plantilla de Flask llamada [Light Bootstrap Flask](https://appseed.us/product/light-bootstrap-dashboard/flask/)_

<br />

## Características Principales
- 👉 Gestión de cuentas financieras: los usuarios pueden agregar, editar y eliminar cuentas financieras, como cuentas bancarias, tarjetas de crédito, inversiones, etc.
- 👉 Registro de transacciones: se pueden registrar ingresos y gastos, y categorizarlos para un seguimiento detallado.
- 👉 Gestión de clientes: permite almacenar información relevante de los clientes y realizar un seguimiento de las interacciones con ellos.
- 👉 Visualización de informes: ofrece informes financieros y de clientes en forma de gráficos y tablas para un análisis claro y comprensible.
- 👉 Integración con otras herramientas: posibilidad de integrar datos con herramientas de contabilidad y gestión de proyectos de terceros.
- 👉 Integración un ChatBot con Inteligencia Artificial para realizar consultas sobre los datos existentes.

<br />

## Capturas de Pantalla
![image](https://github.com/Zauler/OFO/assets/134193754/2670d647-2f28-43f5-927d-fd384d7e9378)

![image](https://github.com/Zauler/OFO/assets/134193754/9c3c03c7-2f7a-4f84-87e5-fd1f795ff412)

![image](https://github.com/Zauler/OFO/assets/134193754/9e0f3436-da02-4b92-b5a7-da540d71cb4f)

![image](https://github.com/Zauler/OFO/assets/134193754/1069f581-49d7-420e-afde-918b131fd692)


## 📐 Requisitos de Instalación

- 🚀 Clona el repositorio para empezar a trabajar con él. Crea un entorno virtual e instala el archivo requirements.txt
- Para arrancar la aplicación ejecutar **`python run.py`**
- Acceder por medio del navegador a `http://127.0.0.1:5500` o  a `http://localhost:5500`.

<br />

## 📜 Guía de Uso

- 👤 El usuario administrador por defecto es `ofo` y la contraseña `1234`. Una vez dentro, accede a la pestaña de gestión de usuarios y crea otro usuario administrador y elimina ofo.
- 👥 El usuario gestor (no tiene permisos de administrador) es `usuario1` y su contraseña es `1234`.

<br />

## ✨ Levantar la aplicación en Docker

> 👉 **Paso 1** - Descargar el código desde el repositorio (usando `GIT`) 

```bash
$ git clone https://github.com/app-generator/flask-light-bootstrap-dashboard.git
$ cd flask-light-bootstrap-dashboard
```

<br />

> 👉 **Paso 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br /> 

## ✨ How to use it

> Download the code 

```bash
$ git clone https://github.com/app-generator/flask-light-bootstrap-dashboard.git
$ cd flask-light-bootstrap-dashboard
```

<br />

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD 
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

### 👉 Create Users

By default, the app redirects guest users to authenticate. In order to access the private pages, follow this set up: 

- Start the app via `flask run`
- Access the `registration` page and create a new user:
  - `http://127.0.0.1:5000/register`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:5000/login`

<br />

## ✨ Estructura de la App

Este proyecto usa blueprints, una configuración dual (desarrollo y producción) y una estructura de archivos que se indica a continuación:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Define app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and register)
   |    |    |-- routes.py                  # Define authentication routes  
   |    |    |-- models.py                  # Defines models  
   |    |    |-- forms.py                   # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## Autores
- José Luis Martínez Soriano
- Jesús Gutiérrez Contreras
