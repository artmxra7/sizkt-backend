import graphene

from graphene_django.types import DjangoObjectType
from .models import Mustahik


class MustahikType(DjangoObjectType):

    class Meta:
        model = Mustahik
