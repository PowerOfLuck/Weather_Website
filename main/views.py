from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
import requests

from .models import UserCity

def index(request):
    weather = None
    last_city = None

    # Ключ
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Проверка: Есть ли у пользователя последний город
    try:
        user_city = UserCity.objects.get(session_key=session_key)
        last_city = user_city.city
    except UserCity.DoesNotExist:
        user_city = None

    if request.method == 'POST':
        city = request.POST['city']
        
        # Координаты от OpenCageData
        geocode_url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key=d2b93cd321c14856b6382fc44da1280c'
        geocode_response = requests.get(geocode_url)
        
        if geocode_response.status_code == 200:
            geocode_data = geocode_response.json()
            results = geocode_data.get('results', [])
            if results:
                # Координаты из ответа
                latitude = results[0]['geometry']['lat']
                longitude = results[0]['geometry']['lng']
                
                # Погода от Open-Meteo
                weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m'
                weather_response = requests.get(weather_url)
                
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    hourly_data = weather_data.get('hourly', {})
                    temperature = hourly_data.get('temperature_2m', [None])[0]
                    
                    weather = {
                        'city': city,
                        'temperature': temperature, # Температура (Open-Meteo)
                        'latitude': latitude,  # Широта (OpenCageData)
                        'longitude': longitude,  # Долгота (OpenCageData)
                    }
                    
                    # Сохраняем/обновляем последний город
                    if user_city:
                        user_city.city = city
                        user_city.latitude = latitude
                        user_city.longitude = longitude
                        user_city.save()
                    else:
                        UserCity.objects.create(session_key=session_key, city=city, latitude=latitude, longitude=longitude)

    context = {'weather': weather, 'last_city': last_city}
    return render(request, 'main/index.html', context)
