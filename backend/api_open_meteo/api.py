from .services import *

class OpenMeteoAPI:

    def __init__(self):
        self.geolocation_service = GeolocationService()
        self.weather_service = WeatherService()
