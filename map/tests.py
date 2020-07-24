from django.test import (
    TestCase,
    Client
)

from .models import (
    City,
    District,
    Province,
    RoomType,
    SubRoomType,
    RoomOption,
    MaintenanceOption,
    Agency,
    ComplexType,
    Complex,
    TradeType,
    Room,
    RoomTradeType,
    RoomImage,
    RoomRoomOption,
    RoomMaintenanceOption,
    Subway,
    Line,
    SubwayLine,
    RoomSubway
)
TestCase.maxDiff = None
class RoomListViewTest(TestCase):
    def setUp(self):
        client = Client()
        city = City.objects.create(
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
        room_type = RoomType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        sub_room_type = SubRoomType.objects.create(
            id   = 1,
            name = '포룸'
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
            longitude      = 127.0428237915039,
            latitude       = 37.50341796875,
            province       = province,
            household      = 220,
            builddate      = '2020-07-11'
        )
        trade_type = TradeType.objects.create(
            id   = 1,
            name = '깔세'
        )
        room = Room.objects.create(
            id                          = 1,
            description                 = '천국동에서 제일 좋은 천국오피스텔',
            is_recommended              = True,
            room_type                   = room_type,
            sub_room_type               = sub_room_type,
            sale_registration_number    = 12341234,
            supply_area_square_meter    = 59.12,
            exclusive_area_square_meter = 36.36,
            is_parking_lot              = True,
            is_elevator                 = False,
            floor                       = '초고',
            entire_floor                = '100층',
            complex_id                  = Complex.objects.get(id=1).id,
            room_image_thumbnail        = 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1'
        )
        RoomTradeType.objects.create(
            id           = 1,
            room         = room,
            trade_type   = trade_type,
            deposit      = 100,
            monthly_rent = 100
        )

    def tearDown(self):
        City.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()
        RoomType.objects.all().delete()
        SubRoomType.objects.all().delete()
        ComplexType.objects.all().delete()
        Complex.objects.all().delete()
        TradeType.objects.all().delete()
        Room.objects.all().delete()
        RoomTradeType.objects.all().delete()
        
    def test_get_roomlistview_success(self):
        client   = Client()
        response = self.client.get('/studio-flat/complex/247')
        self.assertEqual(response.json(), {
            'itemQuantity' : 1,
            'rooms' : [
                {
                    'district'     : '천국구',
                    'province'     : '천국동',
                    'thumbnailImg' : 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1',
                    'roomType'     : '오피스텔',
                    'subRoomType'  : '포룸',
                    'tradeType'    : '깔세',
                    'deposit'      : '100',
                    'monthlyRent'  : '100',
                    'supplyAreaM'  : '59m²',
                    'supplyAreaP'  : '18평',
                    'floor'        : '초고층',
                    'entireFloor'  : '100층',
                    'description'  : '천국동에서 제일 좋은 천국오피스텔'
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_get_roomdetailview_no_item(self):
        client   = Client()
        response = self.client.get('/studio-flat/complex/0')
        self.assertEqual(response.json(), {'message' : 'No items.'})
        self.assertEqual(response.status_code, 200)

    def test_get_roomdetailview_not_found(self):
        client   = Client()
        response = self.client.get('/studio-flat/complex/asdfasdf')
        self.assertEqual(response.status_code, 404)

class RoomDetailViewTest(TestCase):
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
        room_type = RoomType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        sub_room_type = SubRoomType.objects.create(
            id   = 1,
            name = '포룸'
        )
        room_option = RoomOption.objects.create(
            id        = 1,
            name      = '냉풍기',
            image_url = 'https://s.zigbang.com/zuix/ic_aircon_dim_cutline.png'
        )
        maintenance_option = MaintenanceOption.objects.create(
            id        = 1,
            name      = '청소',
            image_url = 'https://s.zigbang.com/zuix/ic_sink_dim_cutline.png'
        )
        agency = Agency.objects.create(
            id             = 1,
            agency_number  = 000000,
            name           = '천국공인중개사',
            representative = '김천국',
            image_url      = 'https://ic.zigbang.com/vp/profile/5479378/4e88d2d4105e710b85828a99716e0e288d82dabf.jpg?w=800&h=600&q=70',
            phone_number   = '010-1234-1234',
            address        = '천국시 천국구 천국동 123-12'
        )
        complex_type = ComplexType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        complexes = Complex.objects.create(
            id                      = 1,
            complex_type            = complex_type,
            name                    = '천국오피스텔',
            complex_number          = 247,
            longitude               = 37.5119323730469,
            latitude                = 127.048614501953,
            province                = province,
            household               = 220,
            builddate               = '2020-07-11',
            complex_image_thumbnail = 'https://ic.zigbang.com/ic/area/danji/57400-fedd3b8e86584e7494073ac0e1024759_r.jpg?w=400&h=300&q=70'
        )
        trade_type = TradeType.objects.create(
            id   = 1,
            name = '깔세'
        )
        room = Room.objects.create(
            id                          = 1,
            building_number             = '101동',
            description                 = '천국동에서 제일 좋은 천국오피스텔',
            detail_description          = '천국동에서 제일 좋은 천국오피스텔! 풀옵션, 올수리, 정남향 귀한 매물',
            post_date                   = '2020-07-11',
            is_recommended              = True,
            room_type                   = room_type,
            sub_room_type               = sub_room_type,
            sale_registration_number    = 12341234,
            supply_area_square_meter    = 59.12,
            exclusive_area_square_meter = 36.36,
            maintenance_fee             = 1.5,
            is_parking_lot              = True,
            is_elevator                 = False,
            floor                       = '초고',
            entire_floor                = '100층',
            moving_in_date_type         = '즉시입주',
            agent_comment               = '기다렸습니다. 제대로 모시겠습니다.',
            agency                      = agency,
            complex_id                  = Complex.objects.get(id=1).id,
            room_image_thumbnail        = 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1'
        )
        RoomTradeType.objects.create(
            id           = 1,
            room         = room,
            trade_type   = trade_type,
            deposit      = 100,
            monthly_rent = 100
        )
        room_image_urls = ['https://ic.zigbang.com/ic/items/22519520/1.jpg?w=800&h=600&q=70&a=1']
        for room_image_url in room_image_urls:
            RoomImage.objects.create(
                    room      = room,
                    image_url = room_image_url
            )
        RoomRoomOption.objects.create(
            id          = 1,
            room_option = room_option,
            room        = room
        )
        RoomMaintenanceOption.objects.create(
            id                 = 1,
            room               = room,
            maintenance_option = maintenance_option
        )
        subway = Subway.objects.create(
            id          = 1,
            subway_code = 111,
            name        = '천국역',
            longitude   = 98.7654321,
            latitude    = 198.7654321,
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
        RoomSubway.objects.create(
            id     = 1,
            room   = room,
            subway = subway
        )

    def tearDown(self):
        City.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()
        RoomType.objects.all().delete()
        SubRoomType.objects.all().delete()
        RoomOption.objects.all().delete()
        MaintenanceOption.objects.all().delete()
        Agency.objects.all().delete()
        ComplexType.objects.all().delete()
        Complex.objects.all().delete()
        TradeType.objects.all().delete()
        Room.objects.all().delete()
        RoomTradeType.objects.all().delete()
        RoomImage.objects.all().delete()
        RoomRoomOption.objects.all().delete()
        RoomMaintenanceOption.objects.all().delete()
        Subway.objects.all().delete()
        Line.objects.all().delete()
        SubwayLine.objects.all().delete()
        RoomSubway.objects.all().delete()

    def test_get_roomdetailview_success(self):
        client   = Client()
        response = self.client.get('/studio-flat/item/12341234')
        self.assertEqual(response.json(), {
            'roomDetail' : [
                {
                    'district'           : '천국구',
                    'province'           : '천국동',
                    'longitude'          : 37.5119323730469,
                    'latitude'           : 127.048614501953,
                    'roomImg'            : [
                        'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=800&h=600&q=70&a=1'
                    ],
                    'roomType'           : '오피스텔',
                    'subRoomType'        : '포룸',
                    'tradeType'          : '깔세',
                    'deposit'            : '100',
                    'monthlyRent'        : '100',
                    'registrationNum'    : 12341234,
                    'supplyAreaM'        : '59m²',
                    'supplyAreaP'        : '18평',
                    'exclusiveAreaM'     : '36m²',
                    'exclusiveAreaP'     : '11평',
                    'maintenanceFee'     : 1.5,
                    'description'        : '천국동에서 제일 좋은 천국오피스텔',
                    'detailDescription'  : '천국동에서 제일 좋은 천국오피스텔! 풀옵션, 올수리, 정남향 귀한 매물',
                    'floor'              : '초고층',
                    'entireFloor'        : '100층',
                    'isParkingLot'       : True,
                    'isElevator'         : False,
                    'moveInDate'         : '즉시입주',
                    'roomOption'         : [
                        {
                            'optionName' : '냉풍기',
                            'iconImg'    : 'https://s.zigbang.com/zuix/ic_aircon_dim_cutline.png'
                        }
                    ],
                    'maintenanceOption'  : [
                        {
                            'optionName' : '청소',
                            'iconImg'    : 'https://s.zigbang.com/zuix/ic_sink_dim_cutline.png'
                        }
                    ],
                    'complexName'        : '천국오피스텔',
                    'complexThumbnail'   : 'https://ic.zigbang.com/ic/area/danji/57400-fedd3b8e86584e7494073ac0e1024759_r.jpg?w=400&h=300&q=70',
                    'complexHousehold'   : 220,
                    'complexBuildDate'   : '2020-07-11',
                    'subway'             : ['천국역(천국선)']
                }
            ],
            'agencies' : [
                {
                    'agencyPhoto'    : 'https://ic.zigbang.com/vp/profile/5479378/4e88d2d4105e710b85828a99716e0e288d82dabf.jpg?w=800&h=600&q=70',
                    'agencyName'     : '천국공인중개사',
                    'agentComment'   : '기다렸습니다. 제대로 모시겠습니다.',
                    'agencyRoomList' : [
                        {
                            'district'     : '천국구',
                            'province'     : '천국동',
                            'thumbnailImg' : 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1',
                            'roomType'     : '오피스텔',
                            'subRoomType'  : '포룸',
                            'tradeType'    : '깔세',
                            'deposit'      : '100',
                            'monthlyRent'  : '100'
                        }
                    ]
                }
            ]
        })
        self.assertEqual(response.status_code, 200)

    def test_get_roomdetailview_no_item(self):
        client   = Client()
        response = self.client.get('/studio-flat/item/11111111')
        self.assertEqual(response.json(), {'message' : 'No item.'})
        self.assertEqual(response.status_code, 200)

    def test_get_roomdetailview_not_found(self):
        client   = Client()
        response = self.client.get('/studio-flat/item/asdfasdf')
        self.assertEqual(response.status_code, 404)

class NearComplexInfoViewTest(TestCase):
    def setUp(self):
        client = Client()
        city = City.objects.create(
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
        room_type = RoomType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        sub_room_type = SubRoomType.objects.create(
            id   = 1,
            name = '포룸'
        )
        complex_type = ComplexType.objects.create(
            id   = 1,
            name = '오피스텔'
        )
        complexes = Complex.objects.create(
            id                      = 1,
            complex_type            = complex_type,
            name                    = '천국오피스텔',
            complex_number          = 247,
            longitude               = '127.042000000000000',
            latitude                = '37.503417968750000',
            province                = province,
            household               = 220,
            builddate               = '2020-07-11'
        )
        trade_type = TradeType.objects.create(
            id   = 1,
            name = '깔세'
        )
        room = Room.objects.create(
            id                          = 1,
            description                 = '천국동에서 제일 좋은 천국오피스텔',
            is_recommended              = True,
            room_type                   = room_type,
            sub_room_type               = sub_room_type,
            sale_registration_number    = '12341234',
            supply_area_square_meter    = '59.12',
            exclusive_area_square_meter = '36.36',
            maintenance_fee             = '1.5',
            is_parking_lot              = True,
            is_elevator                 = False,
            floor                       = '초고',
            entire_floor                = '100층',
            complex_id                  = Complex.objects.get(id=1).id,
            room_image_thumbnail        = 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1'
        )
        RoomTradeType.objects.create(
            id           = 1,
            room         = room,
            trade_type   = trade_type,
            deposit      = 100,
            monthly_rent = 100
        )

    def tearDown(self):
        City.objects.all().delete()
        District.objects.all().delete()
        Province.objects.all().delete()
        RoomType.objects.all().delete()
        SubRoomType.objects.all().delete()
        ComplexType.objects.all().delete()
        Complex.objects.all().delete()
        TradeType.objects.all().delete()
        Room.objects.all().delete()
        RoomTradeType.objects.all().delete()
        
    def test_get_nearcomplexinfoview_success(self):
        client   = Client()
        response = self.client.get('/studio-flat/map?longitude=127.0428237915039&latitude=37.50341796875')
        self.assertEqual(response.json(), {
            'result' : [{
                'complexName'           : '천국오피스텔',
                'complexNumber'         : 247,
                'itemQuantity'          : 1,
                'longitude'             : '127.042000000000000',
                'latitude'              : '37.503417968750000',
                'isParkingLot'          : True,
                'roomFilter' : [{
                        'registrationNum' : 12341234,
                        'city'            : '천국시',
                        'district'        : '천국구',
                        'province'        : '천국동',
                        'thumbnailImg'    : 'https://ic.zigbang.com/ic/items/22519520/1.jpg?w=400&h=300&q=70&a=1',
                        'description'     : '천국동에서 제일 좋은 천국오피스텔',
                        'recommend'       : True,
                        'tradeType'       : '깔세',
                        'subRoomType'     : '포룸',
                        'supplyAreaM'     : '59.12',
                        'supplyAreaP'     : 18,
                        'exclusiveAreaM'  : '36.36',
                        'exclusiveAreaP'  : 11,
                        'floor'           : '초고',
                        'entireFloor'     : '100층',
                        'deposit'         : '100.00',
                        'monthlyRent'     : '100.00',
                        'maintenanceFee'  : '1.50',
                    }
                ]
            }
        ]
    })
        self.assertEqual(response.status_code, 200)

    def test_get_nearcomplexinfoview_no_item(self):
        client   = Client()
        response = self.client.get('/studio-flat/map?longitude=1&latitude=1')
        self.assertEqual(response.json(), {'result': []})
        self.assertEqual(response.status_code, 200)

    def test_get_nearcomplexinfoview_not_found(self):
        client   = Client()
        response = self.client.get('/studio-flat/map?longitude=vbe&latitude=afe')
        self.assertEqual(response.status_code, 400)
