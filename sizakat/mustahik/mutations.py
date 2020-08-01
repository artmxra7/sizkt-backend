import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import (
    MustahikForm, DataSourceForm, DataSourceWargaForm,
    DataSourceInstitusiForm, DataSourcePekerjaForm
)
from .models import Mustahik, DataSource
from .types import (
    MustahikType, DataSourceInstitusiType,
    DataSourcePekerjaType, DataSourceWargaType, DataSourceType
)


class MustahikMutation(DjangoModelFormMutation):
    mustahik = graphene.Field(MustahikType)

    class Meta:
        form_class = MustahikForm


class DeleteMustahik(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, id):
        Mustahik.objects.get(pk=id).delete()
        return DeleteMustahik(deleted=True)


class DataSourceMutation(DjangoModelFormMutation):
    dataSource = graphene.Field(DataSourceType)

    class Meta:
        form_class = DataSourceForm


class DeleteDataSource(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    deleted = graphene.Boolean()

    def mutate(self, info, id):
        DataSource.objects.get(pk=id).delete()
        return DeleteDataSource(deleted=True)


class DataSourceWargaMutation(DjangoModelFormMutation):
    dataSourceWarga = graphene.Field(DataSourceWargaType)

    class Meta:
        form_class = DataSourceWargaForm


class DataSourceInstitusiMutation(DjangoModelFormMutation):
    dataSourceInstitusi = graphene.Field(DataSourceInstitusiType)

    class Meta:
        form_class = DataSourceInstitusiForm


class DataSourcePekerjaMutation(DjangoModelFormMutation):
    dataSourcePekerja = graphene.Field(DataSourcePekerjaType)

    class Meta:
        form_class = DataSourcePekerjaForm
