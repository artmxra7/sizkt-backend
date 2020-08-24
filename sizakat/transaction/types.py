import graphene

from graphene_django.types import DjangoObjectType

from .models import (
    Muzakki, Transaction, ZakatTransaction, ZakatType as ZakatTypeModel
)


class MuzakkiType(DjangoObjectType):
    class Meta:
        model = Muzakki


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction


class ZakatTransactionType(DjangoObjectType):
    class Meta:
        model = ZakatTransaction


class ZakatType(DjangoObjectType):
    class Meta:
        model = ZakatTypeModel
        exclude = ('zakattransaction_set', )
