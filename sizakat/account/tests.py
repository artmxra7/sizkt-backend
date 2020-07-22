import json

from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from .views import post_login

User = get_user_model()


class AccountTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

    def test_user_can_login_via_post_login(self):
        c = Client()
        response = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': '12345'}),
            'text/json')
        message = json.loads(response.content).get('message', '')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message, 'login succeeded')

    def test_user_get_fail_message_when_login_failed(self):
        c = Client()
        response = c.post(
            '/login/',
            json.dumps({'username': 'thisuser', 'password': 'willfailed'}),
            'text/json')
        message = json.loads(response.content).get('message', '')
        self.assertEqual(message, 'login failed')
