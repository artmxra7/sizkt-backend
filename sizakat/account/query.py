import graphene
from graphql_auth.schema import UserQuery, MeQuery

class AccountQuery(UserQuery, MeQuery, graphene.ObjectType):
    pass
