from ...db_manager.models import RawLayerORM
from ...db_manager.definitions import RawLayer
from ...api_open_meteo import OpenMeteoAPI

import numbers

class RawLayerHandler:
    def __init__(self, db_url: str):
        self.orm = RawLayerORM(db_url=db_url)
        self.api = OpenMeteoAPI()

    @staticmethod
    def validate_coordinates(latitude, longitude) -> bool:
        return isinstance(latitude, numbers.Real) and isinstance(longitude, numbers.Real)

    def get_from_db(self, rl_id) -> RawLayer | None:
        db_result = self.orm.get_by_id(rl_id=rl_id)
        if db_result:
            return db_result
        return None

    def get_from_api(self, payload: dict):
        weather_data = self.api.weather_service.get_archived_weather(
            latitude=payload.get("latitude"),
            longitude=payload.get("longitude"),
            start_date=payload.get("start_date"),
            end_date=payload.get("end_date"),
        )

        return weather_data

    def insert_in_db(self, id_, api_response) -> RawLayer:
        record = self.orm.create(
            id_=id_,
            api_response=api_response
        )
        return record


    def monitor(self, payload: dict) -> RawLayer:
        db_result = self.get_from_db(rl_id=payload.get("raw_layer_id"))
        if db_result:
            print("Returning from DB")
            return db_result

        print("Calling OpenMeteoAPI")
        weather_data = self.get_from_api(payload=payload).model_dump()
        raw_layer_record = self.insert_in_db(
            id_=payload.get("raw_layer_id"),
            api_response=weather_data
        )
        return raw_layer_record




