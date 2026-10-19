import requests

#using geocoder, convert location text to longitude, lattitude
def get_coords(location_name):
    url = "https://nominatim.openstreetmao.org/search"
    params = {
        'q': location_name
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'FuelRouteCalculatorAPP/1.0'}

    response=requests.get(url, params=params, headers=headers)
    if response.status_code==200:
        results=response.json()
        if results:
            latitude=float(results[0]['lat'])
            longitude=float(results[0]['lon'])
            return (longitude, latitude)
    return None

def get_route(start_text, finish_text):
    start_coords=get_coords(start_text)
    finish_coords=get_coords(finish_text)

    if not start_coords or not finish_coords:
        raise ValueError("Cannot geocode start and/or finish location/s.")

    url = f"https://router.project-osrm.org/route/v1/driving/{start_coords[0]},{start_coords[1]};{finish_coords[0]},{finish_coords[1]}"
    params = {
        'overview': 'full'
        'geometries': 'geojson'
    }

    response=requests.get(url, params=params)
    if response.status_code==200:
        data=response.json()
        if data.get('routes'):
            route=data['routes'][0]
            distancein_miles=route['distance']*0.000621371
            return{
                'distancein_miles': distancein_miles,
                'geometry': route['geometry']['coordinates']
            }
    return None