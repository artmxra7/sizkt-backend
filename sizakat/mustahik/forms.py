from django import forms

from .models import Mustahik


class MustahikForm(forms.ModelForm):
    class Meta:
        model = Mustahik
        fields = [
            'name',
            'no_ktp',
            'phone',
            'address',
            'birthdate',
            'status',
            'gender',
            'data_source',
        ]
