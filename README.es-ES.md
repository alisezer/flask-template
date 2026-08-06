

# flask-template

## Introducción

Flask es uno de los frameworks populares de desarrollo web disponibles en el ecosistema de Python, junto con otros como Django y Tornado. Personalmente, lo prefiero a los demás porque ofrece un enfoque minimalista. Viene con envoltorios y paquetes auxiliares muy básicos, y puedes elegir instalar piezas específicas del rompecabezas a medida que desarrollas tu proyecto y descubres lo que necesitas.

Recientemente, el desarrollador de Flask, Miguel Grinberg, publicó un proyecto en github donde mostró una manera muy útil de estructurar aplicaciones web basadas en Flask. El proyecto es [flasky](https://github.com/miguelgrinberg/flasky).

Me inspiré en flasky y quería crear y compartir una plantilla basada en Flask que pudiera utilizarse para crear aplicaciones Flask rápidamente. Realicé algunos cambios menores a la estructura original del proyecto flasky y también decidí utilizar una base de datos y una configuración de docker diferentes, que en mi opinión están más orientadas al desarrollo web comercial.

Creé una aplicación web muy básica de relatos cortos, que es más una plantilla que una aplicación web completa y funcional. Permite a los usuarios crear, ver y editar relatos cortos a través de una API y también a través de una página web HTML muy básica.

La siguiente guía proporciona información sobre cómo funcionan las distintas partes del proyecto y, con suerte, no es demasiado complicada para que incluso un desarrollador Python principiante pueda seguirla.

---

## Configuración del Proyecto

### Primeros Pasos

Puedes comenzar descargando un archivo zip del proyecto a través de github o utilizando un comando git para clonar el proyecto mediante:

```bash
git clone https://github.com/alisezer/flask-template.git
```

### Configuración del Entorno Virtual

Se prefiere crear un entorno virtual por proyecto, en lugar de instalar todas las dependencias de cada uno de tus proyectos a nivel del sistema. Una vez que instales [virtual env](https://virtualenv.pypa.io/en/stable/installation/) y te dirijas al directorio de tu proyecto a través de la terminal, puedes configurar un entorno virtual con:

```bash
virtualenv venv -p python3.6
```

Esto creará un entorno virtual basado en python3.6 (venv) para ti dentro del directorio de tu proyecto.

Nota: Necesitas tener [Python 3.6](https://www.python.org/downloads/release/python-360/) instalado en tu dispositivo local.

### Instalación de Dependencias

Para instalar los paquetes necesarios:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Esto instalará los paquetes requeridos dentro de tu venv.

### El Makefile

Cuando estés en el directorio del proyecto en tu terminal, puedes usar el comando `make` para varias opciones, como generar un nuevo archivo `requirements.txt`, instalar los requisitos en tu venv o limpiar los archivos `.pyc` compilados antiguos.

Pruébalo ingresando el comando `make`, que te mostrará las opciones disponibles.

### Archivo .ENV

El archivo .env contiene la configuración específica de tu proyecto, como el nombre de host de tu BD. En la mayoría de los casos, es mejor mantener estos ajustes en secreto, por lo que el archivo .env nunca se confirma en git. Deberás crear un archivo .env, que puede crearse fácilmente utilizando `.env.template`. Solo ejecuta un simple comando de copia:

```bash
cp .env.template .env
```

y tu archivo .env estará listo para ser configurado.

Variables en el archivo .env y sus significados:

- ENV: La configuración que deseas utilizar al configurar tu aplicación.
- CLIENT_LOGGER: El nivel de registro de tu cliente
- FILE_LOGGER: El nivel de registro de tu archivo
- Configuraciones de base de datos: se utilizan para configurar tu base de datos postgres
- SECRET_KEY: La clave secreta de Flask que se utiliza para fines de hashing y seguridad. Asegúrate de mantenerla en secreto y no hacer commit en github.

Las configuraciones se llevan al código a través de la biblioteca `decouple`, que en mi opinión ofrece una mejor solución en comparación con la biblioteca tradicional `python-dotenv`.

---

## Estructura del Proyecto

### Módulos Principales

Cada aplicación Flask tiene un módulo de nivel superior para crear la propia aplicación; en este caso, este módulo es `stories.py`. Este contiene la aplicación Flask y es utilizado por otros servicios como Gunicorn o la CLI de Flask al servir la aplicación.

El módulo `stories.py` depende de los módulos `config.py` y `app/__init__.py`. Utiliza una de las configuraciones especificadas en el archivo `.env` para crear una aplicación a través del método `create_app`, que se encuentra en el módulo `__init__.py`.

`app/__init__.py` vincula los paquetes necesarios, como los envoltorios de SQLAlchemy o Migrations, a tu aplicación y proporciona una función conveniente para generar una aplicación con una configuración predeterminada.

`config.py` contiene múltiples archivos de configuración, que pueden utilizarse en diferentes escenarios, como pruebas frente a producción.

### Modelos

Los modelos, que son tus objetos de base de datos, se manejan a través del ORM de SQLAlchemy. Flask proporciona un envoltorio alrededor del paquete tradicional de SQLAlchemy, que se utiliza en todo este proyecto.

Los modelos creados son similares a tus clases Python regulares. Heredan de clases SQLAlchemy predeterminadas para facilitar los procesos de creación de tablas en la base de datos. Estos modelos se pueden encontrar en la carpeta `app/models`.

En algunos proyectos, los modelos pueden manejarse dentro de un solo módulo; sin embargo, en mi opinión, es más fácil manejarlos en múltiples módulos (un módulo por modelo).

Si deseas crear más modelos en tu aplicación, simplemente puedes crear módulos dentro de esta carpeta y, más adelante, vincularlos nuevamente a tu aplicación.

### API

El proyecto crea una API simple que tiene 4 endpoints para recuperar, crear y editar relatos. La API se estructura utilizando la funcionalidad `blueprint` de Flask.

El módulo `api/stories.py` crea los endpoints, donde `api/__init__.py` crea el blueprint para la formación de la API.

El objeto blueprint se importa y vincula a la aplicación posteriormente en el módulo `app/__init__.py`.

### APP PRINCIPAL (Página Web)

El proyecto también crea una página web muy simple para ver y crear relatos. El flujo para esta lógica se maneja en la carpeta `app/main`. `forms.py` básicamente crea un formulario web muy simple para crear un relato, mientras que las vistas se manejan en el módulo `views.py`.

Al igual que la API, la página web depende de un blueprint, que se inicia en el módulo `__init__.py`.

Los archivos HTML y estáticos para CSS necesarios para renderizar y estilizar las páginas web se pueden encontrar en las carpetas `templates` y `static`. (Aunque por el momento no hay nada en la carpeta static)

### Registro (Logging)

El registro se maneja a través del logger de Flask. Sin embargo, se crean controladores personalizados para el registro en el módulo `app/utils/logging.py`, los cuales se vinculan a la aplicación al iniciarse con la configuración de docker. (Pueden encontrarse en el módulo `config.py`.)

El controlador rotativo crea registros rotativos en la carpeta de logs, mientras que el controlador de flujo registra en la terminal/cliente. Otros controladores de registro pueden colocarse aquí, como un logger SMTP (para enviar errores por correo electrónico).

---

## Elección de Base de Datos y Operaciones

Por lo general, para proyectos más pequeños, se prefieren bases de datos como SQLite por facilidad de uso. Sin embargo, en la mayoría de los entornos de producción, estas bases de datos nunca se utilizan, por lo que aprender a configurarlas podría ser inútil para proyectos comerciales más grandes.

Teniendo esto en cuenta, aunque el proyecto es bastante pequeño, me esforcé más para configurar una base de datos PostgreSQL adecuada. Las configuraciones para esta base de datos se especifican en el archivo `.env` y se establecen como base de datos predeterminada.

Python utiliza el controlador `psycopg2` para conectarse a bases de datos postgres. Es bastante fácil instalar psycopg2 en sistemas operativos basados en Linux, sin embargo, es posible que necesites Homebrew en tu Mac para facilitar tu instalación.

### Configuración de una Base de Datos Postgres

Suponiendo que ya has instalado la base de datos postgres (si no lo has hecho, [Homebrew](https://gist.github.com/sgnl/609557ebacd3378f3b72) es la forma que prefiero para instalaciones en Mac, y con [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04), es aún más fácil), puedes configurar fácilmente una base de datos a través de tu terminal.

Después de acceder a la terminal de postgres mediante un comando `PSQL` como:

```bash
sudo -u postgres psql
```

Puedes crear un nuevo usuario y convertirlo en superusuario para tu proyecto mediante:

```bash
create user tester with password 'password';
alter user tester superuser;
```

(Convertir al usuario en superusuario facilita las cosas al crear tablas o bases de datos)

Y luego crea una base de datos y otorga privilegios localmente mediante:

```bash
create database stories;
grant all privileges on database stories to tester;
```

Otorgar privilegios permite a tu usuario realizar cambios en tu base de datos.

Asegúrate de guardar esta información y agregarla a tu archivo `.env` para que tu código pueda realizar cambios en la base de datos.

En tu archivo `.env`, querrás establecer tu variable `database_host` en `localhost`, y probablemente tu base de datos estará operando en el puerto (`database_port`) `5432` a menos que se especifique lo contrario.

En este caso, tu `database_name` será `stories`, `database_user` será `tester` y `database_password` será `password`.

¡Con esto debería ser suficiente para la configuración de la base de datos!

### Migraciones

Las migraciones de la base de datos se manejan a través del Paquete Migrate de Flask, que proporciona un envoltorio alrededor de Alembic. Las migraciones se realizan para actualizar y crear las tablas/entradas necesarias en tu base de datos. Flask proporciona una forma ordenada de manejar esto.

Después de exportar tu CLI de Flask para que apunte hacia tu aplicación (por ejemplo, en este caso puede hacerse con):

```bash
export FLASK_APP=stories.py
```

Puedes encontrar los comandos necesarios de base de datos con:

```bash
flask db
```

Inicialmente, si crearas una aplicación desde cero, necesitarías iniciar tus migraciones con:

```bash
flask db init
```

En este caso, la carpeta de migraciones ya existe. Por lo tanto, no tendrás que inicializarla. Una vez que comiences a modificar tus modelos, necesitarás crear nuevos scripts de migración. Por ejemplo, si agregas o eliminas campos de los modelos existentes o creas nuevos modelos, necesitarás generar nuevas migraciones y actualizar tu base de datos.

Para generar nuevas migraciones, puedes usar:

```bash
flask db migrate
```

Y para aplicar tus nuevas migraciones a tu base de datos, puedes usar:

```bash
flask db upgrade
```

El proyecto también crea un atajo para actualizar, que se agrega a la CLI de Flask:

```bash
flask deploy
```

---

## Ejecución de la Aplicación

Una vez que hayas configurado tu base de datos, estarás listo para ejecutar la aplicación.
Suponiendo que hayas exportado la ruta de tu aplicación mediante:

```bash
export FLASK_APP=stories.py
```

Puedes continuar y ejecutar la aplicación con un simple comando:

```bash
flask run
```

También puedes ejecutar tu aplicación usando [Gunicorn](http://gunicorn.org/), que es un Servidor WSGI independiente que funciona muy bien con Flask:

```bash
gunicorn --reload stories:app
```

---

## Configuración de Docker

El proyecto también tiene funcionalidad de docker, lo que significa que si tienes docker instalado en tu computadora, ¡también puedes ejecutarlo usando Docker!

Docker crea contenedores para ti y, básicamente, sirve tu aplicación utilizando estos contenedores. Los archivos de configuración necesarios para la configuración de docker se pueden encontrar en `docker-compose.yaml` y en el propio `Dockerfile`.

En este caso, docker utiliza una imagen Python3.6 precompilada que se ejecuta en Ubuntu, y crea contenedores de proxy inverso Nginx y base de datos Postgres para servir la aplicación.

Para construir la imagen de docker, primero, establece tu variable `ENV` dentro de tu archivo `.env` en `docker`.

Y luego, ejecuta:

```bash
sudo docker-compose up --build
```

Una vez construida, realizará las migraciones necesarias para tu aplicación y tu aplicación se ejecutará inmediatamente. No necesitas especificar el comando `--build` una segunda vez para ejecutar la instancia de docker compose:

```bash
sudo docker-compose up
```

Docker se vuelve especialmente útil al desplegar tus aplicaciones en servidores y facilita las tareas de DevOps. Puedes leer más sobre [docker](https://www.docker.com/).

---

## Finalmente

¡Espero que esta guía/plantilla te sea útil! Si tienes algún comentario, bueno o malo, por favor házmelo saber o siéntete libre de bifurcar el repositorio y enviar un PR.
Me encantaría discutir posibles mejoras. Además, he intentado dejar comentarios útiles dentro del propio código, por lo que explicaciones adicionales sobre lo que hace cada módulo pueden encontrarse en los comentarios y docstrings.

### Agradecimientos

Muchas gracias a [Jose Rivera-Rubio](https://github.com/jmrr) por su ayuda con la configuración de docker!

### Todo y Mejoras

1. Agregar pruebas
