import json
from haversine             import haversine

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q


from .utils  import (
    change_price_to_string,
    change_maintenance_fee_to_string
)
from .models import (
    City,
    District,
    Province,
    ComplexType,
    Complex,
    RoomType,
    SubRoomType,
    RoomOption,
    TradeType,
    MaintenanceOption,
    Room,
    RoomImage,
    RoomRoomOption,
    RoomMaintenanceOption,
    RoomTradeType
)

class RoomListView(View):
    def get(self, request, code):
        CONVERTER = 0.3025
        room_list = Room.objects.prefetch_related(
            'complex__province__district',
            'room_type',
            'sub_room_type',
            'trade_type',
        ).filter(complex__complex_number = code)
    
        if room_list:
            rooms = [
                {
                    'district'     : room.complex.province.district.name,
                    'province'     : room.complex.province.name,
                    'thumbnailImg' : room.room_image_thumbnail,
                    'roomType'     : room.room_type.name,
                    'subRoomType'  : room.sub_room_type.name,
                    'tradeType'    : room.roomtradetype_set.get(
                                     room_id = room.id).trade_type.name,
                    'deposit'      : change_price_to_string(room.roomtradetype_set.get(
                                     room_id = room.id).deposit),
                    'monthlyRent'  : change_price_to_string(room.roomtradetype_set.get(
                                     room_id = room.id).monthly_rent) if room.roomtradetype_set.get(
                                     room_id = room.id) else None,
                    'supplyAreaM'  : str(int(room.supply_area_square_meter)) + 'm²',
                    'supplyAreaP'  : str(round(int(room.supply_area_square_meter) * CONVERTER)) + '평',
                    'floor'        : room.floor + '층',
                    'entireFloor'  : room.entire_floor,
                    'description'  : room.description
                } for room in room_list ]
            return JsonResponse(
                {
                    'itemQuantity' : len(room_list),
                    'rooms'        : rooms
                }, status = 200)
        return JsonResponse({'message' : 'No items.'}, status = 200)

class RoomDetailView(View):
    def get(self, request, code):
        CONVERTER = 0.3025
        rooms = Room.objects.prefetch_related(
            'complex__province__district',
            'subway__line',
            'roomimage_set',
            'room_option',
            'room_type',
            'sub_room_type',
            'maintenance_option',
            'trade_type',
            'agency')
        room_infos = rooms.filter(sale_registration_number = code)
            
        if room_infos:
            room_detail = [
                {
                    'district'          : info.complex.province.district.name,
                    'province'          : info.complex.province.name,
                    'longitude'         : float(info.complex.longitude),
                    'latitude'          : float(info.complex.latitude),
                    'roomImg'           : list(info.roomimage_set.values_list('image_url', flat = True)),
                    'roomType'          : info.room_type.name,
                    'subRoomType'       : info.sub_room_type.name,
                    'tradeType'         : info.roomtradetype_set.get(
                                          room_id = info.id).trade_type.name,
                    'deposit'           : change_price_to_string(info.roomtradetype_set.get(
                                          room_id = info.id).deposit),
                    'monthlyRent'       : change_price_to_string(info.roomtradetype_set.get(
                                          room_id = info.id).monthly_rent) if info.roomtradetype_set.get(
                                          room_id = info.id) else None,
                    'registrationNum'   : code,
                    'supplyAreaM'       : str(int(info.supply_area_square_meter)) + 'm²',
                    'supplyAreaP'       : str(round(int(info.supply_area_square_meter) * CONVERTER)) + '평',
                    'exclusiveAreaM'    : str(int(info.exclusive_area_square_meter)) + 'm²',
                    'exclusiveAreaP'    : str(round(int(info.exclusive_area_square_meter) * CONVERTER)) + '평',
                    'maintenanceFee'    : change_maintenance_fee_to_string(info.maintenance_fee),
                    'description'       : info.description,
                    'detailDescription' : info.detail_description,
                    'floor'             : info.floor + '층',
                    'entireFloor'       : info.entire_floor,
                    'isParkingLot'      : info.is_parking_lot,
                    'isElevator'        : info.is_elevator,
                    'moveInDate'        : info.moving_in_date_type,
                    'roomOption'        : [
                        {
                            'optionName' : option.name,
                            'iconImg'    : option.image_url
                        } for option in info.room_option.all()],
                    'maintenanceOption' : [
                        {
                            'optionName' : option.name,
                            'iconImg'    : option.image_url
                        } for option in info.maintenance_option.all()],
                    'complexName'      : info.complex.name,
                    'complexThumbnail' : info.complex.complex_image_thumbnail if info.complex.complex_image_thumbnail else None,
                    'complexHousehold' : info.complex.household,
                    'complexBuildDate' : info.complex.builddate,
                    'subway' : [
                        subway.name + '('
                        + ','.join(list(subway.line.values_list('name', flat = True)))
                        + ')' for subway in info.subway.all()]
                } for info in room_infos]

            agencies = [
                {
                    'agencyPhoto'    : info.agency.image_url if info.agency.image_url else None,
                    'agencyName'     : info.agency.name,
                    'agentComment'   : info.agent_comment if info.agent_comment else None,
                    'agencyRoomList' : [
                        {
                            'district'     : agency_room.complex.province.district.name,
                            'province'     : agency_room.complex.province.name,
                            'thumbnailImg' : agency_room.room_image_thumbnail,
                            'roomType'     : agency_room.room_type.name,
                            'subRoomType'  : agency_room.sub_room_type.name,
                            'tradeType'    : agency_room.roomtradetype_set.get(
                                             room_id = agency_room.id).trade_type.name,
                            'deposit'      : change_price_to_string(agency_room.roomtradetype_set.get(
                                             room_id = agency_room.id).deposit),
                            'monthlyRent'  : change_price_to_string(agency_room.roomtradetype_set.get(
                                             room_id = agency_room.id
                                             ).monthly_rent) if agency_room.roomtradetype_set.get(
                                             room_id = agency_room.id) else None
                        } for agency_room in rooms.filter(agency_id = info.agency.id)]
                } for info in room_infos]
            return JsonResponse({
                    'roomDetail' : room_detail,
                    'agencies'   : agencies
                }, status = 200)
        else:
            return JsonResponse({'message' : 'No item.'}, status = 200)

