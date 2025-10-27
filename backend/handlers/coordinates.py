from backend.api_open_meteo import OpenMeteoAPI
from backend.db_manager.models import CoordinatesORM

import numbers

class CoordinatesHandler:
    def __init__(self, db_url: str):
        self.api = OpenMeteoAPI()
        self.orm = CoordinatesORM(db_url=db_url)

    @staticmethod
    def validate_coordinates(latitude, longitude) -> bool:
        return isinstance(latitude, numbers.Real) and isinstance(longitude, numbers.Real)

    def get_from_db(self, city_name: str) -> tuple[float | None, float | None]:
        db_result = self.orm.get_by_city_name(city_name=city_name)
        if db_result:
            return float(db_result.latitude), float(db_result.longitude)
        return None, None

    def get_from_api(self, city_name) -> tuple[float | None, float | None]:
        city_date = self.api.geolocation_service.get_city_data(city_name=city_name)
        if city_date:
            return city_date.latitude, city_date.longitude

        return None, None

    def insert_in_db(self, city_name: str, latitude: float, longitude: float) -> None:
        self.orm.create(city_name=city_name, latitude=latitude, longitude=longitude)

    def get_coordinates(self, city_name) -> tuple:

        lat_db, long_db = self.get_from_db(city_name=city_name)
        if lat_db and long_db:
            return lat_db, long_db

        lat, lon = self.get_from_api(city_name=city_name)
        if self.validate_coordinates(lat, lon):
            self.insert_in_db(city_name=city_name, latitude=lat, longitude=lon)
            return lat, lon

        return None, None