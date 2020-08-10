import graphene

from graphene_django import DjangoObjectType

from .mustahik.mutations import (
    MustahikMutation, DeleteMustahik, DataSourceMutation,
    DataSourceWargaMutation, DataSourceInstitusiMutation,
    DataSourcePekerjaMutation, DeleteDataSource
)
from .mustahik.query import MustahikQuery
from .transaction.query import TransactionQuery
from .transaction.mutations import (
    MuzakkiMutation, TransactionMutation, ZakatTransactionMutation
)

ABOUT = ('Si Zakat merupakan sistem informasi untuk membantu masjid dalam '
         'mengelola transaksi zakat. Sistem ini dibuat oleh tim lab 1231, '
         'yang dipimpin oleh Prof. Dr. Wisnu Jatmiko.')


class Query(MustahikQuery, TransactionQuery, graphene.ObjectType):
    about = graphene.String()

    def resolve_about(self, info):
        return ABOUT


class Mutation(graphene.ObjectType):
    mustahik_mutation = MustahikMutation.Field()
    delete_mustahik = DeleteMustahik.Field()
    data_source_mutation = DataSourceMutation.Field()
    data_source_warga_mutation = DataSourceWargaMutation.Field()
    data_source_institusi_mutation = DataSourceInstitusiMutation.Field()
    data_source_pekerja_mutation = DataSourcePekerjaMutation.Field()
    delete_data_source = DeleteDataSource.Field()

    muzakki_mutation = MuzakkiMutation.Field()
    transaction_mutation = TransactionMutation.Field()
    zakat_transaction_mutation = ZakatTransactionMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
