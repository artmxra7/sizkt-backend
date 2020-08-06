import graphene

from .models import Transaction, ZakatType as ZakatTypeModel
from .types import TransactionType, ZakatType


class TransactionQuery(graphene.ObjectType):
    transactions = graphene.List(TransactionType)
    transaction = graphene.Field(
        TransactionType, transaction_id=graphene.ID(required=True)
    )
    zakat_types = graphene.List(ZakatType)

    def resolve_transactions(self, info, **kwargs):
        return Transaction.objects.all()

    def resolve_transaction(self, info, transaction_id):
        return Transaction.objects.get(pk=transaction_id)

    def resolve_zakat_types(self, info, **kwargs):
        return ZakatTypeModel.objects.all()
