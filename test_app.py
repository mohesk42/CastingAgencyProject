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

    def test_get_actors(self):
        result = self.client().get(
            '/actors',
            headers = {"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        result = self.client().get(
            '/movies',
            headers = {"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_edit_movie(self):
        movieData = {'title': 'Escape Room', 'release_date': '2018/1/10'}
        result = self.client().patch(
            '/movies/1',
            json = movieData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'Escape Room')
        self.assertTrue(data['movie']['release_date'])

    def test_edit_movie_fail(self):
        movieData = {'title': 'Escape Room', 'release_date': '2018/1/10'}
        result = self.client().patch(
            '/movies/754',
            json = movieData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_actor(self):
        actorData = {'name': 'Faris', 'age': '41', 'gender': 'male'}
        result = self.client().patch(
            '/actors/1',
            json = actorData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Faris')
        self.assertEqual(data['actor']['age'], 41)
        self.assertEqual(data['actor']['gender'], 'male')

    def test_edit_actor_fail(self):
        actorData = {'name': 'Faris', 'age': '41', 'gender': 'male'}
        result = self.client().patch(
            '/actors/454',
            json = actorData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        result = self.client().delete(
            '/actors/2',
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_actor_fail(self):
        result = self.client().delete(
            '/actors/445',
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        result = self.client().delete(
            '/movies/2',
            headers = {"Authorization": "Bearer " + EP_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)

    def test_delete_movie_fail(self):
        result = self.client().delete(
            '/movies/666',
            headers = {"Authorization": "Bearer " + EP_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



if __name__ == "__main__":
    unittest.main()

        
