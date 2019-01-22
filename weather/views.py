import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a6be6d4bc61c5dd4dcd359913154cc69'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        resp = requests.get(url.format(city)).json()

        city_weather = {
            'name' : city.name,
            'temperature' :resp['main']['temp'],
            'description' : resp['weather'][0]['description'],
            'icon' : resp['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
