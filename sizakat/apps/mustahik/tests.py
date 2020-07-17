import json

from datetime import date
from django.db.utils import IntegrityError
from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from sizakat.schema import schema

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


class MustahikGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

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

    def test_mustahik_mutation_can_add_new_mustahik(self):
        no_ktp = '123891210121'
        response = self.query(
            '''
            mutation mustahikMutation($input: MustahikMutationInput!) {
                mustahikMutation(input: $input) {
                    mustahik {
                        id
                        name
                        noKtp
                        status
                        description
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
            ''',
            op_name='mustahikMutation',
            input_data={
                "name": "jumat",
                "noKtp": no_ktp,
                "phone": "02132132180",
                "address": "jalan swadaya",
                "province": "jakarta",
                "regency": "manggarai",
                "rt": "001",
                "rw": "001",
                "birthdate": "1998-03-12",
                "status": "YATIM",
                "familySize": 3,
                "description": "anak yatim"
            }
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['mustahikMutation']
                         ['mustahik']['status'], 'YATIM')

        # Validate success save to db
        self.assertNotEqual(Mustahik.objects.count(), 0)
        mustahik = Mustahik.objects.get(no_ktp=no_ktp)
        self.assertEqual(mustahik.name, 'jumat')

    def test_mustahik_mutation_can_update_mustahik(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        mustahik_id = mustahik.pk
        old_desc = mustahik.description
        new_desc = 'keluarga tidak mampu'
        response = self.query(
            '''
            mutation mustahikMutation($input: MustahikMutationInput!) {
                mustahikMutation(input: $input) {
                    mustahik {
                        id
                        description
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
            ''',
            op_name='mustahikMutation',
            input_data={
                "name": "mustahik",
                "noKtp": "31751234567890",
                "phone": "081234567890",
                "address": "Jalan raya depok",
                "province": "Jawa Barat",
                "regency": "Depok",
                "rt": "003",
                "rw": "002",
                "birthdate": "1987-06-05",
                "status": "MISKIN",
                "familySize": 4,
                "description": new_desc,
                "id": mustahik.pk
            }
        )

        # Validate success update desc mustahik
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        self.assertNotEqual(mustahik.description, old_desc)
        self.assertEqual(mustahik.description, new_desc)
