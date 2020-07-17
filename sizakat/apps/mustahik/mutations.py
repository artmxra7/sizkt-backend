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
