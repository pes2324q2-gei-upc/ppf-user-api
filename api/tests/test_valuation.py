"""
This module contains the tests for the valuation.
"""

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from common.models.valuation import Valuation
from common.models.user import User, Driver, ChargerType, Preference
from common.models.route import Route

import json

from rest_framework.authtoken.models import Token


class CreateValuationTest(APITestCase):
    """
    Test module for creating a valuation.
    """

    def setUp(self):
        self.user = User.objects.create(
            username="test", birthDate="1998-10-06", password="test", email="test@gmail.com"
        )
        self.tokenUser = Token.objects.create(user=self.user)
        self.mennekes = ChargerType.objects.create(chargerType="Mennekes")
        self.driver = Driver.objects.create(
            username="driver1",
            birthDate="1998-10-06",
            email="driver@gmail.com",
            password="driver",
            dni="12345678",
            preference=Preference.objects.create(),
            iban="ES662100999",
        )
        self.driver.chargerTypes.add(self.mennekes)
        self.tokenDriver = Token.objects.create(user=self.driver)
        self.route = Route.objects.create(
            originLat=41.350450,
            originLon=2.132660,
            originAlias="SomeWhere",
            destinationLat=41.419860,
            destinationLon=2.2009346,
            destinationAlias="AnotherPlace",
            distance=100,
            duration=20,
            departureTime="2024-05-19T18:21:56.083Z",
            freeSeats=5,
            price=20.0,
        )

    def testSuccesfullCreateValuation(self):
        """
        Test to create a valuation with valid data.
        """

        url = reverse("valuationListCreate")
        data = {
            "receiver": self.driver.pk,
            "route": self.route.pk,
            "rating": 5,
            "comment": "Valuando driver",
        }
        headers = {
            "Authorization": f"Token {self.tokenUser}",
        }
        response = self.client.post(url, data, format="json", headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = json.loads(response.content.decode("utf-8"))
        valuation = Valuation.objects.get(pk=message.get("id"))
        self.assertEqual(message.get("receiver"), valuation.receiver.pk)
        self.assertEqual(message.get("route"), valuation.route.pk)
        self.assertEqual(message.get("rating"), valuation.rating)
        self.assertEqual(message.get("comment"), valuation.comment)

        url = reverse("valuationListCreate")
        data = {
            "receiver": self.user.pk,
            "route": self.route.pk,
            "rating": 5,
            "comment": "Valuando user",
        }
        headers = {
            "Authorization": f"Token {self.tokenDriver}",
        }
        response = self.client.post(url, data, format="json", headers=headers)  # type: ignore
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = json.loads(response.content.decode("utf-8"))
        valuation = Valuation.objects.get(pk=message.get("id"))
        self.assertEqual(message.get("receiver"), valuation.receiver.pk)
        self.assertEqual(message.get("route"), valuation.route.pk)
        self.assertEqual(message.get("rating"), valuation.rating)
        self.assertEqual(message.get("comment"), valuation.comment)
