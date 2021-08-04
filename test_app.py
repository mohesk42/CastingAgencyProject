import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, setup_db

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZTczMzU4MmJjMDA2OTQ4MjA5MCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMTY0NzgsImV4cCI6MTYyODIwMjg3NywiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.lvpVzTgX9geSCTNOIUBFCSqWbPgF8mYVDnGPvIndMIK0DecacqOsz7lpnCqRykDgx31vGMJ9bOJwgog3k2BVYPE9Z7YACQrqCEdguc4iuRtxF3dLmG8PeBQ4FJEa1_R3AYzBPthXAH8HcawcQMv1KD_Dh6ynptrNklY4S-tnQssF3Zrazr16aPI4N65SB6SaWPjtAROxK1na7xx93moxmVFiI2ZxmtdHwANQB7OGoivO4G1dN7wKnNgZQNf0Ql974frCipx9XWfoWZN2aHo9shaa0PnATR1npLvo9r0fn6SjXXh5m_cX9ERVnNYUp_gD9hKhnlFxQs87t7Xgbt8Wzw'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWFlMjQ1NGYyMDA2YTI1NWNhYyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMTY1MjcsImV4cCI6MTYyODIwMjkyNiwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.ixTE5tl4MjYem3OEh0_a8rGsGScq4zUTwQoRw0tMM1HafkbsKaAERVm20waZ9qDYL6wEUGe1f0IGOUscOlTJOth7Py3EnVdlwPTBzEFcJ0j11q0ShXSL0rrzdVw6rpvDL2Em7UogUVocVIc5x5heAfHoVOwPq1xJG0HklrBy0kh7RmDNan5D-AnPKBOy9MEZeAtPVRt_54TthMYy6f4GtBsjhoDsJJhLOsiik2vBEkXIiXGWn8eS7hjq_OE6E794OoqB8IhtfrthnvIWrS4We0T75uBhLkU2K4SCvd5tMGJoNwzD1RcyCff-XHR44I-7xZP8JEa6Ivz60Q_9JUhs5Q'
EP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWRhMGY4NjY0MDA2OTJjZGMwMSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMTY1NzYsImV4cCI6MTYyODIwMjk3NSwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.JQ5TTVjPhlJ-BoBo2dxWGNexRMq87tTZDYS8Dbnz2dyJiWhVHudIQsiw6Tx7ufxIl1OZyxkqn4I-9eZySobGwb39pYNjwbWtnhM34gil7mVQXb2nlmLwEIjKS_7Hwl9Z1R7W6HPWWzTQ93jSkMqYuBqkT-2llsZVhAxIaQuPYCCgaydJfCyNPLxlgGiOD3VwHUK4odhCi8BUMqo95Kx8EjidJf-UJ2-8eCCgeQcXZ7MwgM6KxIwxw9AC-Ol65ehErbcwHoHeP0V5-P7nvzwHhSE2qtZQB_-ClFCy-Z2mD66a-12XpOTzkYsRuBFxsltZL8VO8I6Ve18hg7qnA76XQQ'

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

    def test_assistant_delete_movie(self):
        result = self.client().delete(
            '/movies/4',
            headers = {"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'User does not have permission')

    def test_assistant_edit_movie(self):
        movieData = {'title': 'Escape Room', 'release_date': '2018/1/10'}
        result = self.client().patch(
            '/movies/5',
            json = movieData,
            headers = {"Authorization": "Bearer " + ASSISTANT_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'User does not have permission')

    def test_director_delete_movie(self):
        result = self.client().delete(
            '/movies/4',
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'User does not have permission')

    def test_director_create_movie(self):
        movieData = {'title': 'Escape Room', 'release_date': '2018/1/10'}
        result = self.client().post(
            '/movies',
            json = movieData,
            headers = {"Authorization": "Bearer " + DIRECTOR_TOKEN}
        )
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'User does not have permission')



if __name__ == "__main__":
    unittest.main()

        
