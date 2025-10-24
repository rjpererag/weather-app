from .request import RequestService
from ..dataclasses.geolocation import GeolocationData


class GeolocationService(RequestService):

    def get_city_data(self, city_name: str) -> GeolocationData | None:

        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name,
            "count": 1
        }

        response = self._get(url, params=params)
        if isinstance(response, dict) and (results := response.get("results")) and (isinstance(results, list)):
            return GeolocationData(**results[0])
        return None