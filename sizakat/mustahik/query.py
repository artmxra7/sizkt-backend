import graphene
from django.db.models import Q

from .models import Mustahik
from .types import MustahikType

class MustahikQuery(graphene.ObjectType):
    mustahiks = graphene.List(MustahikType, statuses=graphene.List(graphene.String))

    def resolve_mustahiks(self, info, statuses=[], **kwargs):
        if statuses and len(statuses) > 0:
            filter = Q(status=statuses[0])
            for status in statuses:
                filter = filter | Q(status=status)
            return Mustahik.objects.filter(filter)

        return Mustahik.objects.all()

