import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
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
  def get_actors():
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
  def get_movies():
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
  def delete_actor(actor_id):
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
  def delete_movie(movie_id):
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


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)