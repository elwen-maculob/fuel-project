import math
import json
import os
from .csv_parser_fp import FUEL_STATION_LIST
from .geocoding_routing import get_route

def load_cached_coords(city, state):
    cache_path = os.path.join(os.path.dirname(__file__), 'station_cache.json')
    try:
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                return cache.get(f"{city}, {state}")
    except Exception:
        pass
    return None

def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius_in_miles = 3958.8
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    central_angle = 2 * math.asin(math.sqrt(a))
    return earth_radius_in_miles * central_angle

def is_near_route(station_lat, station_lon, geometry, max_distance_miles=15.0):
    """Checks if a station is within max_distance_miles of any point along the route geometry.
       Steps through geometry points (every 10th point) for performance.
    """
    for lon, lat in geometry[::10]:
        if calculate_distance(station_lat, station_lon, lat, lon) <= max_distance_miles:
            return True
    return False

def optimal_fuel_stops(start_text, finish_text, fuel_station_list, miles_per_gallon=10, max_range=500):
    route_data = get_route(start_text, finish_text)
    if not route_data:
        raise ValueError("Cannot calculate route between start and finish.")

    total_distance = route_data['distance_miles']
    geometry = route_data['geometry']

    # 1. Filter valid stations with coordinates
    valid_stations = []
    for station in fuel_station_list:
        lat = station.get('lat')
        lon = station.get('lon')

        if not lat or not lon:
            coords = load_cached_coords(station.get('city'), station.get('state'))
            if coords and coords.get('lat') and coords.get('lon'):
                lat = coords['lat']
                lon = coords['lon']
            else:
                continue

        station['lat'] = float(lat)
        station['lon'] = float(lon)
        valid_stations.append(station)

    # 2. Filter stations that actually fall near the route geometry
    route_stations = [
        s for s in valid_stations 
        if is_near_route(s['lat'], s['lon'], geometry, max_distance_miles=15.0)
    ]

    # Calculate fuel requirements
    gallons_needed = total_distance / miles_per_gallon
    stops = []
    
    # 3. Pick the cheapest station along the filtered route
    if route_stations:
        cheapest_station = min(route_stations, key=lambda s: float(s.get('Retail Price', 999)))
        
        station_name = (
            cheapest_station.get('Truckstop Name') or 
            cheapest_station.get('station_name') or 
            cheapest_station.get('Name') or 
            'Fuel Station'
        )
        city = cheapest_station.get('City') or cheapest_station.get('city') or ''
        state = cheapest_station.get('State') or cheapest_station.get('state') or ''
        price_per_gallon = float(cheapest_station.get('Retail Price', 3.50))
        
        stops.append({
            'station_name': station_name,
            'city': city,
            'state': state,
            'price_per_gallon': price_per_gallon,
            'lat': cheapest_station['lat'],
            'lon': cheapest_station['lon']
        })
        
        total_cost = round(gallons_needed * price_per_gallon, 2)
    elif valid_stations:
        # Fallback if no stations are within 15 miles of the exact route line
        cheapest_station = min(valid_stations, key=lambda s: float(s.get('Retail Price', 999)))
        price_per_gallon = float(cheapest_station.get('Retail Price', 3.50))
        total_cost = round(gallons_needed * price_per_gallon, 2)
    else:
        total_cost = round(gallons_needed * 3.50, 2)

    return {
        'total_distance_miles': round(total_distance, 2),
        'stops': stops,
        'total_cost': total_cost
    }