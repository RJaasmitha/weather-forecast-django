import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import WeatherRecord
import plotly.express as px
import plotly.offline as opy
import os
from dotenv import load_dotenv   # ✅ NEW

# Load environment variables
load_dotenv()

def home(request):
    weather_data = None
    chart_div = None

    if request.method == "POST":
        city = request.POST.get("city")
        api_key = os.getenv("API_KEY") # ✅ fetch from .env
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        print("API Key:", api_key)
        print("City from form:", city)
        print("API Response:", response)

        if response.get("cod") == 200:  # success
            weather_data = {
                "city": city,
                "temperature": response["main"]["temp"],
                "condition": response["weather"][0]["description"],
                "humidity": response["main"]["humidity"],
                "wind_speed": response["wind"]["speed"],
            }

            # Save to DB
            WeatherRecord.objects.create(
                city=city,
                temperature=weather_data["temperature"],
                condition=weather_data["condition"],
                humidity=weather_data["humidity"],
                wind_speed=weather_data["wind_speed"],
            )

    # Get last 5 searches
    history = WeatherRecord.objects.all().order_by("-searched_at")[:5]

    # Create a temperature trend chart (from history)
    if history:
        df = {
            "City": [h.city for h in history],
            "Temperature": [h.temperature for h in history],
            "Humidity": [h.humidity for h in history],
        }

        fig = px.line(
            x=df["City"],
            y=df["Temperature"],
            markers=True,
            labels={"x": "City", "y": "Temperature (°C)"},
            title="Temperature Trend (Last Searches)"
        )
        chart_div = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, "weather/home.html", {
        "weather_data": weather_data,
        "history": history,
        "chart": chart_div
    })
