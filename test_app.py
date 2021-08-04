import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Movie, Actor, setup_db

ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZTczMzU4MmJjMDA2OTQ4MjA5MCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMDA5NTYsImV4cCI6MTYyODE4NzM1NSwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Y8KDJ0hJBnSyYXaY_l9io0zC_o36Ce4IGiCbFf_P8oGp6JQhVJYwq16ZwmptzpjkWjIt-ag593gldtQHVsrQJjatzU1Yi05srp4YTUOz-VGnqTStjHcT5vYacpfDYN1aEkyudCTUbxD_pKOPjrwNZSd0dlnck_wn-n5WmdNPmDkllvAny3y7lPk6UFIJsehQu7Bj-L1e8gg2JtRuMt0lwCgF1owlPYt7dXaAfqQi0KC2IBluwXtP0LOETxb_uHiKE36uNE_gGPx0b7j8hYJpms_xkFXdDsf8PiarLENShF-3snq0XCQUNohk-IFiMLRhW6jpO9TBgTEjH5-kgSwI7A'
DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWFlMjQ1NGYyMDA2YTI1NWNhYyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMDEwMTEsImV4cCI6MTYyODE4NzQxMCwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZWRpdDphY3RvcnMiLCJlZGl0Om1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.r4Q2O2A0ge-rc8Y7MSiZ23coZvAPxdsYVxF990r8rLDcznpYkyJTqeRcb_GxwTORrOEqxKWmsLCSXHlIHiMmYmPbpQZk-K00KS-nshO4bEVk6mFDwig_esPpZo9PC7u9H93iyEeO01G1dXSuby5V8zsjSHR40WfLKC5tWR3vV85YKqpaef6jTQg0Smh68eAXx3ogHjJ47xIceQ5RxPVJot0RZAYvHONGRuwtZiF-MlKIO8tc_jNPKjiE-rLNM5qwJQ7n8ubvmej-rljajUeoyg8EFlSmpf5kyCntxNsUAl2uI2hFfJo0mlQVqckRwyywoS4WxXFTt7r_GL4V3i5Iuw'
EP_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxUR0M4NHp1c3J2WUhaZnZoWG5iWiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LTI0NDIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMGFjZWRhMGY4NjY0MDA2OTJjZGMwMSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MjgxMDEwNTksImV4cCI6MTYyODE4NzQ1OCwiYXpwIjoiUEhLeEJLVWxEMGtRbVpMdWRKNklEV0ZWYm1XR01MQXEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.HbAllZt1sWZHRZht5GRrTKbbufeoiz43qPsUM75dJEFARQOym1jjNSSkjiivZF-keYNxA9NFySYN211uldsR6-5qYx2WPtkt602-8ee2vrqv7xMsRN4JdBLnorrYjT2UDbFFRyVj4mnB2FhzxdKXYl8L0PygTJvjYSHCMKfJLNI0BuvkqmlQolmIz6ARFuUOfA-_tWWI1pBc9xc4LL2I8si6A_756dSilkvP3ONoj_HKZaGzYH26yyoYRJBHrM9OJ9sG1PSitGm5WYr8YbjzoUW-ygIde8nYdx5VGbEfuxCYed8flo8g5vno9kbDWwXN84n4piuYAo5rvvSpqE65Bw'

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

        
