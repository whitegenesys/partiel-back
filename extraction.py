import requests
import json
from datetime import date, datetime
from urllib.parse import urlparse, urlencode

def get_weather_data(api_key, city_name):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # or 'imperial' for Fahrenheit
    }
    url_with_params = f"{base_url}?{urlencode(params)}"
    
    result = requests.get(url_with_params)
    
    endpoint = urlparse(base_url).path
    endpoint = endpoint.replace("/", "_")
    
    today = date.today()
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y")
    
    payload = {
        'data': result.json(),
        'date': date_time,
        'endpoint': endpoint
    }
    
    filename = f"{city_name}{endpoint}_{date_time}.json"
    with open(filename, "w") as outfile:
        json.dump(payload, outfile)


get_weather_data("578485d42ee05d236a960b75dbcf2544", "Lyon")