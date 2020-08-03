import graphene

from django.db.models import Q
from functools import reduce

from .models import Mustahik, DataSource
from .types import MustahikType, DataSourceType


class MustahikQuery(graphene.ObjectType):
    mustahiks = graphene.List(
        MustahikType,
        statuses=graphene.List(graphene.String),
        name_contains=graphene.String()
    )
    mustahik = graphene.Field(MustahikType, id=graphene.ID(required=True))
    data_sources = graphene.List(DataSourceType, category=graphene.String())
    data_source = graphene.Field(DataSourceType, id=graphene.ID(required=True))

    def resolve_mustahiks(self, info, **kwargs):
        statuses = kwargs.get('statuses', None)
        name_contains = kwargs.get('name_contains', None)
        filter_query = Q()

        if statuses and len(statuses) > 0:
            filter_query |= reduce(
                lambda a, b: a | b,
                [Q(status=status) for status in statuses]
            )

        if name_contains:
            filter_query &= Q(name__icontains=name_contains)

        return Mustahik.objects.filter(filter_query)

    def resolve_mustahik(self, info, id):
        return Mustahik.objects.get(pk=id)

    def resolve_data_sources(self, info, **kwargs):
        category = kwargs.get('category')
        filter_query = Q()
        if category:
            filter_query &= Q(category=category)

        return DataSource.objects.filter(filter_query)

    def resolve_data_source(self, info, id):
        return DataSource.objects.get(pk=id)
