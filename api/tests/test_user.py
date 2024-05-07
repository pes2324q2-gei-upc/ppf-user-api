from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from common.models.user import User

import json

from rest_framework.authtoken.models import Token


class CreateUserTest(APITestCase):
    """
    Test Create User
    """

    def setUp(self):
        self.userFail = User.objects.create(
            username="failUser",
            birthDate="1998-10-06",
            password="failUser",
            email="failUser@gmail.com",
        )

    def testSuccessfulCreateUser(self):
        """
        Ensure the API call creates a user in the database.
        """

        username = "test"
        birthDate = "1998-10-06"
        password = "test"
        password2 = "test"
        email = "test@gmail.com"

        url = reverse("userListCreate")
        data = {
            "username": username,
            "birthDate": birthDate,
            "password": password,
            "password2": password2,
            "email": email,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        self.assertIsNotNone(user)

        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("username"), username)
        self.assertEqual(message.get("birthDate"), birthDate)
        self.assertEqual(message.get("email"), email)

    def testUserExists(self):
        """
        Ensure the API call returns an error if the user already exists.
        """

        username = "failUser"
        birthDate = "1998-10-06"
        password = "failUser"
        password2 = "failUser"
        email = "failUser@gmail.com"

        url = reverse("userListCreate")
        data = {
            "username": username,
            "birthDate": birthDate,
            "password": password,
            "password2": password2,
            "email": "distintUser@gmail.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("username"), "A user with that username already exists.")

        url = reverse("userListCreate")
        data = {
            "username": "distintUser",
            "birthDate": birthDate,
            "password": password,
            "password2": password2,
            "email": email,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("email"), "A user with that email already exists.")

    def incorrectPassword(self):
        """
        Ensure the API call returns an error if the password is incorrect.
        """

        url = reverse("userListCreate")
        data = {
            "username": "distintUser",
            "birthDate": "1998-10-06",
            "password": "distintUser",
            "password2": "distintUser2",
            "email": "distintUser@gmail.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("non_field_errors"), "Passwords must match.")


class ListUserTest(APITestCase):
    """
    Test List User
    """

    def setUp(self):
        self.user = User.objects.create(
            username="test", birthDate="1998-10-06", password="test", email="test@gmail.com"
        )
        self.user2 = User.objects.create(
            username="test2", birthDate="1998-10-06", password="test2", email="test2@gmail.com"
        )
        self.user3 = User.objects.create(
            username="test3", birthDate="1998-10-06", password="test3", email="test3@gmail.com"
        )

    def testSuccessfulListUser(self):
        """
        Ensure the API call returns a list of users.
        """

        url = reverse("userListCreate")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))

        # Check the number of users returned
        self.assertEqual(len(message), 3)

        # Check the details of the first user
        self.assertEqual(message[0].get("id"), self.user.pk)
        self.assertEqual(message[0].get("username"), self.user.username)
        self.assertEqual(message[0].get("first_name"), self.user.first_name)
        self.assertEqual(message[0].get("last_name"), self.user.last_name)
        self.assertEqual(message[0].get("birthDate"), self.user.birthDate)
        self.assertEqual(message[0].get("email"), self.user.email)
        self.assertEqual(message[0].get("points"), self.user.points)

        # Check the details of the second user
        self.assertEqual(message[1].get("id"), self.user2.pk)
        self.assertEqual(message[1].get("username"), self.user2.username)
        self.assertEqual(message[1].get("first_name"), self.user2.first_name)
        self.assertEqual(message[1].get("last_name"), self.user2.last_name)
        self.assertEqual(message[1].get("birthDate"), self.user2.birthDate)
        self.assertEqual(message[1].get("email"), self.user2.email)
        self.assertEqual(message[1].get("points"), self.user2.points)

        # Check the details of the third user
        self.assertEqual(message[2].get("id"), self.user3.pk)
        self.assertEqual(message[2].get("username"), self.user3.username)
        self.assertEqual(message[2].get("first_name"), self.user3.first_name)
        self.assertEqual(message[2].get("last_name"), self.user3.last_name)
        self.assertEqual(message[2].get("birthDate"), self.user3.birthDate)
        self.assertEqual(message[2].get("email"), self.user3.email)
        self.assertEqual(message[2].get("points"), self.user3.points)


class GetUserTest(APITestCase):
    """
    Test Get User
    """

    def setUp(self):
        self.user = User.objects.create(
            username="test", birthDate="1998-10-06", password="test", email="test@gmail.com"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def testSuccessfulGetUser(self):
        """
        Ensure the API call returns the user information.
        """

        url = reverse("userRetriever", kwargs={"id": self.user.pk})
        headers = {
            "Authorization": f"Token {self.token}",
        }
        response = self.client.get(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.user.pk)
        self.assertEqual(message.get("username"), self.user.username)
        self.assertEqual(message.get("first_name"), self.user.first_name)
        self.assertEqual(message.get("last_name"), self.user.last_name)
        self.assertEqual(message.get("birthDate"), self.user.birthDate)
        self.assertEqual(message.get("email"), self.user.email)
        self.assertEqual(message.get("points"), self.user.points)

    def testUnauthorizedGetUser(self):
        """
        Ensure the API call returns an error if the user is not authenticated.
        """

        url = reverse("userRetriever", kwargs={"id": self.user.pk})
        response = self.client.get(url)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Authentication credentials were not provided.")

    def testUserNotExists(self):
        """
        Ensure the API call returns an error if the user does not exist.
        """

        url = reverse("userRetriever", kwargs={"id": 1000})
        headers = {
            "Authorization": f"Token {self.token}",
        }
        response = self.client.get(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Not found.")
