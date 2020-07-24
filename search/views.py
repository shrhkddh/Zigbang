import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

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


class SearchView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            search_term = data['searchTerm']
            if search_term == ' ' or search_term == '':
                return JsonResponse({'message' : 'No results.'}, status = 400)
            complexes = Complex.objects.prefetch_related('province__district__city')
            provinces = Province.objects.select_related('district__city')
            districts = District.objects.select_related('city')
            subways   = Subway.objects.prefetch_related('line')
            schools   = School.objects.select_related(
                'school_establishment_type',
                'school_gender',
                'school_type',
                'school_category'
            )
            
            search = Q(name__contains = search_term)
            complex_search_result  = complexes.filter(search)
            city_search_result     = City.objects.filter(search)
            district_search_result = districts.filter(search)
            province_search_result = provinces.filter(search)
            subway_search_result   = subways.filter(search)
            school_search_result   = schools.filter(search)

            complex_search_list = [
                {
                    'type'      : '오피스텔',
                    'name'      : word.name,
                    'city'      : word.province.district.city.name,
                    'district'  : word.province.district.name,
                    'province'  : word.province.name,
                    'longitude' : word.longitude,
                    'latitude'  : word.latitude
                } for word in complex_search_result]

            city_search_list = [
                {
                    'type'      : '지역',
                    'name'      : word.name,
                    'city'      : word.name,
                    'district'  : None,
                    'province'  : None,
                    'longitude' : None,
                    'latitude'  : None
                } for word in city_search_result]

            district_search_list = [
                {
                    'type'      : '지역',
                    'name'      : word.name,
                    'city'      : word.city.name,
                    'district'  : word.name,
                    'province'  : None,
                    'longitude' : None,
                    'latitude'  : None
                } for word in district_search_result]

            province_search_list = [
                {
                    'type'      : '지역',
                    'name'      : word.name,
                    'city'      : word.district.city.name,
                    'district'  : word.district.name,
                    'province'  : word.name,
                    'longitude' : None,
                    'latitude'  : None
                } for word in province_search_result]
            
            subway_search_list = [
                {
                    'type'       : '지하철',
                    'name'       : word.name,
                    'city'       : word.local,
                    'district'   : None,
                    'province'   : None,
                    'longitude'  : word.longitude,
                    'latitude'   : word.latitude,
                    'line'       : list(word.line.values_list('name', flat = True))
                } for word in subway_search_result]
            
            school_search_list = [
                {
                    'type'      : '학교',
                    'name'      : word.name,
                    'city'      : word.address.split(' ')[0],
                    'district'  : word.address.split(' ')[1],
                    'province'  : word.address.split(' ')[2],
                    'longitude' : word.longitude,
                    'latitude'  : word.latitude
                } for word in school_search_result]

            return JsonResponse(
                {
                    'complexes' : complex_search_list,
                    'cities'    : city_search_list,
                    'districts' : district_search_list,
                    'provinces' : province_search_list,
                    'subways'   : subway_search_list,
                    'schools'   : school_search_list
                }, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'Invalid key.'}, status = 400)
