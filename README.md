# flask-template
This is a basic template which can be used for creating flask based APPs and APIs. It is influenced by Miguel Grinberg's [flasky](https://github.com/miguelgrinberg/flasky) project, which provides an amazing guide to generate flask apps.

The project creates a basic web app for creating and viewing short stories. These stories can be viewed, created and edited through API endpoints, and through a very basic web page.

The idea is to have a ready project structure whenever a quick flask app needs to be created. The project structure can be used for scaling for bigger projects as well.


## Virtual Environment Setup

The project uses Python3.6. In order to get started, you can set up a virtual env with:
```
virtualenv venv -p python3.6
```

This will create a python3.6 based virtualenv for you. Note: You need to have [Python3.6](https://www.python.org/downloads/release/python-360/) installed on your local device.

To install the necessary packages:
```
source venv/bin/activate
pip install -r requirements.txt
```

This will install the required packages within your virtualenv.

## The Makefile

When you are in the project directory on your terminal, you can use the `make` command for various options such as generating a new `reqirements.txt` file, installing requirements on your virtualenv or cleaning old compiled python `.pyc` files.

Try it out by entering the `make` command, which will show you available options.

## .ENV File

You will need to create a .env file, which can easily be created using the `.env.template`. Just run a simple copying command:
```
cp .env.template .env
```
and your .env file should be ready to be configured.

Variables in the .env file and their meanings:

- ENV: The config you want to use while setting up your app.
- CLIENT_LOGGER: Your client logger level
- FILE_LOGGER: Your file logger level
- Database configurations: these are used for configuring your postgres database
- SECRET_KEY: Flask's secret key which is used for hashing and security purposes. Make sure to keep this secret and don't commit to github.

The configurations are carried to code through the `decouple` library, which IMO provides a better solution compared to the traditional `python-dotenv` library.


## Project Structure

### Main Modules
Every flask application has a top-level module for creating the app itself, in this case, this module is the `stories.py`. This contains the flask application, and is used by other services such as Gunicorn or Flask's CLI while serving the application.

The `stories.py` module relies on the `config.py` and the `app/__init__.py` modules. It uses one of the configs specified in the `.env` file to create an application through the `create_app` method created under the `__init__.py` module.

`app/__init__.py` ties the necessary packages such as your SQLAlchemy or Migrations packages to your app, and provides a nice function for generating an application through with a pre-specified config.

`config.py` hold multiple configuration files, which can be used in different scenarios such as testing vs production.

### Models
The models, which are your database objects, are handled through SQLAlchemy's ORM. Flask provides a wrapper around the traditional SQLAlchemy package, which is used through out this project.

The models created are similar to your regular Python classes. They are inherited from pre-specified SQLAlchemy classes to make database table creation processes easier. These models can be found under the `app/models` folder.

In some projects, models can be handled within only one module, however in my opinion, it makes things easier when you handle them in multiple modules (one module per model).

If you want to create more models in your application, you can simply create modules under this folder, and later on tie them back to your app.


### API
The project creates a simple API which has 4 endpoints for retrieving, creating and editing stories. The API is structured by using Flask's `blueprint` functionality.

`api/stories.py` module creates the endpoints, where the `api/__init__.py` creates the blueprint for API formation.

The blueprint object is later on imported and tied to the app in the `app/__init__.py` module.

### Main APP (Web Page)
The project also creates a very simple web page for viewing and creating stories. The flow for this logic is handled under the `app/main` folder. `forms.py` basically creates a very simple web form for creating a story, while the views handled in the `views.py` module.

Like the API, the web page relies on a blueprint, which is initiated in the `__init__.py` module.

The HTML and Static files required for rendering the web page can be found under the `templates` and `static` folder. (Although there is nothing in the static folder at the moment)

### Logging

Logging is handled through flask's logger. However, custom handlers for logging is created under the `app/utils/logging.py` module, which are tied to application when initiated with the docker config. (Can be found under the `config.py` module.)

The rotating handler creates rotating logs under the logs folder, while the stream handler logs to the terminal/client. Other logger handlers can be placed here such as an SMTP logger (for emailing errors).


## Database Choice & Operations

Usually for smaller projects, databases such as SQLite is preferred for the ease of use. However, in most of the production environments, these databases are never used so learning how to set them up might because useless for larger commercial projects.

Keeping this in mind, even though the project is quite small, I went the extra mile to setup a proper PostgreSQL database. The configurations for this database is specified under the `.env` file, and it is set as the default database.

Python uses `psycopg2` driver to connect to postgres databases. It quite easy to install psycopg2 on Linux OS, however you may need to get Homebrew on your Mac to make your installation easier for you.

### Setting up a Postgres Database
Assuming that you have installed postgres database (if you haven't [Homebrew](https://gist.github.com/sgnl/609557ebacd3378f3b72) is the way I prefer for installations on Mac, and with [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04), its even easier), you can easily setup a database through your terminal.

After reaching the postgres terminal through a `PSQL` command such as
```
sudo -u postgres psql
```

You can create a new user and make the user a superuser for your project by
```
create user tester with password 'password';
alter user tester superuser;
```
(Making the user a superuser makes things easier when creating tables or databases)

And then create a database and grant priveleges locally by
```
create database stories;
grant all privileges on database stories to tester;
```
Granting privileges allows your user to make changes to your database.

Make sure you save these information, and add them to your `.env` file so your code can make changes to the database

On your `.env` file, you will want to set your `database_host` variable to `localhost`, and probably your database will be operating on port (`database_port`) `5432` unless specified otherwise.

For this case, your `database_name` will be `stories`, `database_user` will be `tester` and `database_password` will be `password`.

This should do it with the database setup!

### Migrations

Database migrations is handled through Flask's Migrate Package, which provides a wrapper around Alembic. Migrations are done for updating and creating necessary tables/entries in your database. Flask provides a neat way of handling these.

After exporting your flask CLI to point towards your application (for example in this case it can be done with):
```
export FLASK_APP=stories.py
```
You can find the necessary database commands with:
```
flask db
```
Initially, if you were to create an app from scratch, you would need to initiate your migrations with:
```
flask db init
```
In this case migrations folder is already there. So, you won't have to initiate it. This folder can be used when in the future, once you start altering your models. For example, when you add or remove fields or create new models.

For generating new migrations, you can use:
```
flask db migrate
```
And for applying your new migrations to your database, you can use:
```
flask db upgrade
```

The project also creates a shortcut for upgrading, which is added to FLask's CLI:
```
flask deploy
```

## Running the Application
Once you have setup your database, you are ready to run the application.
Assuming that you have exported your app's path by:
```
export FLASK_APP=stories.py
```

You can go ahead and run the application with a simple command:
```
flask run
```

You can also run your app using [Gunicorn](http://gunicorn.org/), which a separate WSGI Server that plays very well with Flask:
```
gunicorn --reload stories:app
```


## Docker Setup
The project also has docker functionality, which means you can run it using Docker as well!

Docker creates containers for you, and basically serves your application using these containers. The necessary setting files for the docker setup can be found under `docker-compose.yaml` and `Dockerfile` it self.

In this case, docker uses a prebuilt Python3.6 image that runs on Ubuntu, and creates Nginx reverse proxy and Postgres database containers to serve the application.

To build the docker image, simply run:
```
sudo docker-compose up --build
```

Once its built, it will do the necessary migrations for your application, and your app will be running straight away. You do not need to specify the `--build` command a second time to run the docker compose instance:
```
sudo docker-compose up
```

## Finally

Hope this guide/template comes useful to you!

## Acknowledgements
Many thanks to [Jose Rivera-Rubio](https://github.com/jmrr) for his help with the docker setup!



## Todos and Improvements
1. Add tests
2. Add a create a story button on the main page

