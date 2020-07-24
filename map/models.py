from django.db import models

class City(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'cities'

class District(models.Model):
    name = models.CharField(max_length = 50)
    city = models.ForeignKey('City', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'districts'

class Province(models.Model):
    name     = models.CharField(max_length = 50)
    district = models.ForeignKey('District', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'provinces'

class Subway(models.Model):
    subway_code = models.IntegerField()
    name        = models.CharField(max_length = 50)
    longitude   = models.DecimalField(max_digits = 18, decimal_places = 15)
    latitude    = models.DecimalField(max_digits = 18, decimal_places = 15)
    local       = models.CharField(max_length = 50, null = True, blank = True)
    line        = models.ManyToManyField('Line', through = 'SubwayLine')

    class Meta:
        db_table = 'subways'

class Line(models.Model):
    name  = models.CharField(max_length = 50)
    color = models.CharField(max_length = 50)

    class Meta:
        db_table = 'line'

class SubwayLine(models.Model):
    subway = models.ForeignKey('Subway', on_delete = models.SET_NULL, null = True)
    line   = models.ForeignKey('Line', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'subways_line'

class RoomSubway(models.Model):
    room   = models.ForeignKey('Room', on_delete = models.SET_NULL, null = True)
    subway = models.ForeignKey('Subway', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'rooms_subways'

class School(models.Model):
    school_gender             = models.ForeignKey('SchoolGender', on_delete = models.SET_NULL, null = True)
    school_type               = models.ForeignKey('SchoolType', on_delete = models.SET_NULL, null = True)
    school_category           = models.ForeignKey('SchoolCategory', on_delete = models.SET_NULL, null = True)
    address                   = models.CharField(max_length = 500)
    district                  = models.ForeignKey('District', on_delete = models.SET_NULL, null = True)
    road_address              = models.CharField(max_length = 500)
    longitude                 = models.DecimalField(max_digits = 18, decimal_places = 15)
    latitude                  = models.DecimalField(max_digits = 18, decimal_places = 15)
    foundation_date           = models.CharField(max_length = 50)
    name                      = models.CharField(max_length = 50)
    school_establishment_type = models.ForeignKey(
                                    'SchoolEstablishmentType', on_delete = models.SET_NULL, null = True)
    school_phone_number       = models.CharField(max_length = 50)

    class Meta:
        db_table = 'schools'

class SchoolEstablishmentType(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'school_establishment_types'

class SchoolGender(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'school_genders'

class SchoolType(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'school_types'

class SchoolCategory(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'school_categories'

class ComplexType(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'complex_types'

class Complex(models.Model):
    complex_type            = models.ForeignKey('ComplexType', on_delete = models.SET_NULL, null = True)
    name                    = models.CharField(max_length = 50)
    complex_number          = models.IntegerField()
    longitude               = models.DecimalField(max_digits = 18, decimal_places = 15)
    latitude                = models.DecimalField(max_digits = 18, decimal_places = 15)
    province                = models.ForeignKey('Province', on_delete = models.SET_NULL, null = True)
    household               = models.IntegerField(default = 1)
    builddate               = models.CharField(max_length = 50)
    complex_image_thumbnail = models.URLField(max_length = 2000, null = True, blank = True) 

    class Meta:
        db_table = 'complexes'

class Room(models.Model):
    building_number             = models.CharField(max_length = 50, null = True, blank = True)
    description                 = models.CharField(max_length = 100, null = True, blank = True)
    detail_description          = models.CharField(max_length = 3000, null = True, blank = True)
    post_date                   = models.CharField(max_length = 50, null = True, blank = True)
    is_recommended              = models.BooleanField(default = 0)
    room_type                   = models.ForeignKey('RoomType', on_delete = models.SET_NULL, null = True)
    sub_room_type               = models.ForeignKey('SubRoomType', on_delete = models.SET_NULL, null = True)
    sale_registration_number    = models.IntegerField()
    supply_area_square_meter    = models.DecimalField(max_digits = 10, decimal_places = 2)
    exclusive_area_square_meter = models.DecimalField(max_digits = 10, decimal_places = 2)
    maintenance_fee             = models.DecimalField(max_digits = 5, decimal_places = 2, null = True, blank = True)
    is_parking_lot              = models.BooleanField(default = 0)
    is_elevator                 = models.BooleanField(default = 0)
    floor                       = models.CharField(max_length = 50)
    entire_floor                = models.CharField(max_length = 50)
    moving_in_date_type         = models.CharField(max_length = 100, null = True, blank = True)
    agent_comment               = models.CharField(max_length = 3000, null = True, blank = True)
    agency                      = models.ForeignKey('Agency', on_delete = models.SET_NULL, null = True)
    complex                     = models.ForeignKey('Complex', on_delete = models.CASCADE)
    subway                      = models.ManyToManyField('Subway', through = 'RoomSubway')
    trade_type                  = models.ManyToManyField('TradeType', through = 'RoomTradeType')
    maintenance_option          = models.ManyToManyField('MaintenanceOption', through = 'RoomMaintenanceOption')
    room_option                 = models.ManyToManyField('RoomOption', through = 'RoomRoomOption')
    room_image_thumbnail        = models.URLField(max_length = 2000, null = True, blank = True)

    class Meta:
        db_table = 'rooms'

class TradeType(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'trade_types'

class RoomTradeType(models.Model):
    room         = models.ForeignKey('Room', on_delete = models.SET_NULL, null = True)
    trade_type   = models.ForeignKey('TradeType', on_delete = models.SET_NULL, null = True)
    deposit      = models.DecimalField(max_digits = 20, decimal_places = 2)
    monthly_rent = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, blank = True)

    class Meta:
        db_table = 'rooms_trade_types'

class MaintenanceOption(models.Model):
    name      = models.CharField(max_length = 50)
    image_url = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'maintenance_options'

class RoomMaintenanceOption(models.Model):
    room               = models.ForeignKey('Room', on_delete = models.SET_NULL, null = True)
    maintenance_option = models.ForeignKey('MaintenanceOption', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'rooms_maintenance_options'

class RoomImage(models.Model):
    room      = models.ForeignKey('Room', on_delete = models.SET_NULL, null = True)
    image_url = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'room_images'

class RoomType(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'room_types'

class SubRoomType(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'sub_room_types'

class RoomOption(models.Model):
    name      = models.CharField(max_length = 50)
    image_url = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'room_options'

class RoomRoomOption(models.Model):
    room_option = models.ForeignKey('RoomOption', on_delete = models.SET_NULL, null = True)
    room        = models.ForeignKey('Room', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'rooms_room_options'

class Agency(models.Model):
    agency_number  = models.IntegerField()
    name           = models.CharField(max_length = 50)
    representative = models.CharField(max_length = 50)
    image_url      = models.URLField(max_length = 2000, null = True, blank = True)
    phone_number   = models.CharField(max_length = 50)
    address        = models.CharField(max_length = 500)

    class Meta:
        db_table = 'agencies'
