import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Actor, Movie, db, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
      'Content-Type,Authorization,true')

    response.headers.add('Access-Control-Allow-Methods',
      'GET,POST,PATCH,DELETE,OPTIONS')

    return response

  @app.route('/')
  def index():
    return jsonify({
      'message': 'Hello'
    })

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(jwt):
    actors = Actor.query.all()

    actorsList = []
    for actor in actors:
      actorsList.append(actor.format())
    
    if len(actorsList) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'actors': actorsList
      }), 200
  
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(jwt):
    movies = Movie.query.all()
    
    moviesList = []
    for movie in movies:
      moviesList.append(movie.format())
    
    if len(moviesList) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'movies': moviesList
      }), 200
  
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    try:
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': actor_id
      }), 200
    except:
      abort(422)
  
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    try:    
      movie.delete()
      return jsonify({
        'success': True,
        'deleted': movie_id
      }), 200
    except:
      abort(422)
  
  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actors')
  def create_actor(jwt):
    body = request.get_json()

    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()
      return jsonify({
        'success': True,
        'actor': actor.format()
      }), 201
    except:
      abort(422)
  
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movies')
  def create_movie(jwt):
    body = request.get_json()

    title = body.get('title', None)
    releaseDate = body.get('release_date', None)

    try:
      movie = Movie(title=title, releaseDate=releaseDate)
      movie.insert()
      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 201
    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('edit:actors')
  def edit_actor(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)
    
    body = request.get_json()
    if 'name' in body:
      actor.name = body.get('name', None)
    if 'age' in body:
      actor.age = body.get('age', None)
    if 'gender' in body:
      actor.gender = body.get('gender', None)
    
    actor.update()
    return jsonify({
      'success': True,
      'actor': actor.format()
    }), 200

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('edit:movies')
  def edit_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)
    
    body = request.get_json()
    if 'title' in body:
      movie.title = body.get('title', None)
    if 'release_date' in body:
      movie.releaseDate = body.get('release_date', None)
    
    movie.update()
    return jsonify({
      'success': True,
      'movie': movie.format()
    }), 200

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500

  @app.errorhandler(AuthError)
  def AuthErrorP(error):
      response = jsonify(error.error)
      response.status_code = error.status_code
      return response

  return app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
