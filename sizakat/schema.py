import graphene

from graphene_django import DjangoObjectType

from .mustahik.mutations import (
    MustahikMutation, DeleteMustahik, DataSourceMutation,
    DataSourceWargaMutation, DataSourceInstitusiMutation,
    DataSourcePekerjaMutation
)
from .mustahik.query import MustahikQuery

ABOUT = ('Si Zakat merupakan sistem informasi untuk membantu masjid dalam '
         'mengelola transaksi zakat. Sistem ini dibuat oleh tim lab 1231, '
         'yang dipimpin oleh Prof. Dr. Wisnu Jatmiko.')


class Query(MustahikQuery, graphene.ObjectType):
    about = graphene.String()

    def resolve_about(self, info):
        return ABOUT


class Mutation(graphene.ObjectType):
    mustahik_mutation = MustahikMutation.Field()
    delete_mustahik = DeleteMustahik.Field()
    dataSource_mutation = DataSourceMutation.Field()
    dataSourceWarga_mutation = DataSourceWargaMutation.Field()
    dataSourceInstitusi_mutation = DataSourceInstitusiMutation.Field()
    dataSourcePekerja_mutation = DataSourcePekerjaMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
