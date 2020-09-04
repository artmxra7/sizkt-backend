from django.contrib import admin

from .models import (
    Mustahik,
    DataSource,
    DataSourceWarga,
    DataSourceInstitusi,
    DataSourcePekerja,
)

admin.site.register([
    Mustahik,
    DataSource,
    DataSourceWarga,
    DataSourceInstitusi,
    DataSourcePekerja,
])
