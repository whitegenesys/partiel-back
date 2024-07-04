import requests
import json
from datetime import date, datetime
from urllib.parse import urlparse, urlencode
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
from cachetools import TTLCache, cached

# Configuration de l'API OpenWeatherMap
API_KEY = "578485d42ee05d236a960b75dbcf2544"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Cache pour stocker les résultats des requêtes
cache = TTLCache(maxsize=100, ttl=300)  # Cache de 5 minutes

# Modèles de données
class WeatherData(BaseModel):
    temperature: float
    temp_min: float
    temp_max: float
    humidity: int
    wind_speed: float
    wind_deg: int
    pressure: int
    weather_description: str
    sunrise: int
    sunset: int

class WeatherResponse(BaseModel):
    city: str
    data: WeatherData

# Client pour l'API OpenWeatherMap
class WeatherClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    @cached(cache)
    def get_weather(self, city: str):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        url_with_params = f"{self.api_url}?{urlencode(params)}"
        response = requests.get(url_with_params)
        response.raise_for_status()
        return response.json()

client = WeatherClient(API_KEY, API_URL)

# Application FastAPI
app = FastAPI()

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str, data_type: Optional[str] = Query(None, alias="filter")):
    try:
        data = client.get_weather(city)
        weather_data = WeatherData(
            temperature=data['main']['temp'],
            temp_min=data['main']['temp_min'],
            temp_max=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
            pressure=data['main']['pressure'],
            weather_description=data['weather'][0]['description'],
            sunrise=data['sys']['sunrise'],
            sunset=data['sys']['sunset']
        )
        if data_type:
            filtered_data = {key: value for key, value in weather_data.dict().items() if data_type in key}
            return WeatherResponse(city=city, data=filtered_data)
        return WeatherResponse(city=city, data=weather_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="City not found or API error")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="API request failed")

# Endpoint pour filtrer les données météorologiques
@app.get("/weather/{city}/{data_type}", response_model=WeatherResponse)
async def get_filtered_weather(city: str, data_type: str):
    try:
        data = client.get_weather(city)
        weather_data = WeatherData(
            temperature=data['main']['temp'],
            temp_min=data['main']['temp_min'],
            temp_max=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
            pressure=data['main']['pressure'],
            weather_description=data['weather'][0]['description'],
            sunrise=data['sys']['sunrise'],
            sunset=data['sys']['sunset']
        )
        filtered_data = {key: value for key, value in weather_data.dict().items() if data_type in key}
        return WeatherResponse(city=city, data=filtered_data)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="City not found or API error")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="API request failed")

# Fonction pour enregistrer les données météorologiques dans un fichier
def save_weather_data_to_file(api_key, city_name):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # or 'imperial' for Fahrenheit
    }
    url_with_params = f"{base_url}?{urlencode(params)}"
    
    result = requests.get(url_with_params)
    result.raise_for_status()  # Raise an error for bad responses
    
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

# Testez la fonction de sauvegarde des données météorologiques
save_weather_data_to_file(API_KEY, "Lyon")