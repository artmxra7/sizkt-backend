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
            'province',
            'regency',
            'rt',
            'rw',
            'birthdate',
            'status',
            'family_size',
            'description',
        ]
