"""
This module contains the tests for the driver.
"""
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from common.models.user import Driver, ChargerType, Preference

import json

from rest_framework.authtoken.models import Token


class CreateDriverTest(APITestCase):
    """
    Test Create Driver
    """

    def setUp(self):
        self.mennekes = ChargerType.objects.create(chargerType="Mennekes")
        self.tesla = ChargerType.objects.create(chargerType="Tesla")
        self.schuko = ChargerType.objects.create(chargerType="Schuko")
        self.chademo = ChargerType.objects.create(chargerType="ChadeMO")
        self.css_combo2 = ChargerType.objects.create(chargerType="CSS Combo2")
        self.driver = Driver.objects.create(
            username="driver1",
            birthDate="1998-10-06",
            email="driver@gmail.com",
            password="driver",
            dni="12345678",
            chargerTypes=[self.mennekes, self.tesla, self.schuko, self.chademo, self.css_combo2],
            preference=Preference.objects.create(),
            iban="ES662100999",
        )
        self.token, _ = Token.objects.get_or_create(user=self.driver)

    def testSuccessfulCreateUser(self):
        """
        Ensure the API call creates a user in the database.
        """

        url = reverse("driverListCreate")
        data = {
            "username": "test",
            "birthDate": "1998-10-06",
            "password": "test",
            "password2": "test",
            "email": "test@gmail.com",
            "chargerTypes": [self.mennekes.pk],
            "preference": {
                "canNotTravelWithPets": True,
                "listenToMusic": True,
                "noSmoking": True,
                "talkTooMuch": True,
            },
            "iban": "ES662100999",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            driver = Driver.objects.get(username="test")
        except Driver.DoesNotExist:
            driver = None
        self.assertIsNotNone(driver)

        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("username"), "test")
        self.assertEqual(message.get("birthDate"), "1998-10-06")
        self.assertEqual(message.get("email"), "test@gmail.com")
        self.assertEqual(message.get("chargerTypes"), [1])
        self.assertEqual(
            message.get("preference"),
            {
                "canNotTravelWithPets": True,
                "listenToMusic": True,
                "noSmoking": False,
                "talkTooMuch": True,
            },
        )
        self.assertEqual(message.get("iban"), "ES662100999")

    def testDriverExists(self):
        """
        Ensure the API call returns an error if the driver already exists.
        """

        url = reverse("driverListCreate")
        data = {
            "username": "driver1",
            "birthDate": "1998-10-06",
            "password": "driver",
            "password2": "driver",
            "email": "driver@gmail.com",
            "dni": "12345678",
            "chargerTypes": [self.mennekes.pk],
            "preference": {
                "canNotTravelWithPets": True,
                "listenToMusic": True,
                "noSmoking": True,
                "talkTooMuch": True,
            },
            "iban": "ES662100999",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("username"), "user with that username already exists.")
        self.assertEqual(message.get("email"), "user with that email already exists.")
        self.assertEqual(message.get("dni"), "driver with that dni already exists.")
        self.assertEqual(message.get("iban"), "driver with that iban already exists.")

    def ibanMoreThan36(self):
        """
        Ensure the API call returns an error if the iban is more than 36 characters.
        """

        url = reverse("driverListCreate")
        data = {
            "username": "test",
            "birthDate": "1998-10-06",
            "password": "test",
            "password2": "test",
            "email": "test@gmail.com",
            "chargerTypes": [self.mennekes.pk],
            "iban": "ES662100999123456789012345678901234567890",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("iban"), "Ensure this field has no more than 36 characters.")

    def dniHas8Characters(self):
        """
        Ensure the API call returns an error if the dni is not 8 characters.
        """

        url = reverse("userListCreate")
        data = {
            "username": "test",
            "birthDate": "1998-10-06",
            "password": "test",
            "password2": "test",
            "email": "test@gmail.com",
            "dni": "12345678X",
            "iban": "ES662100999",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("dni"), "Ensure this field has exactly 8 characters.")


