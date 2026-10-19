import math
from .csv_parser_fp import FUEL_STATION_LIST
from .geocoding_routing import get_route

def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius_in_miles=3958.8
    latitude_to_radian1 = math.radians(lat1)
    latitude_to_radian2 = math.radians(lat2)
    difference_latitude = math.radians(lat2 - lat1)
    difference_longitude = math.radians(lon2 - lon1)
    
    a = (math.sin(difference_latitude / 2) ** 2 + 
         math.cos(latitude_to_radian1) * math.cos(latitude_to_radian2) * math.sin(difference_longitude / 2) ** 2)
    
    central_angle = 2 * math.asin(math.sqrt(a))
    
    return earth_radius_in_miles * central_angle

def optimal_fuel_stops(start_text, finish_text, fuel_station_list, miles_per_gallon=10, max_range=500):
    route_data=get_route(start_text, finish_text)
    if not route_data:
        raise ValueError("Cannot calculate route between start and finish.")

    total_distance=route_data['distance_miles']
    geometry=route_data['geometry']

    if total_distance <= max_range:
        pass

    valid_stations=[]
    for station in fuel_station_list:
        station_lattitude=station['lat']
        station_longitude=station['lon']

    return {
        'total_distancein_miles': total_distance,
        'stops':[],
        'total_cost': 0.0
    }