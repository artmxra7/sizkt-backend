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

        data_source_institusi = DataSource.objects.create(
            category=DataSource.Category.INSTITUSI
        )

        institusi_detail = DataSourceInstitusi.objects.create(
            pic_ktp='12345678901234',
            pic_name='instisusi',
            pic_phone='123456789012',
            pic_position='Head',
            name='Institusi Bandung',
            province='Jawa Barat',
            sub_district='Bogor',
            village='Desa',
            rt='001',
            rw='001',
            address='Jalan suatu desa no 1',
            data_source=data_source_institusi,
        )

        data_source_warga = DataSource.objects.create(
            category=DataSource.Category.WARGA
        )

        warga_detail = DataSourceWarga.objects.create(
            pic_ktp='12345678901111',
            pic_name='wargai',
            pic_phone='123456789012',
            pic_position='Ketua RT',
            province='Test Barat',
            regency='Kabupaten test',
            sub_district='Testmatan',
            village='Desa tes',
            rt='001',
            rw='002',
            data_source=data_source_warga
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

    def test_data_source_warga_creation(self):
        data_source_warga = DataSourceWarga.objects.get(pic_ktp='12345678901111')
        self.assertTrue(isinstance(data_source_warga, DataSourceWarga))

    def test_data_source_institusi_creation(self):
        data_source_institusi = DataSourceInstitusi.objects.get(pic_ktp='12345678901234')
        self.assertTrue(isinstance(data_source_institusi, DataSourceInstitusi))


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
                "photo": "",
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
                "photo": "",
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
                mutation deleteMustahik($id: ID!) {
                    deleteMustahik(id: $id) {
                        deleted
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
        warga_detail = DataSourceWarga.objects.get(pic_ktp='1234567892')

        data_source_pekerja = DataSource.objects.create(
            category=DataSource.Category.PEKERJA
        )
        pekerja_detail = DataSourcePekerja.objects.create(
            pic_name='pic test',
            pic_ktp='1234567890',
            pic_phone='0812389120',
            pic_position='test',
            profession='tester',
            location='jl tester',
            data_source=data_source_pekerja,
        )
        data_source_institusi = DataSource.objects.create(
            category=DataSource.Category.INSTITUSI
        )
        institusi_detail = DataSourceInstitusi.objects.create(
            pic_name='pic test',
            pic_ktp='1234567891',
            pic_phone='0812389120',
            pic_position='test',
            name='test',
            province='test',
            sub_district='test',
            village='test',
            rw='01',
            rt='01',
            address='test',
            data_source=data_source_institusi,
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
            variables={'id1': warga_detail.data_source.pk,
                       'id2': pekerja_detail.data_source.pk,
                       'id3': institusi_detail.data_source.pk}
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(content['data']['q1']['id'], str(warga_detail.data_source.pk))
        self.assertEqual(content['data']['q1']['detail']['__typename'], 'DataSourceWargaType')
        self.assertEqual(content['data']['q2']['id'], str(pekerja_detail.data_source.pk))
        self.assertEqual(content['data']['q2']['detail']['__typename'], 'DataSourcePekerjaType')
        self.assertEqual(content['data']['q3']['id'], str(institusi_detail.data_source.pk))
        self.assertEqual(content['data']['q3']['detail']['__typename'], 'DataSourceInstitusiType')

    def test_data_source_mutation_can_add_new_data_source(self):
        existing_data_source_ammount = DataSource.objects.count()
        response = self.query(
            '''
            mutation dataSourceMutation($input: DataSourceMutationInput!){
                dataSourceMutation(input: $input){
                    dataSource{
                        category
                    }
                }
            }
            ''',
            op_name='dataSourceMutation',
            input_data={
                'category': 'WARGA',
            }
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['dataSourceMutation']['dataSource']['category'], "WARGA")

        # Validate successful save to db
        new_ammount = existing_data_source_ammount + 1
        self.assertEqual(DataSource.objects.count(), new_ammount)

    def test_data_source_warga_mutation_can_add_new_data_source_warga(self):
        pic_ktp = "123456789012"
        old_ammount = DataSourceWarga.objects.count()
        data_source_warga = DataSource.objects.create(category=DataSource.Category.WARGA)

        response = self.query(
            '''
            mutation dataSourceWargaMutation($input: DataSourceWargaMutationInput!){
                dataSourceWargaMutation(input: $input){
                    dataSourceWarga{
                        picName
                        picKtp
                        picPhone
                        picPosition
                        province
                        regency
                        subDistrict
                        village
                        rt
                        rw
                        dataSource{id}
                    }
                }
            }
            ''',
            op_name='dataSourceWargaMutation',
            input_data={
                "picName": "Anjay",
                "picKtp": pic_ktp,
                "picPhone": "1231231234",
                "picPosition": "Head",
                "province": "Jawa Barat",
                "regency": "Kebumen",
                "subDistrict": "Anjaydsitrict",
                "village": "Desa dusun",
                "rt": "001",
                "rw": "002",
                "dataSource": data_source_warga.pk
            }
        )
        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['dataSourceWargaMutation']
                         ['dataSourceWarga']['picKtp'], pic_ktp)

        # Validate successful save to db
        new_ammount = old_ammount + 1
        self.assertEqual(DataSourceWarga.objects.count(), new_ammount)
        source_warga = DataSourceWarga.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source_warga.pic_name, "Anjay")

    def test_data_source_warga_mutation_can_update_data_source_warga(self):
        pic_ktp = "123456789012"
        new_pic_name = "Aryo"
        data_source_warga = DataSource.objects.create(
            category=DataSource.Category.WARGA
        )

        warga_detail = DataSourceWarga.objects.create(
            pic_ktp=pic_ktp,
            pic_name='wargai',
            pic_phone='123456789012',
            pic_position='Ketua RT',
            province='Test Barat',
            regency='Kabupaten test',
            sub_district='Testmatan',
            village='Desa tes',
            rt='001',
            rw='002',
            data_source=data_source_warga
        )

        response = self.query(
            '''
            mutation dataSourceWargaMutation($input: DataSourceWargaMutationInput!){
                dataSourceWargaMutation(input: $input){
                    dataSourceWarga{
                        picName
                    }
                }
            }
            ''',
            op_name='dataSourceWargaMutation',
            input_data={
                "picName": new_pic_name,
                "picKtp": pic_ktp,
                "picPhone": "1231231234",
                "picPosition": "Head",
                "province": "Jawa Barat",
                "regency": "Kebumen",
                "subDistrict": "Anjaydsitrict",
                "village": "Desa dusun",
                "rt": "001",
                "rw": "002",
                "dataSource": data_source_warga.pk,
                "id": warga_detail.pk
            }
        )

        # Validate success update data source warga
        source = DataSourceWarga.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source.pic_name, new_pic_name)

    def test_data_source_pekerja_mutation_can_add_new_data_source_pekerja(self):
        pic_ktp = "123456789012"
        pic_name = "lulu"
        old_ammount = DataSourcePekerja.objects.count()
        data_source_pekerja = DataSource.objects.create(
            category=DataSource.Category.PEKERJA
        )

        response = self.query(
            '''
            mutation dataSourcePekerjaMutation($input: DataSourcePekerjaMutationInput!){
                dataSourcePekerjaMutation(input: $input){
                        dataSourcePekerja{
                        picName
                        picKtp
                        picPhone
                        picPosition
                        profession
                        location
                        dataSource{id}
                    }
                }
            }

            ''',
            op_name='dataSourcePekerjaMutation',
            input_data={
                "picName": pic_name,
                "picKtp": pic_ktp,
                "picPhone": "098765432123",
                "picPosition": "Leader",
                "profession": "Programmer",
                "location": "Bogor",
                "dataSource": data_source_pekerja.pk,
            }
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['dataSourcePekerjaMutation']
                         ['dataSourcePekerja']['picKtp'], pic_ktp)

        # Validate successful save to db
        new_ammount = old_ammount + 1
        self.assertEqual(DataSourcePekerja.objects.count(), new_ammount)
        source = DataSourcePekerja.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source.pic_name, pic_name)

    def test_data_source_pekerja_mutation_can_update_data_source_pekerja(self):
        pic_ktp = "123456789012"
        new_pic_name = "Aryo"

        data_source_pekerja = DataSource.objects.create(
            category=DataSource.Category.PEKERJA
        )
        source_pekerja = DataSourcePekerja.objects.create(
            pic_name='wargai',
            pic_ktp=pic_ktp,
            pic_phone='123456789012',
            pic_position='Ketua RT',
            profession='tester',
            location='jl tester',
            data_source=data_source_pekerja,
        )

        response = self.query(
            '''
            mutation dataSourcePekerjaMutation($input: DataSourcePekerjaMutationInput!){
                dataSourcePekerjaMutation(input: $input){
                        dataSourcePekerja{
                        picName
                    }
                }
            }
            ''',
            op_name="dataSourcePekerjaMutation",
            input_data={
                "picName": new_pic_name,
                "picKtp": pic_ktp,
                "picPhone": '123456789012',
                "picPosition": 'Ketua RT',
                "profession": 'tester',
                "location": 'jl tester',
                "dataSource": data_source_pekerja.pk,
                "id": source_pekerja.pk
            }
        )

        # Validate successful update to data source pekerja
        source = DataSourcePekerja.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source.pic_name, new_pic_name)

    def test_data_source_institusi_mutation_can_add_new_data_source_institusi(self):
        pic_ktp = "109872901098"
        pic_name = "Susi"
        old_ammount = DataSourceInstitusi.objects.count()
        data_source_institusi = DataSource.objects.create(
            category=DataSource.Category.INSTITUSI
        )

        response = self.query(
            '''
            mutation dataSourceInstitusiMutation($input: DataSourceInstitusiMutationInput!){
                dataSourceInstitusiMutation(input: $input){
                    dataSourceInstitusi{
                        picName
                        picKtp
                        picPhone
                        picPosition
                    }
                }
            }
        
            ''',
            op_name="dataSourceInstitusiMutation",
            input_data={
                "picName": pic_name,
                "picKtp": pic_ktp,
                "picPhone": "09876544323",
                "picPosition": "Vice",
                "name": "Pesantren Yatim",
                "province": "Jawa Barat",
                "regency": "Kabupaten",
                "subDistrict": "Dusun",
                "village": "desa",
                "rt": "002",
                "rw": "001",
                "address": "Jalan duku empat 1",
                "dataSource": data_source_institusi.pk,
            }
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Validate content
        content = json.loads(response.content)
        self.assertEqual(content['data']['dataSourceInstitusiMutation']
                         ['dataSourceInstitusi']['picKtp'], pic_ktp)

        # Validate success save to db
        new_ammount = old_ammount + 1
        self.assertEqual(DataSourceInstitusi.objects.count(), new_ammount)
        source = DataSourceInstitusi.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source.pic_name, pic_name)

    def test_data_source_institusi_mutation_can_update_data_source_institusi(self):
        pic_ktp = '12345678901234'
        new_pic_name = 'Rofi Arief'

        data_source_institusi = DataSource.objects.create(
            category=DataSource.Category.INSTITUSI
        )

        source_institusi = DataSourceInstitusi.objects.create(
            pic_ktp=pic_ktp,
            pic_name='Rofi',
            pic_phone='123456789012',
            pic_position='Head',
            name='Institusi Bandung',
            province='Jawa Barat',
            sub_district='Bogor',
            village='Desa',
            rt='001',
            rw='001',
            address='Jalan suatu desa no 1',
            data_source=data_source_institusi,
        )

        response = self.query(
            '''
            mutation dataSourceInstitusiMutation($input: DataSourceInstitusiMutationInput!){
                dataSourceInstitusiMutation(input: $input){
                    dataSourceInstitusi{
                        picName
                        picKtp
                        picPhone
                        picPosition
                    }
                }
            }
            ''',
            op_name='dataSourceInstitusiMutation',
            input_data={
                "picKtp": pic_ktp,
                "picName": new_pic_name,
                "picPhone": "123456789012",
                "name": "Institusi Bandung",
                "province": "Jawa Barat",
                "regency": "Kota",
                "subDistrict": "Bogor",
                "village": "Desa",
                "rt": "001",
                "rw": "001",
                "dataSource": data_source_institusi.pk,
                "id": source_institusi.pk,
            }
        )

        # Validate success update data source institusi
        source = DataSourceInstitusi.objects.get(pic_ktp=pic_ktp)
        self.assertEqual(source.pic_name, new_pic_name)

    def test_delete_datasource_mutations_can_delete_datasource(self):
        count = DataSource.objects.count()
        datasource = DataSource.objects.all()[0]
        response = self.query(
            '''
                mutation deleteDataSource($id: ID!) {
                    deleteDataSource(id: $id) {
                        deleted
                    }
                }
            ''',
            op_name='deleteDataSource',
            variables={'id': datasource.pk}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertTrue(content['data']['deleteDataSource']['deleted'])
        self.assertEquals(DataSource.objects.count(), count-1)

    def test_query_search_data_source_by_name(self):
        response = self.query(
            '''
            {
                dataSources(nameContains:"pinangranti") {
                    id
                    category
                    dataSourceDetail {
                    __typename
                    ... on DataSourceInstitusiType {
                        name
                    }
                    ... on DataSourcePekerjaType {
                        profession
                        location
                    }
                    ... on DataSourceWargaType {
                        rt
                        rw
                        village
                    }
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        datasources = json.loads(response.content)['data']['dataSources']
        for datasource in datasources:
            datasource_warga = datasource['dataSourceDetail']
            kelurahan = datasource_warga.get('village', None)
            self.assertIn(kelurahan, ['pinangranti', None])
