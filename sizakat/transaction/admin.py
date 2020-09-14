from django.contrib import admin

from .models import *

admin.site.register([
    ZakatType,
    Transaction,
    ZakatTransaction,
    Muzakki
])
