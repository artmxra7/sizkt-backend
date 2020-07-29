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

    data_source_detail = graphene.Field(DataSourceDetailType)

    def resolve_data_source_detail(self, info):
        if self.category == DataSource.Category.INSTITUSI:
            return DataSourceInstitusi.objects.get(data_source__pk=self.pk)
        if self.category == DataSource.Category.PEKERJA:
            return DataSourcePekerja.objects.get(data_source__pk=self.pk)
        if self.category == DataSource.Category.WARGA:
            return DataSourceWarga.objects.get(data_source__pk=self.pk)
