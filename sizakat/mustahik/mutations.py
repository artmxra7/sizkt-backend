import graphene

from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_django.types import ErrorType
from sizakat.validators import validate_photo

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

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        form = cls.get_form(root, info, **input)
        photo = info.context.FILES['photo']
        if not validate_photo(photo):
            form.add_error('photo', 'invalid photo format')

        if form.is_valid():
            mustahik = form.save(commit=False)
            mustahik.photo = photo
            mustahik.save()
            kwargs = {cls._meta.return_field_name: mustahik}
            return cls(errors=[], **kwargs)
        else:
            errors = ErrorType.from_errors(form.errors)
            return cls(errors=errors)


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
