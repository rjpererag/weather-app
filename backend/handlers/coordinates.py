from backend.api_open_meteo import OpenMeteoAPI
from backend.db_manager.models import CoordinatesORM
from backend.db_manager.definitions import Coordinates

import numbers

class CoordinatesHandler:
    def __init__(self, db_url: str):
        self.api = OpenMeteoAPI()
        self.orm = CoordinatesORM(db_url=db_url)

    @staticmethod
    def validate_coordinates(latitude, longitude) -> bool:
        return isinstance(latitude, numbers.Real) and isinstance(longitude, numbers.Real)

    def get_from_db(self, city_name: str) -> Coordinates:
        db_result = self.orm.get_by_city_name(city_name=city_name)
        return db_result

    def get_from_api(self, city_name) -> tuple[float | None, float | None]:
        city_date = self.api.geolocation_service.get_city_data(city_name=city_name)
        if city_date:
            return city_date.latitude, city_date.longitude

        return None, None

    def insert_in_db(self, city_name: str, latitude: float, longitude: float) -> Coordinates:
        record = self.orm.create(city_name=city_name, latitude=latitude, longitude=longitude)
        return record

    def get_coordinates(self, city_name) -> dict:

        db_result = self.get_from_db(city_name=city_name)
        if db_result:
            print("Coordinates found in db")
            return {
                "coordinates_id": db_result.id,
                "city_name": db_result.city_name,
                "latitude": float(db_result.latitude),
                "longitude": float(db_result.longitude),
            }

        print("Calling Geolocation service")
        lat, lon = self.get_from_api(city_name=city_name)
        record = self.insert_in_db(city_name=city_name, latitude=lat, longitude=lon)
        return {
            "coordinates_id": record.id,
            "city_name": record.city_name,
            "latitude": float(record.latitude),
            "longitude": float(record.longitude),
        }
