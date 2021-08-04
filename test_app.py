import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, setup_db

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZTczMzU4MmJjMDA2OTQ4MjA5MCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgwOTkwODAsImV4cCI6MTYyODEwNjI4MCwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.msV1G56N9QhAENB0RabnVPpXKfw2vMqKH8ZtO4tOQJ1F8Oee9GghpsNpWI_izleVXTtOHoIwsD5THlgCoen2afbwHPS9N8lbPNJvAbUmm9vZMzsJOYAbtT66G0sc7RI-7pT0SuoabwNYEMPwkLShVjRb9LoA0PwZT_adCbVuern5xMR3VzstdzVICRAm4LsaAhzf2kf1UdaY9vbxNp_7zEibUqODwLxCc16vyaOZ3Y9wq2NtE1MExFtBrRZvXdZqX6ePRmmzub0y3-YmZnY3PPN1ci6qceN5GaBrvltCKIR_HQCaIkyUMvHu4TTJBEcVRY18QeqcTPMW3SmTEcDhQQ'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWFlMjQ1NGYyMDA2YTI1NWNhYyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgwOTgzMTYsImV4cCI6MTYyODEwNTUxNiwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.CUd-t3AKGR51SLRa5lWtEPbeBqT18QyoWJBBgIyu1ujmaoM4O2S_j_Z_3zxOToGvFb7b5iyzqUSmxxq1H2aqvyHPYgHXglBXwOvxXnG9Tbe_CjxABbUKdDmnOKsvNyH3rQVWGxBJDfbHSxKug2JBOGaHhnVFDbBHicfnQ76jlsoKtCHGG1QbhBKZLI9ynlufqXhlSoIYJ88YA3KgM0SNDVptMU46zJQ4YbPZ_J77mwLTPquDAHPyEv68a8rIQ6gOOYVjPLcAKOzdeQycSp0zfK3zlzZAum-i9IkYB0Lk9dQBOBoM87fgHSRetuqiXkOS8m8InUKie7DpIGH-_eJPMw'
EP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWRhMGY4NjY0MDA2OTJjZGMwMSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgwOTkxMjMsImV4cCI6MTYyODEwNjMyMywiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.dPWyrAs4Aj06FbJvkkOcEg3YSLJiCYOOXjRc8XeogiQxuqIE4cheVaYB5hQB008QpsgpQl92WBw3VJCzV5jvptlS-AQe5Vb03LW3JJAcvtQZuruvLWy0-OHZ6VN1XWNxP65t7LqvaFuwOv8MyLqBOR27_9eMOYZ5mZLRrEG1i6Si2mRY3Db0w4ow8i-d9fBJebZEOyUh7Bz02FMelmf8F1_kvkm_A62OMrei_AYUDjEHSXI3XwhpT2K-e26vx4tWlJEXPu_p69xhTW7Z0qOxQcHBk8lvgkAVUKBEFWClzBxM6T1Tmp6gTtg8SJR2mRzgdZxD4hR8T_BTysaMVsXi-w'

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

        
