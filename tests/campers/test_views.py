import json
from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

SEARCHES_PATH = "./tests/campers/data/searches.json"
SEARCH_EXPECTED_CAMPERS_PATH = "./tests/campers/data/search_expected_campers.json"


def load_search_results():
    expected_search_results = open(SEARCH_EXPECTED_CAMPERS_PATH, "rb")
    search_results = json.load(expected_search_results, object_pairs_hook=OrderedDict)
    expected_search_results.close()
    return search_results


def load_search_requests():
    search_file = open(SEARCHES_PATH, "rb")
    searches = json.load(search_file)["searches"]
    search_file.close()
    return searches


class TestCampersViews(TestCase):
    fixtures = ["campers.json"]

    def test_search_with_results(self):
        url = reverse("camper-search")
        search_requests = load_search_requests()
        search_results = load_search_results()
        for search_request in search_requests:
            search_id = str(search_request["id"])
            response = self.client.get(url, data=search_request, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_campers = response.data
            expected_campers = search_results[search_id]
            self.assertListEqual(response_campers, expected_campers)

    def test_search_no_result(self):
        url = reverse("camper-search")

        response = self.client.get(
            url, data={"latitude": 25.0000188, "longitude": -71.0087548}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
