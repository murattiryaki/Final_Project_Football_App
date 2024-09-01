from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)




