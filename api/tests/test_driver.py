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
        mennekes = ChargerType.objects.create(chargerType="Mennekes")
        tesla = ChargerType.objects.create(chargerType="Tesla")
        schuko = ChargerType.objects.create(chargerType="Schuko")
        chademo = ChargerType.objects.create(chargerType="ChadeMO")
        css_combo2 = ChargerType.objects.create(chargerType="CSS Combo2")
        self.driver = Driver.objects.create(
            username="driver1",
            birthDate="1998-10-06",
            email="driver@gmail.com",
            password="driver",
            dni="12345678",
            preference=Preference.objects.create(),
            iban="ES662100999",
        )
        self.driver.chargerTypes.add(mennekes)
        self.driver.chargerTypes.add(tesla)
        self.driver.chargerTypes.add(schuko)
        self.driver.chargerTypes.add(chademo)
        self.driver.chargerTypes.add(css_combo2)
        self.token, _ = Token.objects.get_or_create(user=self.driver)

    def testSuccessfulCreateUser(self):
        """
        Ensure the API call creates a user in the database.
        """

        url = reverse("userListCreate")
        data = {
            "username": "test",
            "birthDate": "1998-10-06",
            "password": "test",
            "password2": "test",
            "email": "test@gmail.com",
            "chargerTypes": [1],
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
                "noSmoking": True,
                "talkTooMuch": True,
            },
        )
        self.assertEqual(message.get("iban"), "ES662100999")

    def testDriverExists(self):
        """
        Ensure the API call returns an error if the driver already exists.
        """

        url = reverse("userListCreate")
        data = {
            "username": "driver1",
            "birthDate": "1998-10-06",
            "password": "driver",
            "password2": "driver",
            "email": "driver@gmail.com",
            "dni": "12345678",
            "chargerTypes": [1],
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
