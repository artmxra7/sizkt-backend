import graphene

from django.db.models import Q
from functools import reduce

from .models import Mustahik
from .types import MustahikType


class MustahikQuery(graphene.ObjectType):
    mustahiks = graphene.List(
        MustahikType,
        statuses=graphene.List(graphene.String),
        name_contains=graphene.String()
    )
    mustahik = graphene.Field(MustahikType, id=graphene.ID(required=True))

    def resolve_mustahiks(self, info, **kwargs):
        statuses = kwargs.get('statuses', None)
        name_contains = kwargs.get('name_contains', None)
        mustahiks = Mustahik.objects.all()

        if statuses and len(statuses) > 0:
            mustahiks = mustahiks.filter(reduce(
                lambda a, b: a | b,
                list(map(lambda s: Q(status=s), statuses))
            ))

        if name_contains:
            mustahiks = mustahiks.filter(name__icontains=name_contains)

        return mustahiks

    def resolve_mustahik(self, info, id):
        return Mustahik.objects.get(pk=id)
