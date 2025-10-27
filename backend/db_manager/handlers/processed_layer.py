from backend.db_manager.models import ProcessedLayerORM
from backend.db_manager.definitions import ProcessedLayer
from backend.utils.stats_generator import StatisticsGenerator

import numbers

class ProcessedLayerHandler:
    def __init__(self, db_url: str):
        self.orm = ProcessedLayerORM(db_url=db_url)
        self.stats_generator = StatisticsGenerator()

    @staticmethod
    def validate_coordinates(latitude, longitude) -> bool:
        return isinstance(latitude, numbers.Real) and isinstance(longitude, numbers.Real)

    def get_from_db(self, pl_id) -> ProcessedLayer | None:
        db_result = self.orm.get_by_id(pl_id=pl_id)
        if db_result:
            return db_result
        return None

    def _get_statistics(self, payload: dict) -> dict:
        general = self.stats_generator.get_general(data=payload)
        weather = self.stats_generator.get_general(data=payload)
        precipitation = self.stats_generator.get_general(data=payload)

        return {
            **payload,
            "general_stats": general,
            "weather_stats": weather,
            "precipitation_stats": precipitation,
        }

    def insert_in_db(self, payload: dict) -> ProcessedLayer:
        record = self.orm.create(payload=payload)
        return record


    def monitor(self, payload: dict):
        db_result = self.get_from_db(pl_id=payload.get("results_id"))
        if db_result:
            print("Returning from DB")
            return db_result

        print("Processing data")
        processed_data = self._get_statistics(payload=payload)
        processed_layer_record = self.insert_in_db(
            payload=processed_data,
        )
        return processed_layer_record




