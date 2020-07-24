import json

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from .views import post_login

User = get_user_model()


class AccountTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser', email='test@mail.com')
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

    def test_user_can_logout_via_post_logout(self):
        c = Client()
        log_in = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': '12345'}),
            'text/json')
        response = c.post('/logout/')
        message = json.loads(response.content).get('message', '')
        self.assertEqual(message, 'logout succeeded')

    def test_user_can_reset_password_and_change_with_valid_token(self):
        c = Client()
        response = c.post(
            '/reset-password/',
            json.dumps({
                'email': 'test@mail.com',
                'changePasswordUrl': 'localhost/reset-password'}),
            'text/json'
        )
        message = json.loads(response.content).get('message', '')
        self.assertEqual(message, 'reset token has been sent to your email')

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Reset password akun sizakat')

        email_msg = str(mail.outbox[0].message())
        user_id = int(email_msg.split('userId=')[1].split('&')[0])
        token = email_msg.split('token=')[1].split('&')[0]

        new_pass = '54321'
        change_reset_password = c.post(
            '/change-reset-password/',
            json.dumps({'userId': user_id, 'token': token,
                        'newPassword': new_pass}),
            'text/json'
        )
        self.assertEqual(
            json.loads(change_reset_password.content).get('message'),
            'password successfully changed')

        login_response = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': new_pass}),
            'text/json')
        self.assertEqual(json.loads(login_response.content).get(
            'message'), 'login succeeded')
