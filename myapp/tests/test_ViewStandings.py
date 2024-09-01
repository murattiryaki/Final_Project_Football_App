from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

class ViewStandingsTest(TestCase):

    @patch('myapp.views.requests.get')
    def test_view_standings(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': 1,
            'response': [
                {
                    'league': {
                        'standings': [
                            [{
                                'rank': 1,
                                'team': {'name': 'Mocked Team'},
                                'points': 55,
                                'goalsDiff': 30,
                            }]
                        ]
                    }
                }
            ]
        }

        response = self.client.get(reverse('standings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mocked Team')
