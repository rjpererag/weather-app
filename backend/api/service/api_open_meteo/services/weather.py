from .request import RequestService
from ..dataclasses.weather import WeatherData


class WeatherService(RequestService):

    def get_archived_weather(
            self,
            latitude: float,
            longitude: float,
            start_date: str,
            end_date: str,
    ) -> WeatherData | None:

        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly":  ["temperature_2m", "precipitation"],
        }

        response = self._get(url, params=params)
        return WeatherData(**response) if response else None