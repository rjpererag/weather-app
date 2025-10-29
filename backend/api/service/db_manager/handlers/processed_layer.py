from ...db_manager.models import ProcessedLayerORM
from ...db_manager.definitions import ProcessedLayer
from ...utils import StatisticsGenerator, logger

import json

import numbers

class ProcessedLayerHandler:
    def __init__(self, db_url: str):
        self.orm = ProcessedLayerORM(db_url=db_url)
        self.stats_generator = StatisticsGenerator()

    @staticmethod
    def validate_coordinates(latitude, longitude) -> bool:
        return isinstance(latitude, numbers.Real) and isinstance(longitude, numbers.Real)

    def get_from_db(self, pl_id) -> ProcessedLayer | None:
        try:
            db_result = self.orm.get_by_id(pl_id=pl_id)
            if db_result:
                return db_result
            return None
        except:
            logger.error("      Failed to get processed data from DB")
            return None

    def _get_statistics(self, payload: dict) -> dict | None:
        try:
            logger.info("       Getting statistics")
            weather = self.stats_generator.get_weather(data=payload)
            precipitation = self.stats_generator.get_precipitation(data=payload)
            general = self.stats_generator.get_general(data=payload)

            return {
                **payload,
                "general_stats": general if general else None,
                "weather_stats": weather if weather else None,
                "precipitation_stats": precipitation if precipitation else None,
            }
        except:
            logger.error("      Failed to get data statistics")
            return None

    def insert_in_db(self, payload: dict) -> ProcessedLayer:
        record = self.orm.create(payload=payload)
        return record


    def monitor(self, payload: dict) -> ProcessedLayer | None:
        db_result = self.get_from_db(pl_id=payload.get("results_id"))
        if db_result:
            logger.info("       Returning from DB")
            return db_result

        logger.info("       Processing data")
        processed_data = self._get_statistics(payload=payload)

        if processed_data:
            processed_layer_record = self.insert_in_db(
                payload=processed_data,
            )
            return processed_layer_record
        return None




