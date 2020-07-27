import json

from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core import mail

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
        logged_in = json.loads(response.content).get('loggedIn', None)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(logged_in)

    def test_user_get_fail_message_when_login_failed(self):
        c = Client()
        response = c.post(
            '/login/',
            json.dumps({'username': 'thisuser', 'password': 'willfailed'}),
            'text/json')
        logged_in = json.loads(response.content).get('loggedIn', None)
        self.assertFalse(logged_in)

    def test_user_can_logout_via_post_logout(self):
        c = Client()
        log_in = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': '12345'}),
            'text/json')
        response = c.post('/logout/')
        logged_out = json.loads(response.content).get('loggedOut', None)
        self.assertTrue(logged_out)

    def test_user_can_reset_password_and_change_with_valid_token(self):
        c = Client()
        response = c.post(
            '/reset-password/',
            json.dumps({
                'email': 'test@mail.com',
                'changePasswordUrl': 'localhost/reset-password'}),
            'text/json'
        )
        success = json.loads(response.content).get('success', None)
        self.assertTrue(success)

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
        self.assertTrue(json.loads(
            change_reset_password.content).get('success'))

        login_response = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': new_pass}),
            'text/json')
        self.assertTrue(json.loads(login_response.content).get('loggedIn'))

    def test_session_is_valid_after_logged_in(self):
        c = Client()
        response = c.post(
            '/login/',
            json.dumps({'username': 'testuser', 'password': '12345'}),
            'text/json')
        logged_in = json.loads(response.content).get('loggedIn', None)

        self.assertTrue(logged_in)

        session = json.loads(response.content).get('session', None)
        auth_headers = {
            'HTTP_AUTHORIZATION': session,
        }
        verify_response = c.get('/verify-session/', **auth_headers)
        self.assertTrue(json.loads(
            verify_response.content).get('active', None))