class ListDriverTest(APITestCase):
    """
    Test List Driver
    """

    def setUp(self):
        self.mennekes = ChargerType.objects.create(chargerType="Mennekes")
        self.tesla = ChargerType.objects.create(chargerType="Tesla")
        self.schuko = ChargerType.objects.create(chargerType="Schuko")
        self.chademo = ChargerType.objects.create(chargerType="ChadeMO")
        self.css_combo2 = ChargerType.objects.create(chargerType="CSS Combo2")
        self.driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            chargerTypes=[self.mennekes],
            iban="ES662100999",
        )
        self.driver2 = Driver.objects.create(
            username="test2",
            birthDate="1998-10-06",
            password="test2",
            email="test2@gmail.com",
            dni="12345679",
            chargerTypes=[self.tesla],
            iban="ES662100991",
        )
        self.driver3 = Driver.objects.create(
            username="test3",
            birthDate="1998-10-06",
            password="test3",
            email="test3@gmail.com",
            dni="12345670",
            chargerTypes=[self.schuko],
            iban="ES662100990",
        )

    def testListDrivers(self):
        """
        Ensure the API call returns a list of drivers.
        """

        url = reverse("driverListCreate")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))

        # Check the number of drivers returned
        self.assertEqual(len(message), 3)

        # Check the details of the first driver
        self.assertEqual(message[0].get("id"), self.driver.pk)
        self.assertEqual(message[0].get("username"), self.driver.username)
        self.assertEqual(message[0].get("first_name"), self.driver.first_name)
        self.assertEqual(message[0].get("last_name"), self.driver.last_name)
        self.assertEqual(message[0].get("birthDate"), self.driver.birthDate)
        self.assertEqual(message[0].get("email"), self.driver.email)
        self.assertEqual(message[0].get("points"), self.driver.points)
        self.assertEqual(message[0].get("driverPoints"), self.driver.driverPoints)
        self.assertEqual(message[0].get("autonomy"), self.driver.autonomy)
        self.assertEqual(message[0].get("chargerTypes"), self.driver.chargerTypes)
        self.assertEqual(message[0].get("preference"), self.driver.preference)
        self.assertEqual(message[0].get("iban"), self.driver.iban)

        # Check the details of the second driver
        self.assertEqual(message[1].get("id"), self.driver2.pk)
        self.assertEqual(message[1].get("username"), self.driver2.username)
        self.assertEqual(message[1].get("first_name"), self.driver2.first_name)
        self.assertEqual(message[1].get("last_name"), self.driver2.last_name)
        self.assertEqual(message[1].get("birthDate"), self.driver2.birthDate)
        self.assertEqual(message[1].get("email"), self.driver2.email)
        self.assertEqual(message[1].get("points"), self.driver2.points)
        self.assertEqual(message[1].get("driverPoints"), self.driver2.driverPoints)
        self.assertEqual(message[1].get("autonomy"), self.driver2.autonomy)
        self.assertEqual(message[1].get("chargerTypes"), self.driver2.chargerTypes)
        self.assertEqual(message[1].get("preference"), self.driver2.preference)
        self.assertEqual(message[1].get("iban"), self.driver2.iban)

        # Check the details of the third driver
        self.assertEqual(message[2].get("id"), self.driver3.pk)
        self.assertEqual(message[2].get("username"), self.driver3.username)
        self.assertEqual(message[2].get("first_name"), self.driver3.first_name)
        self.assertEqual(message[2].get("last_name"), self.driver3.last_name)
        self.assertEqual(message[2].get("birthDate"), self.driver3.birthDate)
        self.assertEqual(message[2].get("email"), self.driver3.email)
        self.assertEqual(message[2].get("points"), self.driver3.points)
        self.assertEqual(message[2].get("driverPoints"), self.driver3.driverPoints)
        self.assertEqual(message[2].get("autonomy"), self.driver3.autonomy)
        self.assertEqual(message[2].get("chargerTypes"), self.driver3.chargerTypes)
        self.assertEqual(message[2].get("preference"), self.driver3.preference)
        self.assertEqual(message[2].get("iban"), self.driver3.iban)


