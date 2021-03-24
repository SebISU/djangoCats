from django.contrib.auth.models import User
from .models import Cat, Loot, Hunting
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
import json


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="asdf", password="asdf")

    def test_login1(self):
        data = {
            "username" : "asdf",
            "password" : "asdf"
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login2(self):
        data = {
            "username" : "asdf",
            "password" : "assdf"
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsersTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="sdfg", password="sdfg")
        self.user2 = User.objects.create_user(username="dfgh", password="dfgh")
        self.cat = Cat.objects.create(owner=self.user1, name="roman", bodyColor="white")
        self.token1, _ = Token.objects.get_or_create(user=self.user1)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

    def test_users_authenticated(self):
        response = self.client.get("/users/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_users_second_user(self):
        response = self.client.get("/users/2/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            
    def test_users_not_found(self):
        response = self.client.get("/users/3/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/users/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    

class HuntingTestCase(APITestCase):

        def setUp(self):
            self.user1 = User.objects.create_user(username="sdfg", password="sdfg")
            self.user2 = User.objects.create_user(username="dfgh", password="dfgh")
            self.cat1 = Cat.objects.create(owner=self.user1, name="roman", bodyColor="white")
            self.cat2 = Cat.objects.create(owner=self.user2, name="arnold", bodyColor="black")
            self.token1, _ = Token.objects.get_or_create(user=self.user1)
            self.api_authentication()

        def api_authentication(self):
            self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        def test_user_unauthenticated(self):
            self.client.force_authenticate(user=None)
            response = self.client.get("/hunting/1/")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        def test_cat_not_found(self):
            response = self.client.get("/hunting/3/")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_user_cat_owner(self):
            response = self.client.get("/hunting/1/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_user_not_cat_owner(self):
            response = self.client.get("/hunting/2/")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        def test_user_unauthenticated_post(self):
            self.client.force_authenticate(user=None)
            response = self.client.post("/hunting/1/")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_cat_not_found_post(self):
            response = self.client.post("/hunting/3/")
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_user_not_cat_owner_post(self):
            response = self.client.post("/hunting/2/")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_cat_correct_post(self):
            response = self.client.post("/hunting/1/", json.dumps(
                {
                    "loots":["mouse", "rat", "fish", "bird"],
                    "hunter" : 1,
                    "dateStart" : "2021-03-22T16:25:02.536987Z",
                    "dateEnd" : "2022-03-22T19:25:02.536987Z"
                }),
                content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_cat_missing_data_post(self):
            response = self.client.post("/hunting/1/", json.dumps(
                {
                    "loots":["mouse", "rat", "fish", "bird"],
                    "hunter" : 1,
                    "dateEnd" : "2022-03-22T19:25:02.536987Z"
                }),
                content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_cat_wrong_hunter_post(self):
            response = self.client.post("/hunting/1/", json.dumps(
                {
                    "loots":["mouse", "rat", "fish", "bird"],
                    "hunter" : 5,
                    "dateStart" : "2021-03-22T16:25:02.536987Z",
                    "dateEnd" : "2022-03-22T19:25:02.536987Z"
                }),
                content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_cat_wrong_date_post(self):
            response = self.client.post("/hunting/1/", json.dumps(
                {
                    "loots":["mouse", "rat", "fish", "bird"],
                    "hunter" : 5,
                    "dateStart" : "2021-03-22T16:25:02.536987Z",
                    "dateEnd" : "2020-03-22T19:25:02.536987Z"
                }),
                content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_cat_wrong_loots_post(self):
            response = self.client.post("/hunting/1/", json.dumps(
                {
                    "loots":["mouse", "ratatuj", "fish", "bird"],
                    "hunter" : 5,
                    "dateStart" : "2021-03-22T16:25:02.536987Z",
                    "dateEnd" : "2022-03-22T19:25:02.536987Z"
                }),
                content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
