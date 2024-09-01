from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

class ViewFixturesTest(TestCase):

    @patch('myapp.views.requests.get')
    def test_view_fixtures(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': 1,
            'response': [
                {
                    'fixture': {
                        'id': 1,
                        'date': '2024-09-01T14:00:00Z',
                    },
                    'league': {'round': 'Regular Season - 1'},
                    'teams': {
                        'home': {'name': 'Team A'},
                        'away': {'name': 'Team B'},
                    },
                    'goals': {'home': 2, 'away': 1}
                }
            ]
        }

        response = self.client.get(reverse('fixtures'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team A')
