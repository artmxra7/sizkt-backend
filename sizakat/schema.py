import graphene

from graphene_django import DjangoObjectType

from .mustahik.mutations import MustahikMutation
from .mustahik.query import MustahikQuery

ABOUT = 'Si Zakat merupakan sistem informasi untuk membantu masjid dalam \
mengelola transaksi zakat. Sistem ini dibuat oleh tim lab 1231, \
yang dipimpin oleh Prof. Dr. Wisnu Jatmiko.'


class Query(MustahikQuery, graphene.ObjectType):
    about = graphene.String()

    def resolve_about(self, info):
        return ABOUT


class Mutation(graphene.ObjectType):
    mustahik_mutation = MustahikMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
