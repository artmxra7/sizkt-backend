from datetime import date
from django.db.utils import IntegrityError
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

    def test_no_ktp_mustahik_is_unique(self):
        with self.assertRaises(IntegrityError):
            Mustahik.objects.create(
                name='kihatsum',
                no_ktp='31751234567890',
                phone='08987654321',
                address='Jalan raya bogor',
                province='Jawa Barat',
                regency='Bogor',
                rt='002',
                rw='003',
                birthdate=date(1987, 4, 3),
                status=Mustahik.Status.MISKIN,
                family_size=1,
                description='no_ktp is unique'
            )
