from django import forms

from .models import Mustahik, DataSource, DataSourceWarga, DataSourceInstitusi, DataSourcePekerja


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
            'photo',
        ]


class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = [
            'category',
        ]


class DataSourceWargaForm(forms.ModelForm):
    class Meta:
        model = DataSourceWarga
        fields = [
            'pic_name',
            'pic_ktp',
            'pic_phone',
            'pic_position',
            'province',
            'regency',
            'sub_district',
            'village',
            'rt',
            'rw',
            'data_source',
        ]


class DataSourceInstitusiForm(forms.ModelForm):
    class Meta:
        model = DataSourceInstitusi
        fields = [
            'pic_name',
            'pic_ktp',
            'pic_phone',
            'pic_position',
            'name',
            'province',
            'sub_district',
            'village',
            'rt',
            'rw',
            'address',
            'data_source',
        ]


class DataSourcePekerjaForm(forms.ModelForm):
    class Meta:
        model = DataSourcePekerja
        fields = [
            'pic_name',
            'pic_ktp',
            'pic_phone',
            'pic_position',
            'profession',
            'location',
            'data_source',
        ]
