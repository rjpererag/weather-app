from ...api_open_meteo import OpenMeteoAPI

class CoordinatesHandler:
    def __init__(self):
        self.open_meteo_api = OpenMeteoAPI()

    def check_on_db(self) -> dict:
        ...

    def validate_db_result(self) -> bool:
        ...

    def get_from_api(self):
        ...

    def get_coordinates(self, city_name):
        ...