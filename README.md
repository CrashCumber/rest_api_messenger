# REST API FOR MESSENGER ON FLASK

#### To see all endpoints and structure of api requests read [API_README.md](API_README.md)

<!--### App structure

Files:

* `README.md`
* `config.py` - This is a config file of this RESTful API Server example.
* `Dockerfile` - Docker config file which is used to build a Docker image
  running this RESTful API Server example.
*
* `.gitignore` - Lists files and file masks of the files which should not be
  added to git repository.
* `auth_views.py, chat_views.py, user_views.py` - functions and its routes.
* `models.py` - models of database`s tables. 
* `forms.py` - forms of client`s entry.
*  `__init__` - creation app, migrate, db, bcrypt objects.
*  `docker-compose.yml` - File of 
-->
## Main dependencies. 

- Python 3+
- Flask framework
- SQLAlchemy, flask-sqlalchemy - for Database ORM.
- Bcrypt - for password hashing.
- Alembic - for DB migrations.
- WTForms - for flask form.
- all dependencies you can see in requirements.txt ...


## Build and launch the app
### Using Docker
##### The first build

1. You need mysql docker image, for downloading it execute:  
`docker pull mysql`
2. Clone the Project 
3. Build the project with:  
`docker-compose build`
4. First launch with:  
`docker-compose up`

##### To start and stop the app later
- `docker-compose start`
- `docker-compose stop`

### From sources
1. Clone the Project
2. Setup Environment  
`pip install pipenv`
3. Install dependencies  
`pip install -r requirements.txt`
4. Initialization database and execution migrations   
`python manage.py runserver db init`
`python manage.py runserver db migrate`
`python manage.py runserver db upgrate`   
After these commands folder`migrations` will be created. It includes database  migrations and versions (execute `python manage.py runserver db -?` to see all  commands with database)
5. Run server  
`python manage.py runserver -h 0.0.0.0 -p 5000`

* You can start the server with different options. To see them execute: `python manage.py runserver -?` 

##### App is accessed on http://0.0.0.0:5000/


