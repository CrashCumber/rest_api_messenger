# REST API FOR MESSENGER ON FLASK

#### To see all endpoints and structure of api requests read [API_README.md](API_README.md)


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
4. Run server  
`python manage.py runserver -h 0.0.0.0 -p 5000`

* You can start the server with different options. To see them execute: `python manage.py runserver -?` 

#####App is accessed on http://0.0.0.0:5000/


