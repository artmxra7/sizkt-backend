import graphene

from django import forms
from graphene_django.forms.mutation import DjangoModelFormMutation

from .models import Mustahik
from .types import MustahikType


class MustahikForm(forms.ModelForm):

    class Meta:
        model = Mustahik
        fields = [
            'name',
            'no_ktp',
            'phone',
            'address',
            'province',
            'regency',
            'rt',
            'rw',
            'birthdate',
            'status',
            'family_size',
            'description',
        ]


class MustahikMutation(DjangoModelFormMutation):

    mustahik = graphene.Field(MustahikType)

    class Meta:
        form_class = MustahikForm

class DeleteMustahik(graphene.Mutation): 
    class Arguments:
        id = graphene.ID()
    
    message = graphene.String()
    idMustahik = graphene.ID()
    nama = graphene.String()
    noKtp = graphene.String()
    mustahik = graphene.Field(MustahikType)

    def mutate(self, info, id):
        mustahik = Mustahik.objects.get(pk=id)
        _nama = mustahik.name
        _no_ktp = mustahik.no_ktp
        mustahik.delete()
        return DeleteMustahik(message = "Success", idMustahik=id, nama=_nama, noKtp=_no_ktp)


