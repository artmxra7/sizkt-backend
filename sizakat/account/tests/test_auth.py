import json
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from freezegun import freeze_time
from graphene_django.utils.testing import GraphQLTestCase
from graphql_auth.constants import Messages

from sizakat.schema import schema

User = get_user_model()


class UserAuthenticationTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            'testuser',
            'test@mail.com',
            'supersecretpassword',
        )

    def test_login_with_username(self):
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

        me_resp = self.query(
            '''
            {
              me {
                username
                email
              }
            }
            ''',
            headers={'HTTP_AUTHORIZATION': 'JWT {}'.format(token)},
        )

        me = json.loads(me_resp.content)['data']['me']
        self.assertEqual(me['username'], 'testuser')
        self.assertEqual(me['email'], 'test@mail.com')

    def test_login_with_email(self):
        token_resp = self.query(
            '''
            mutation {
              tokenAuth(
                email: "test@mail.com"
                password: "supersecretpassword"
              ) {
                token
              }
            }
            '''
        )

        token = json.loads(token_resp.content)['data']['tokenAuth']['token']

        me_resp = self.query(
            '''
            {
              me {
                username
                email
              }
            }
            ''',
            headers={'HTTP_AUTHORIZATION': 'JWT {}'.format(token)},
        )

        me = json.loads(me_resp.content)['data']['me']
        self.assertEqual(me['username'], 'testuser')
        self.assertEqual(me['email'], 'test@mail.com')

    def test_refresh_token(self):
        token_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "supersecretpassword"
              ) {
                token
                refreshToken
              }
            }
            '''
        )

        token_auth = json.loads(token_resp.content)['data']['tokenAuth']
        token = token_auth['token']
        refresh_token = token_auth['refreshToken']

        with freeze_time(datetime.now() + timedelta(minutes=5, seconds=1), tick=True):
            me_resp = self.query(
                '''
                {
                  me {
                    username
                  }
                }
                ''',
                headers={'HTTP_AUTHORIZATION': 'JWT {}'.format(token)},
            )

            self.assertIsNone(json.loads(me_resp.content)['data']['me'])

            new_token_resp = self.query(
                '''
                mutation {{
                  refreshToken(refreshToken: "{}") {{
                    token
                  }}
                }}
                '''.format(refresh_token)
            )

            new_token = json.loads(new_token_resp.content)['data']['refreshToken']['token']

            new_me_resp = self.query(
                '''
                {
                  me {
                    username
                  }
                }
                ''',
                headers={'HTTP_AUTHORIZATION': 'JWT {}'.format(new_token)},
            )

            self.assertEqual(json.loads(new_me_resp.content)['data']['me']['username'], 'testuser')

    def test_revoke_refresh_token(self):
        token_resp = self.query(
            '''
            mutation {
              tokenAuth(
                username: "testuser"
                password: "supersecretpassword"
              ) {
                refreshToken
              }
            }
            '''
        )

        refresh_token = json.loads(token_resp.content)['data']['tokenAuth']['refreshToken']

        revoke_resp = self.query(
            '''
            mutation {{
              revokeToken(refreshToken: "{}") {{
                success
              }}
            }}
            '''.format(refresh_token)
        )

        self.assertTrue(json.loads(revoke_resp.content)['data']['revokeToken']['success'])

        refresh_resp = self.query(
            '''
            mutation {{
              refreshToken(refreshToken: "{}") {{
                errors
              }}
            }}
            '''.format(refresh_token)
        )

        errors = json.loads(refresh_resp.content)['data']['refreshToken']['errors']
        self.assertEqual(errors['nonFieldErrors'], Messages.INVALID_TOKEN)
