# Casting Agency Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This API has 3 types of users:

1. Assistant
2. Director
3. Executive Producer 

## URL
1. Heroku: https://casting-agency2442.herokuapp.com/
2. Localhost: localhost:5000

## Authentication

You can use this [link](https://casting-agency-2442.us.auth0.com/authorize?audience=casting&response_type=token&client_id=PHKxBKUlD0kQmZLudJ6IDWFVbmWGMLAq&redirect_uri=https://127.0.0.1:8080/) to login using the credentials provied for each role. 

## Setup for local

## Install requirements

```
pip install -r requirements.txt
```

## Setup database
Use the following commands to create the database and supply it with data
```
createdb castingagencydb
python manage.py db upgrade
python manage.py seed
```

## To start the server
First excute this command to setup environment variables
```
bash setup.sh
```

Then use the following commands to start the the server 
```
export FLASK_APP=app
flask run
```
Then you can use the link provided in the output.

## Testing
To run the tests, use the commands
```
dropdb castingagencydb
createdb castingagencydb
python manage.py db upgrade
python manage.py seed
python test_flaskr.py
```

## API Documentation

### Getting Started
- Base URL: `http://127.0.0.1:5000/` or live at `https://casting-agency2442.herokuapp.com/` 
- Authentication: the authentication is deployed using Auth0 service.

### RBAC
There are three roles: 

1. Casting Assistant: 
* permissions: get:actors, get:movies
2. Casting Director
* permissions: get:actors, get:movies, add:actors, delete:actors, edit:actors, edit:movies 
3. Executive Producer
* permissions: get:actors, get:movies, add:actors, delete:actors, edit:actors, edit:movies, add:movies, delete:movies

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: unprocessable 

### Endpoints 
#### GET /actors
- General:
    - Returns all actors.
    - and success status.
    - Require users of type assistant, director, and executive producer
- RBAC:
    - get:actors
- Sample: `curl http://127.0.0.1:5000/actors`

```
{
    "actors": [
        {
            "age": 29,
            "gender": "Female",
            "id": 1,
            "name": "Nemo"
        },
        {
            "age": 22,
            "gender": "Male",
            "id": 2,
            "name": "Basil"
        },
        {
            "age": 44,
            "gender": "male",
            "id": 3,
            "name": "Fahad"
        }
    ],
    "success": true
}
```

#### GET /movies
- General:
    - Returns all movies.
    - and success status.
    - Require users of type assistant, director, and executive producer

- RBAC:
    - get:movies

- Sample: `curl http://127.0.0.1:5000/movies`

```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Wed, 01 Jan 2020 00:00:00 GMT",
            "title": "Ice Land"
        },
        {
            "id": 2,
            "release_date": "Thu, 03 Apr 2014 00:00:00 GMT",
            "title": "Fire"
        }
    ],
    "success": true
}
```

#### DELETE '/actors/<id>'
- General:
    - Delete an actor.
    - return success status and deleted actor ID.
    - Require users of type director, and executive producer

- RBAC:
    - delete:actors

- Sample: `curl http://127.0.0.1:5000/actors/1 -X DELETE`

```
{
    "deleted": 1,
    "success": true
}
```

#### DELETE '/movies/<id>'
- General:
    - Delete a movie.
    - return success status and deleted movie ID.
    - Require users of type executive producer

- RBAC:
    - delete:movies

- Sample: `curl http://127.0.0.1:5000/movies/1 -X DELETE`

```
{
    "deleted": 1,
    "success": true
}
```

#### POST '/actors'
- General:
    - create new actor.
    - return sucess status and actor data.
    - Require users of type director, and executive producer

- RBAC:
    - add:actors
 
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Ahmed", "age": "44", "gender": "male"}'`

```
{
    "actor": {
        "age": 44,
        "gender": "male",
        "id": 4,
        "name": "Ahmed"
    },
    "success": true
}
```

#### POST '/movies'
- General:
    - create new movie.
    - return sucess status and movie data.
    - Require users of type executive producer

- RBAC:
    - add:movies
 
- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "Titanc", "release_date": "1990/1/1"}'`

```
{
    "movie": {
        "id": 3,
        "release_date": "Mon, 01 Jan 1990 00:00:00 GMT",
        "title": "Titanc"
    },
    "success": true
}
```

#### PATCH '/actors/<id>'
- General:
    - edit actor.
    - return sucess status and actor data.
    - Require users of type director, and executive producer

- RBAC:
    - edit:actors
 
- Sample: `curl http://127.0.0.1:5000/actors/4 -X PATCH -H "Content-Type: application/json" -d '{ "name": "Nasser", "age": "44", "gender": "male"}'`

```
{
    "actor": {
        "age": 44,
        "gender": "male",
        "id": 4,
        "name": "Nasser"
    },
    "success": true
}
```

#### PATCH '/movies/<id>'
- General:
    - edit movie.
    - return sucess status and movie data.
    - Require users of type director, and executive producer

- RBAC:
    - edit:movies
 
- Sample: `curl http://127.0.0.1:5000/movies/3 -X PATCH -H "Content-Type: application/json" -d '{ "title": "Titanc", "release_date": "1995/1/1"}'`

```
{
    "movie": {
        "id": 3,
        "release_date": "Mon, 01 Jan 1995 00:00:00 GMT",
        "title": "Titanc"
    },
    "success": true
}
```
