import csv
import json
import time
import requests

def get_coords(location_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': location_name, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'FuelRouteCalculatorAPP/1.0 (elwenmaculob@ymail.com)'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json()
            if results:
                return float(results[0]['lon']), float(results[0]['lat'])
    except Exception as e:
        print(f"Error geocoding {location_name}: {e}")
    return None

def build_cache():
    cache = {}
    print("Reading CSV and building coordinate cache...")
    
    with open('fuel_prices.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_state = f"{row['City']}, {row['State']}"
            if city_state not in cache:
                print(f"Geocoding new location: {city_state}")
                coords = get_coords(city_state)
                if coords:
                    cache[city_state] = {"lon": coords[0], "lat": coords[1]}
                else:
                    cache[city_state] = {"lon": None, "lat": None}
                time.sleep(1) # Respect Nominatim rate limit
                
    with open('station_cache.json', 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)
    print("Cache built successfully!")

if __name__ == '__main__':
    build_cache()