import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation

from .forms import MustahikForm, DataSourceForm, DataSourceWargaForm, DataSourceInstitusiForm, DataSourcePekerjaForm
from .models import Mustahik
from .types import MustahikType, DataSourceInstitusiType,  DataSourcePekerjaType, DataSourceWargaType, DataSourceType


class MustahikMutation(DjangoModelFormMutation):
    mustahik = graphene.Field(MustahikType)

    class Meta:
        form_class = MustahikForm


class DeleteMustahik(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    deleted = graphene.Boolean()
    id_mustahik = graphene.ID()
    name = graphene.String()
    no_ktp = graphene.String()

    def mutate(self, info, id):
        mustahik = Mustahik.objects.get(pk=id)
        name = mustahik.name
        no_ktp = mustahik.no_ktp
        mustahik.delete()
        deleted = True
        return DeleteMustahik(deleted=deleted, id_mustahik=id, name=name, no_ktp=no_ktp)

class DataSourceMutation(DjangoModelFormMutation):
    dataSource = graphene.Field(DataSourceType)

    class Meta:
        form_class = DataSourceForm

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
