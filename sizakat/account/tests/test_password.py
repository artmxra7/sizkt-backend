import json
import re

from django.contrib.auth import get_user_model
from django.core import mail
from graphene_django.utils.testing import GraphQLTestCase
from graphql_auth.constants import Messages

from sizakat.schema import schema

User = get_user_model()


class UserPasswordTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'testuser',
            'test@mail.com',
            'supersecretpassword',
        )
        cls.user.status.verified = True
        cls.user.status.save()

    def test_password_change(self):
        token_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "supersecretpassword"
              ) {
                token
              }
            }
            '''
        )

        token = json.loads(token_resp.content)['data']['tokenAuth']['token']

        pwchange_resp = self.query(
            '''
            mutation {
              passwordChange(
                oldPassword: "supersecretpassword"
                newPassword1: "abrandnewpassword"
                newPassword2: "abrandnewpassword"
              ) {
                success
              }
            }
            ''',
            headers={'HTTP_AUTHORIZATION': 'JWT {}'.format(token)},
        )

        self.assertTrue(json.loads(pwchange_resp.content)['data']['passwordChange']['success'])

        old_auth_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "supersecretpassword"
              ) {
                errors
              }
            }
            '''
        )

        errors = json.loads(old_auth_resp.content)['data']['tokenAuth']['errors']
        self.assertEqual(errors['nonFieldErrors'], Messages.INVALID_CREDENTIALS)

        new_auth_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "abrandnewpassword"
              ) {
                success
              }
            }
            '''
        )

        self.assertTrue(json.loads(new_auth_resp.content)['data']['tokenAuth']['success'])

    def test_reset_password(self):
        sendreset_resp = self.query(
            '''
            mutation {
              sendPasswordResetEmail(email: "test@mail.com") {
                success
              }
            }
            '''
        )

        self.assertTrue(json.loads(sendreset_resp.content)['data']['sendPasswordResetEmail']['success'])

        token_regex = '[A-z0-9-_]+:[A-z0-9-_]+:[A-z0-9-_]+'
        token = re.search(token_regex, mail.outbox[0].body).group()

        pwreset_resp = self.query(
            '''
            mutation {{
              passwordReset(
                token: "{}"
                newPassword1: "abrandnewpassword"
                newPassword2: "abrandnewpassword"
              ) {{
                success
              }}
            }}
            '''.format(token)
        )

        self.assertTrue(json.loads(pwreset_resp.content)['data']['passwordReset']['success'])

        old_auth_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "supersecretpassword"
              ) {
                errors
              }
            }
            '''
        )

        errors = json.loads(old_auth_resp.content)['data']['tokenAuth']['errors']
        self.assertEqual(errors['nonFieldErrors'], Messages.INVALID_CREDENTIALS)

        new_auth_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "abrandnewpassword"
              ) {
                success
              }
            }
            '''
        )

        self.assertTrue(json.loads(new_auth_resp.content)['data']['tokenAuth']['success'])
