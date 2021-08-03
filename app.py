import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Actor, Movie, db, setup_db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response

  @app.route('/actors', methods=['GET'])
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
  def delete_actor(jwt, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if actor is None:
        abort(404)
      
      actor.delete()
      return jsonify({
        'success': True,
        'deleted': actor_id
      })
    except:
      abort(422)
  
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(jwt, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if movie is None:
        abort(404)
      
      movie.delete()
      return jsonify({
        'success': True,
        'deleted': movie_id
      })
    except:
      abort(422)
  
  @app.route('/actors', methods=['POST'])
  def create_actor():
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
  def create_movie():
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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)