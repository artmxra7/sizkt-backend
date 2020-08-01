import graphene

from graphene_django.types import DjangoObjectType
from .models import (
    Mustahik, DataSource, DataSourceInstitusi,
    DataSourcePekerja, DataSourceWarga
)


class MustahikType(DjangoObjectType):
    class Meta:
        model = Mustahik

    age = graphene.Int(source='calculate_age')


class DataSourceInstitusiType(DjangoObjectType):
    class Meta:
        model = DataSourceInstitusi


class DataSourcePekerjaType(DjangoObjectType):
    class Meta:
        model = DataSourcePekerja


class DataSourceWargaType(DjangoObjectType):
    class Meta:
        model = DataSourceWarga


class DataSourceDetailType(graphene.Union):
    class Meta:
        types = (
            DataSourceInstitusiType, DataSourcePekerjaType,
            DataSourceWargaType
        )
        my_attr = True


class DataSourceType(DjangoObjectType):
    class Meta:
        model = DataSource
        exclude = (
            'datasourceinstitusi', 'datasourcepekerja', 'datasourcewarga'
        )

    data_source_detail = graphene.Field(
        DataSourceDetailType, source='get_source_detail'
    )
