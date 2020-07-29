import json

from datetime import date
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone
from graphene_django.utils.testing import GraphQLTestCase
from sizakat.schema import schema

from .models import DataSource, DataSourceInstitusi, DataSourcePekerja, DataSourceWarga, Mustahik


class MustahikModelTestCase(TestCase):
    def setUp(self):
        data_source_detail = {
            'pic_name': 'pic test',
            'pic_ktp': '1234567890',
            'pic_phone': '0812389120',
            'pic_position': 'test',
        }
        data_source_pekerja = DataSource.objects.create(
            category=DataSource.Category.PEKERJA
        )
        pekerja_detail = DataSourcePekerja.objects.create(
            data_source=data_source_pekerja,
            profession='tester',
            location='jl tester'
        )
        mustahik_base = {
            'phone': '081234567890',
            'address': 'Jalan raya depok',
            'birthdate': date(1987, 6, 5),
            'status': Mustahik.Status.MISKIN,
            'gender': Mustahik.Gender.LAKILAKI,
        }
        mustahik = Mustahik.objects.create(
            name='mustahik1',
            no_ktp='31751234567891',
            data_source=data_source_pekerja,
            **mustahik_base
        )

    def test_mustahik_creation(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567891')
        self.assertTrue(isinstance(mustahik, Mustahik))

    def test_calculate_mustahik_age(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567891')
        self.assertEqual(
            mustahik.calculate_age(),
            timezone.now().year - mustahik.birthdate.year
        )


class MustahikGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        data_source_warga = DataSource.objects.create(
            category=DataSource.Category.WARGA
        )
        data_source_detail = DataSourceWarga.objects.create(
            data_source=data_source_warga,
            pic_name='pic test',
            pic_ktp='1234567892',
            pic_phone='0812389122',
            pic_position='test',
            province='jakarta',
            regency='jakarta timur',
            sub_district='makasar',
            village='pinangranti',
            rt='001',
            rw='001'
        )
        mustahik = Mustahik.objects.create(
            name='mustahik',
            no_ktp='31751234567890',
            phone='081234567890',
            address='Jalan raya depok',
            birthdate=date(1987, 6, 5),
            status=Mustahik.Status.MISKIN,
            gender=Mustahik.Gender.LAKILAKI,
            data_source=data_source_warga
        )

    def test_about_query(self):
        response = self.query('{ about }')
        self.assertResponseNoErrors(response)

    def test_mustahik_mutation_can_add_new_mustahik(self):
        no_ktp = '123891210121'
        data_source_warga = DataSourceWarga.objects.get(pic_ktp='1234567892')
        data_source = data_source_warga.data_source
        response = self.query(
            '''
            mutation mustahikMutation($input: MustahikMutationInput!) {
                mustahikMutation(input: $input) {
                    mustahik {
                        name
                        noKtp
                        status
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
                "birthdate": "1998-03-12",
                "status": "MISKIN",
                "gender": "L",
                "dataSource": data_source.pk
            }
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['mustahikMutation']
                         ['mustahik']['status'], 'MISKIN')

        # Validate success save to db
        self.assertEqual(Mustahik.objects.count(), 2)
        mustahik = Mustahik.objects.get(no_ktp=no_ktp)
        self.assertEqual(mustahik.name, 'jumat')

    def test_mustahik_mutation_can_update_mustahik(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        data_source_warga = DataSourceWarga.objects.get(pic_ktp='1234567892')
        data_source = data_source_warga.data_source
        mustahik_id = mustahik.pk
        old_status = mustahik.status
        new_status = 'MUSAFIR'
        response = self.query(
            '''
            mutation mustahikMutation($input: MustahikMutationInput!) {
                mustahikMutation(input: $input) {
                    mustahik {
                        id
                        status
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
                "birthdate": "1987-06-05",
                "status": "MUSAFIR",
                "gender": "L",
                "id": mustahik.pk,
                "dataSource": data_source.pk
            }
        )

        # Validate success update desc mustahik
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        self.assertEqual(mustahik.status, new_status)

    def test_query_mustahik_should_return_list_of_mustahiks(self):
        response = self.query(
            '''
            query mustahiksQuery{
                mustahiks {
                    id,
                    name
                }
            }
            ''',
            op_name='mustahiksQuery'
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['mustahiks']), 1)
        self.assertEqual(content['data']['mustahiks'][0]['name'], 'mustahik')

    def test_query_mustahiks_if_statuses_is_set_should_return_list_of_mustahiks_with_coresponding_status(self):
        response = self.query(
            '''
                query mustahiksQuery($statuses: [String]) {
                    mustahiks(statuses: $statuses) {
                        id,
                        name,
                        status
                    }
                }
            ''',
            op_name='mustahiksQuery',
            variables={'statuses': [Mustahik.Status.MISKIN]}
        )

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['mustahiks']), 1)

        for mustahik in content['data']['mustahiks']:
            self.assertEqual(mustahik['status'], Mustahik.Status.MISKIN)

    def test_query_mustahiks_if_statuses_is_provided_and_no_mustahiks_are_qualified_it_should_return_empty_list(self):
        response = self.query(
            '''
                query mustahiksQuery($statuses: [String]) {
                    mustahiks(statuses: $statuses) {
                        id,
                        name,
                        status
                    }
                }
            ''',
            op_name='mustahiksQuery',
            variables={'statuses': [Mustahik.Status.GHARIM]}
        )

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['mustahiks']), 0)

    def test_mustahik_mutation_can_delete_mustahik(self):
        count = Mustahik.objects.count()
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        mustahik_id = mustahik.pk
        response = self.query(
            '''
                mutation deleteMustahik($id: ID) {
                    deleteMustahik(id: $id) {
                        deleted
                        idMustahik
                        name
                        noKtp
                    }
                }
            ''',
            op_name='deleteMustahik',
            variables={'id': mustahik_id}
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteMustahik']['deleted'])
        self.assertEquals(Mustahik.objects.count(), count-1)

    def test_mustahik_query_can_read_detail_mustahik(self):
        mustahik = Mustahik.objects.get(no_ktp='31751234567890')
        mustahik_id = mustahik.pk
        response = self.query(
            '''
                query detailMustahikQuery($id:ID!){
                    mustahik(id:$id){
                        name
                        noKtp
                        address
                        age
                    }
                }
            ''',
            op_name='detailMustahikQuery',
            variables={'id': mustahik_id}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        data_mustahik = content['data']['mustahik']
        self.assertEqual(len(content['data']), 1)
        self.assertEqual(data_mustahik['name'], 'mustahik')
        self.assertEqual(data_mustahik['noKtp'], '31751234567890')
        self.assertEqual(data_mustahik['address'], 'Jalan raya depok')
        self.assertEqual(data_mustahik['age'], mustahik.calculate_age())

    def test_mustahiks_if_name_is_set_should_return_list_of_mustahiks_that_contain_the_name(self):
        response = self.query(
            '''
            query mustahiks($nameContains:String){
                mustahiks(nameContains: $nameContains){
                    id,
                    name
                }

            }
            ''',
            op_name='mustahiks',
            variables={'nameContains': 'hik'}
        )

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['mustahiks']), 1)
        self.assertEqual(
            content['data']['mustahiks'][0]['name'], 'mustahik')

    def test_mustahiks_if_name_is_not_available_should_return_empty_list(self):
        response = self.query(
            '''
            query mustahiks($nameContains:String){
                mustahiks(nameContains: $nameContains){
                    id,
                    name
                }

            }
            ''',
            op_name='mustahiks',
            variables={'nameContains': '#'}
        )

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['mustahiks']), 0)

    def test_data_sources_query_should_return_list_data_sources(self):
        response = self.query(
            '''
            query dataSourcesQuery{
                dataSources {
                    id
                    category
                    dataSourceDetail {
                        __typename
                        ... on DataSourceWargaType {
                            rt
                        }
                        ... on DataSourcePekerjaType {
                            profession
                        }
                        ... on DataSourceInstitusiType {
                            name
                        }
                    }
                }
            }
            ''',
            op_name='dataSourcesQuery'
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(len(content['data']['dataSources']), 1)
        self.assertEqual(content['data']['dataSources'][0]['category'], 'WARGA')

        first_data_source = content['data']['dataSources'][0]['dataSourceDetail']
        self.assertEqual(first_data_source['__typename'], 'DataSourceWargaType')
        self.assertTrue('rt' in first_data_source.keys())

    def test_data_sources_query_with_category_selection(self):
        response = self.query(
            '''
            query dataSourcesQuery($category: String) {
                dataSources(category: $category) {
                    id
                    category
                }
            }
            ''',
            op_name='dataSourcesQuery',
            variables={'category': DataSource.Category.WARGA}
        )

        content = json.loads(response.content)
        categories = [source['category'] for source in content['data']['dataSources']]
        self.assertTrue(all([category == DataSource.Category.WARGA for category in categories]))

    def test_data_source_query_detail_with_given_id(self):
        data_source_detail = {
            'pic_name': 'pic test',
            'pic_ktp': '1234567890',
            'pic_phone': '0812389120',
            'pic_position': 'test',
        }
        data_source_pekerja = DataSource.objects.create(
            category=DataSource.Category.PEKERJA
        )
        pekerja_detail = DataSourcePekerja.objects.create(
            data_source=data_source_pekerja,
            profession='tester',
            location='jl tester',
            **data_source_detail
        )
        data_source_institusi = DataSource.objects.create(
            category=DataSource.Category.INSTITUSI
        )
        pekerja_detail = DataSourceInstitusi.objects.create(
            data_source=data_source_institusi,
            name='test',
            province='test',
            regency='test',
            sub_district='test',
            village='test',
            rw='01',
            rt='01',
            address='test',
            **data_source_detail
        )
        response = self.query(
            '''
            query dataSourceQuery($id1: ID!, $id2: ID!, $id3: ID!) {
                q1: dataSource(id: $id1) {
                    id
                    detail: dataSourceDetail { __typename }
                }
                q2: dataSource(id: $id2) {
                    id
                    detail: dataSourceDetail { __typename }
                }
                q3: dataSource(id: $id3) {
                    id
                    detail: dataSourceDetail { __typename }
                }
            }
            ''',
            op_name='dataSourceQuery',
            variables={'id1': 2, 'id2': 3, 'id3': 4}
        )
        content = json.loads(response.content)
        self.assertEqual(content['data']['q1']['id'], '2')
        self.assertEqual(content['data']['q1']['detail']['__typename'], 'DataSourceWargaType')
        self.assertEqual(content['data']['q2']['id'], '3')
        self.assertEqual(content['data']['q2']['detail']['__typename'], 'DataSourcePekerjaType')
        self.assertEqual(content['data']['q3']['id'], '4')
        self.assertEqual(content['data']['q3']['detail']['__typename'], 'DataSourceInstitusiType')
