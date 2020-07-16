from datetime import date
from django.test import TestCase

from .models import Mustahik


class MustahikModelTestCase(TestCase):
    def setUp(self):
        Mustahik.objects.create(
            name='mustahik',
            no_ktp='31751234567890',
            phone='081234567890',
            address='Jalan raya depok',
            province='Jawa Barat',
            regency='Depok',
            rt='003',
            rw='002',
            birthdate=date(1987, 6, 5),
            status=Mustahik.Status.MISKIN,
            family_size=4,
            description='desc'
        )

    def test_mustahik_creation(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        self.assertTrue(isinstance(mustahik, Mustahik))
