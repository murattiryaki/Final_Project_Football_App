from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.teams_url = reverse('teams')

    def test_teams_GET(self):
        response = self.client.get(self.teams_url)

        self.assertEqual(response.status_code, 200)