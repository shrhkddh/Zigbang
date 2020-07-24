import json

from django.test import (
    TestCase,
    Client
)

from map.models import (
    City,
    District,
    Province,
    ComplexType,
    Complex,
    Subway,
    Line,
    SubwayLine,
    SchoolEstablishmentType,
    SchoolGender,
    SchoolType,
    SchoolCategory,
    School
)

class SearchViewTest(TestCase):
    def setUp(self):
        client = Client()
        city   = City.objects.create(
            id   = 1,
            name = '천국시'
        )
        district = District.objects.create(
            id   = 1,
            name = '천국구',
            city = city 
        )
        province = Province.objects.create(
            id       = 1,
            name     = '천국동',
            district = district
        )
        complex_type = ComplexType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        complexes = Complex.objects.create(
            id             = 1,
            complex_type   = complex_type,
            name           = '천국오피스텔',
            complex_number = 247,
            longitude      = '127.0428237915039',
            latitude       = '37.50341796875',
            province       = province,
            household      = 220,
            builddate      = '2020-07-11'
        )
        subway = Subway.objects.create(
            id          = 1,
            subway_code = 111,
            name        = '천국역',
            longitude   = '198.7654321',
            latitude    = '98.7654321',
            local       = '수도권'
        )
        line = Line.objects.create(
            id    = 1,
            name  = '천국선',
            color = '#ffffff'
        )
        SubwayLine.objects.create(
            id     = 1,
            subway = subway,
            line   = line
        )
        school_gender = SchoolGender.objects.create(
            id   = 1,
            name = 'both'
        )
        school_establishment_type = SchoolEstablishmentType.objects.create(
            id   = 1,
            name = 'public'
        )
        school_type = SchoolType.objects.create(
            id   = 1,
            name = '일반고등학교'
        )
        school_category = SchoolCategory.objects.create(
            id   = 1,
            name = 'high'
        )
        School.objects.create(
            id                        = 1,
            school_gender             = school_gender,
            school_type               = school_type,
            school_category           = school_category,
            address                   = '천국시 천국구 천국동 123',
            district                  = district,
            road_address              = '천국시 천국구 천국로 456',
            longitude                 = '127.009313836442800',
            latitude                  = '37.511063320925740',
            foundation_date           = '1981-03-01',
            name                      = '천국고등학교',
            school_establishment_type = school_establishment_type,
            school_phone_number       = '02-593-6578'
        )

    def tearDown(self):
        City.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()
        ComplexType.objects.all().delete()
        Complex.objects.all().delete()
        Subway.objects.all().delete()
        Line.objects.all().delete()
        SubwayLine.objects.all().delete()
        SchoolGender.objects.all().delete()
        SchoolEstablishmentType.objects.all().delete()
        SchoolType.objects.all().delete()
        SchoolCategory.objects.all().delete()
        School.objects.all().delete()

    def test_post_searchview_success(self):
        client      = Client()
        search_term = {
            'searchTerm' : '천'
        }
        response = client.post('/search', json.dumps(search_term), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'complexes' : [
                    {
                        'type'      : '오피스텔',
                        'name'      : '천국오피스텔',
                        'city'      : '천국시',
                        'district'  : '천국구',
                        'province'  : '천국동',
                        'longitude' : '127.042823791503900',
                        'latitude'  : '37.503417968750000'
                    }
                ],
                'cities' : [
                    {
                        'type'      : '지역',
                        'name'      : '천국시',
                        'city'      : '천국시',
                        'district'  : None,
                        'province'  : None,
                        'longitude' : None,
                        'latitude'  : None
                    }
                ],
                'districts' : [
                    {
                        'type'      : '지역',
                        'name'      : '천국구',
                        'city'      : '천국시',
                        'district'  : '천국구',
                        'province'  : None,
                        'longitude' : None,
                        'latitude'  : None
                    }
                ],
                'provinces' : [
                    {
                        'type'      : '지역',
                        'name'      : '천국동',
                        'city'      : '천국시',
                        'district'  : '천국구',
                        'province'  : '천국동',
                        'longitude' : None,
                        'latitude'  : None
                    }
                ],
                'subways' : [
                    {
                        'type'      : '지하철',
                        'name'      : '천국역',
                        'city'      : '수도권',
                        'district'  : None,
                        'province'  : None,
                        'longitude' : '198.765432100000000',
                        'latitude'  : '98.765432100000000',
                        'line'      : [
                            '천국선'
                        ]
                    }
                ],
                'schools' : [
                    {
                        'type'      : '학교',
                        'name'      : '천국고등학교',
                        'city'      : '천국시',
                        'district'  : '천국구',
                        'province'  : '천국동',
                        'longitude' : '127.009313836442800',
                        'latitude'  : '37.511063320925740'
                    }
                ]
            }
        )

    def test_post_searchview_no_result(self):
        client      = Client()
        search_term = {
            'searchTerm' : 'ㅇ'
        }
        response = client.post('/search', json.dumps(search_term), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_searchview_invalid_key(self):
        client      = Client()
        search_term = {
            'search' : '천'
        }
        response = client.post('/search', json.dumps(search_term), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message' : 'Invalid key.'
            }
        )

    def test_post_searchview_blank(self):
        client      = Client()
        search_term = {
            'searchTerm' : ' '
        }
        response = client.post('/search', json.dumps(search_term), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_searchview_no_value(self):
        client      = Client()
        search_term = {
                'searchTerm' : ''
        }
        response = client.post('/search', json.dumps(search_term), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
