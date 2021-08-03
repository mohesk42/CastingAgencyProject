import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, setup_db

ASSISTANT_TOKEN = ''
DIRECTOR_TOKEN = ''
EP_TOKEN = ''

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        pass

    def test_create_actor(self):
        actorData = {'name': 'Mohammad', 'age': '44', 'gender': 'male'}
        result = self.client().post(
            '/actors',
            json = actorData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 201)
        self.assertEqual(data['success'], True)
    
    def test_create_actor_fail(self):
        actorData = {'name': 'Mohammad', 'age': 'fgdfd', 'gender': 'male'}
        result = self.client().post(
            '/actors',
            json = actorData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_movie(self):
        movieData = {'title': 'Escape Plane', 'release_date': '2016/8/10'}
        result = self.client().post(
            '/movies',
            json = movieData,
            headers = {"Authorization": "Bearer " + EP_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_create_movie_fail(self):
        movieData = {'title': 'Escape Plane', 'release_date': 'sdfsdf'}
        result = self.client().post(
            '/movies',
            json = movieData,
            headers = {"Authorization": "Bearer " + EP_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

        