class NearComplexInfoView(View):
    def get(self, request):
        CONVERTER = 0.3025
        try:
            longitude = request.GET.get('longitude', None)
            latitude  = request.GET.get('latitude', None)

            if (latitude == None) or (longitude == None):
                return JsonResponse({'message' : 'No Location'}, status = 400)

            longitude = float(longitude)
            latitude  = float(latitude)
            position  = (longitude, latitude)

            radius = (
                Q(longitude__range = (longitude - 0.03, longitude + 0.03)) &
                Q(latitude__range  = (latitude - 0.02, latitude + 0.02))
            )            

            radius_complex = Complex.objects.filter(radius)
            complex_info   = radius_complex.select_related(
                'complex_type',
                'province__district__city',
            ).prefetch_related(
                'room_set__roomtradetype_set',
                'room_set__sub_room_type',
                )

            result = []
            for info in complex_info:
                distance  = haversine(position, (float(info.longitude), float(info.latitude)))
                room_list = info.room_set.all()

                if distance <= 1:

                    result.append({
                        'complexName'           : info.name,
                        'complexNumber'         : info.complex_number,
                        'itemQuantity'          : len(info.room_set.filter(complex = info.id)),
                        'longitude'             : info.longitude,
                        'latitude'              : info.latitude,
                        'isParkingLot'          : room_list[0].is_parking_lot,
                        'roomFilter'            : [{
                            'registrationNum'    : room_trade.sale_registration_number,
                            'city'               : info.province.district.city.name,
                            'district'           : info.province.district.name,
                            'province'           : info.province.name,
                            'thumbnailImg'       : room_trade.room_image_thumbnail,
                            'description'        : room_trade.description,
                            'recommend'          : room_trade.is_recommended,
                            'tradeType'          : trade_type.trade_type.name,
                            'subRoomType'        : room_trade.sub_room_type.name,
                            'supplyAreaM'        : room_trade.supply_area_square_meter,
                            'supplyAreaP'        : round(int(room_trade.supply_area_square_meter) * CONVERTER),
                            'exclusiveAreaM'     : room_trade.exclusive_area_square_meter,
                            'exclusiveAreaP'     : round(int(room_trade.exclusive_area_square_meter) * CONVERTER),
                            'floor'              : room_trade.floor,
                            'entireFloor'        : room_trade.entire_floor,
                            'deposit'            : trade_type.deposit, 
                            'monthlyRent'        : trade_type.monthly_rent,
                            'maintenanceFee'     : room_trade.maintenance_fee
                            } for room_trade in room_list for trade_type in room_trade.roomtradetype_set.all()]})
            return JsonResponse({'result' : result}, status = 200)
            
        except TypeError:
            return JsonResponse({'message' : 'INVALID_QUERY_PARAMETERS'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'INVALID_QUERY_PARAMETERS'}, status = 400)
