from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from campers.views import SEARCH_COORDINATES_PADDING


class TestCampersViews(TestCase):
    fixtures = ['campers.json']

    def test_search_with_results(self):
        url = reverse('camper-search')

        search_latitude = 44.8637834
        search_longitude = -0.6211603
        response = self.client.get(
            url, data={"latitude": search_latitude, "longitude": search_longitude}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_campers = response.data
        self.assertEqual(len(response_campers), 2)
        for camper in response_campers:
            self.assertTrue(
                (
                    search_latitude - SEARCH_COORDINATES_PADDING < camper.get('latitude')
                    < search_latitude + SEARCH_COORDINATES_PADDING
                ) and
                (
                    search_longitude - SEARCH_COORDINATES_PADDING < camper.get('longitude')
                    < search_longitude + SEARCH_COORDINATES_PADDING
                )
            )

    def test_search_no_result(self):
        url = reverse('camper-search')

        response = self.client.get(
            url, data={"latitude": 25.0000188, "longitude": -71.0087548}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
