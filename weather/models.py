from django.db import models

# Create your models here.

class WeatherRecord(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)  # saves timestamp automatically

    def __str__(self):
        return f"{self.city} ({self.temperature}°C)"