class GetDriverTest(APITestCase):
    """
    Test Get Driver
    """

    def setUp(self):
        self.mennekes = ChargerType.objects.create(chargerType="Mennekes")
        self.driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        self.token, _ = Token.objects.get_or_create(user=self.driver)

    def testSuccessfulGetDriver(self):
        """
        Ensure the API call returns the driver.
        """

        url = reverse("driverRetriever", kwargs={"id": self.driver.pk})
        headers = {
            "Authorization": f"Token {self.token}",
        }
        response = self.client.get(url, format="json", headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.driver.pk)
        self.assertEqual(message.get("username"), self.driver.username)
        self.assertEqual(message.get("first_name"), self.driver.first_name)
        self.assertEqual(message.get("last_name"), self.driver.last_name)
        self.assertEqual(message.get("birthDate"), self.driver.birthDate)
        self.assertEqual(message.get("email"), self.driver.email)
        self.assertEqual(message.get("points"), self.driver.points)
        self.assertEqual(message.get("driverPoints"), self.driver.driverPoints)
        self.assertEqual(message.get("autonomy"), self.driver.autonomy)
        self.assertEqual(message.get("chargerTypes"), self.driver.chargerTypes)
        self.assertEqual(message.get("preference"), self.driver.preference)
        self.assertEqual(message.get("iban"), self.driver.iban)

    def testUnauthorizedGetDriver(self):
        """
        Ensure the API call returns an error if the user is not authenticated.
        """

        url = reverse("driverRetriever", kwargs={"id": self.driver.pk})
        response = self.client.get(url)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Authentication credentials were not provided.")

    def testDriverDoesNotExist(self):
        """
        Ensure the API call returns an error if the driver does not exist.
        """

        url = reverse("driverRetriever", kwargs={"id": 999})
        headers = {
            "Authorization": f"Token {self.token}",
        }
        response = self.client.get(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Not found.")


class UpdateDriverTest(APITestCase):
    """
    Test Update Driver
    """

    def setUp(self):
        self.mennekes = ChargerType.objects.create(chargerType="Mennekes")
        self.tesla = ChargerType.objects.create(chargerType="Tesla")
        self.driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        self.token, _ = Token.objects.get_or_create(user=self.driver)

    def testSuccessfulUpdateDriver(self):
        """
        Ensure the API call updates the driver.
        """

        url = reverse("driverRetriever", kwargs={"id": self.driver.pk})
        headers = {
            "Authorization": f"Token {self.token}",
        }
        dataPut = {
            "username": "test2",
            "first_name": "newFirstName",
            "last_name": "newLastName",
            "password": "test2",
            "password2": "test2",
            "birthDate": "1999-10-06",
            "autonomy": 100,
            "chargerTypes": [self.tesla.pk],
            "preference": {
                "canNotTravelWithPets": True,
                "listenToMusic": False,
                "noSmoking": True,
                "talkTooMuch": False,
            },
            "iban": "ES662100999",
        }
        # Complete PUT
        response = self.client.put(url, dataPut, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.driver.pk)
        self.assertEqual(message.get("username"), "test2")
        self.assertEqual(message.get("first_name"), "newFirstName")
        self.assertEqual(message.get("last_name"), "newLastName")
        self.assertEqual(message.get("birthDate"), "1999-10-06")
        self.assertEqual(message.get("autonomy"), 100)
        self.assertEqual(message.get("chargerTypes"), [self.tesla.pk])
        self.assertEqual(
            message.get("preference"),
            {
                "canNotTravelWithPets": True,
                "listenToMusic": False,
                "noSmoking": True,
                "talkTooMuch": False,
            },
        )
        self.assertEqual(message.get("iban"), "ES662100999")

        # Partial PUT
        dataPut2 = {
            "iban": "FR0239876567",
        }
        response = self.client.put(url, dataPut2, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.driver.pk)
        self.assertEqual(message.get("username"), "test3")
        self.assertEqual(message.get("first_name"), self.driver.first_name)
        self.assertEqual(message.get("last_name"), self.driver.last_name)
        self.assertEqual(message.get("birthDate"), self.driver.birthDate)
        self.assertEqual(message.get("autonomy"), self.driver.autonomy)
        self.assertEqual(message.get("chargerTypes"), self.driver.chargerTypes)
        self.assertEqual(message.get("preference"), self.driver.preference)
        self.assertEqual(message.get("iban"), "FR0239876567")

        # Complete PATCH
        dataPatch = {
            "username": "test4",
            "first_name": "newFirstName2",
            "last_name": "newLastName2",
            "password": "test4",
            "password2": "test4",
            "birthDate": "2002-10-06",
            "autonomy": 102,
            "chargerTypes": [self.mennekes.pk],
            "preference": {
                "canNotTravelWithPets": True,
                "listenToMusic": True,
                "noSmoking": False,
                "talkTooMuch": True,
            },
            "iban": "ES6621009991",
        }
        response = self.client.patch(url, dataPatch, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.driver.pk)
        self.assertEqual(message.get("username"), "test4")
        self.assertEqual(message.get("first_name"), "newFirstName2")
        self.assertEqual(message.get("last_name"), "newLastName2")
        self.assertEqual(message.get("birthDate"), "2002-10-06")
        self.assertEqual(message.get("autonomy"), 102)
        self.assertEqual(message.get("chargerTypes"), [self.mennekes.pk])
        self.assertEqual(
            message.get("preference"),
            {
                "canNotTravelWithPets": True,
                "listenToMusic": True,
                "noSmoking": False,
                "talkTooMuch": True,
            },
        )
        self.assertEqual(message.get("iban"), "ES6621009991")

        # Partial PATCH
        dataPatch2 = {
            "iban": "FR6621009991",
        }
        response = self.client.patch(url, dataPatch2, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("id"), self.driver.pk)
        self.assertEqual(message.get("username"), self.driver.username)
        self.assertEqual(message.get("first_name"), self.driver.first_name)
        self.assertEqual(message.get("last_name"), self.driver.last_name)
        self.assertEqual(message.get("birthDate"), self.driver.birthDate)
        self.assertEqual(message.get("autonomy"), self.driver.autonomy)
        self.assertEqual(message.get("chargerTypes"), self.driver.chargerTypes)
        self.assertEqual(message.get("preference"), self.driver.preference)
        self.assertEqual(message.get("iban"), "FR6621009991")

    def testUnauthorizedUpdateDriver(self):
        """
        Ensure the API call returns an error if the user is not authenticated.
        """

        url = reverse("driverRetriever", kwargs={"id": self.driver.pk})
        data = {"iban": "ES000000000111"}
        responsePut = self.client.put(url, data)
        self.assertEqual(responsePut.status_code, status.HTTP_401_UNAUTHORIZED)
        message = json.loads(responsePut.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Authentication credentials were not provided.")

        responsePatch = self.client.put(url, data)
        self.assertEqual(responsePatch.status_code, status.HTTP_401_UNAUTHORIZED)
        message = json.loads(responsePatch.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Authentication credentials were not provided.")

    def testDriverNotExists(self):
        """
        Ensure the API call returns an error if the user does not exist.
        """

        url = reverse("driverRetriever", kwargs={"id": 1000})
        data = {"iban": "ES000000000111"}
        headers = {
            "Authorization": f"Token {self.token}",
        }
        responsePut = self.client.put(url, data, headers=headers)  # type: ignore
        self.assertEqual(responsePut.status_code, status.HTTP_404_NOT_FOUND)
        message = json.loads(responsePut.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Not found.")

        responsePatch = self.client.patch(url, data, headers=headers)  # type: ignore
        self.assertEqual(responsePatch.status_code, status.HTTP_404_NOT_FOUND)
        message = json.loads(responsePatch.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Not found.")

    def testUserCannotUpdateOtherUser(self):
        """
        Ensure the API call returns an error if the user tries to update another user.
        """

        user2 = Driver.objects.create(
            username="test2",
            birthDate="1998-10-06",
            password="test2",
            email="test2@gmail.com",
            dni="12345679",
            iban="ES662100991",
        )
        url = reverse("driverRetriever", kwargs={"id": user2.pk})
        data = {"iban": "ES000000000111"}
        headers = {"Authorization": f"Token {self.token}"}
        responsePut = self.client.put(url, data, headers=headers)  # type: ignore
        self.assertEqual(responsePut.status_code, status.HTTP_403_FORBIDDEN)
        message = json.loads(responsePut.content.decode("utf-8"))
        self.assertEqual(message.get("error"), "You can only update your own user account.")

        responsePatch = self.client.patch(url, data, headers=headers)  # type: ignore
        self.assertEqual(responsePatch.status_code, status.HTTP_403_FORBIDDEN)
        message = json.loads(responsePatch.content.decode("utf-8"))
        self.assertEqual(message.get("error"), "You can only update your own user account.")


class DeleteDriverTest(APITestCase):
    """
    Test Delete Driver
    """

    def testSuccessfulDeleteDriver(self):
        driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        token, _ = Token.objects.get_or_create(user=driver)

        url = reverse("driverRetriever", kwargs={"id": driver.pk})
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.delete(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testUnauthorizedDeleteUser(self):
        """
        Ensure the API call returns an error if the user is not authenticated.
        """
        driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )

        url = reverse("driverRetriever", kwargs={"id": driver.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Authentication credentials were not provided.")

    def testUserWhoDeleteNotExists(self):
        """
        Ensure the API call returns an error if the user does not exist.
        """
        driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        token, _ = Token.objects.get_or_create(user=driver)

        url = reverse("driverRetriever", kwargs={"id": 1000})
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.delete(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Invalid token.")

    def testUserDeletedNotExists(self):
        """
        Ensure the API call returns an error if the user does not exist.
        """
        driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        token, _ = Token.objects.get_or_create(user=driver)

        url = reverse("driverRetriever", kwargs={"id": 1000})
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.delete(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("detail"), "Not found.")

    def testUserCannotDeleteOtherUser(self):
        """
        Ensure the API call returns an error if the user tries to delete another user.
        """
        driver = Driver.objects.create(
            username="test",
            birthDate="1998-10-06",
            password="test",
            email="test@gmail.com",
            dni="12345678",
            iban="ES662100999",
        )
        token, _ = Token.objects.get_or_create(user=driver)
        driver2 = Driver.objects.create(
            username="test2",
            birthDate="1998-10-06",
            password="test2",
            email="test2@gmail.com",
            dni="12345678P",
            iban="FR662100999",
        )

        url = reverse("driverRetriever", kwargs={"id": driver2.pk})
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.delete(url, headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(message.get("error"), "You can only delete your own user account.")
