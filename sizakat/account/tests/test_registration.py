import json
import re

from django.contrib.auth import get_user_model
from django.core import mail
from graphene_django.utils.testing import GraphQLTestCase

from sizakat.schema import schema

User = get_user_model()


class UserRegistrationTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_register_with_verification(self):
        register_resp = self.query(
            '''
            mutation {
              register(
                username: "testuser"
                email: "test@mail.com"
                password1: "supersecretpassword"
                password2: "supersecretpassword"
              ) {
                success
              }
            }
            '''
        )

        self.assertTrue(json.loads(register_resp.content)['data']['register']['success'])

        user = User.objects.get(username='testuser', email='test@mail.com')
        self.assertFalse(user.status.verified)

        token_regex = '[A-z0-9-_]+:[A-z0-9-_]+:[A-z0-9-_]+'
        token = re.search(token_regex, mail.outbox[0].body).group()

        verify_resp = self.query(
            '''
            mutation {{
              verifyAccount(token: "{}") {{
                success
                errors
              }}
            }}
            '''.format(token)
        )

        self.assertTrue(json.loads(verify_resp.content)['data']['verifyAccount']['success'])

        user.status.refresh_from_db()
        self.assertTrue(user.status.verified)
