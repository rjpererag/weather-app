
class IDGenerator:

    def __init__(self, payload: dict):
        self.payload = payload

    def create_base_id(self) -> str | None:
        longitude = self.payload.get("longitude")
        latitude = self.payload.get("longitude")
        start = self.payload.get("start_date")
        end = self.payload.get("end_date")

        _id = f"{longitude}_{latitude}_{start}_{end}"
        return _id

    @staticmethod
    def create_results_id(base_id: str) -> str | None:
        _id = f"pl_{base_id}"
        return _id


    @staticmethod
    def create_raw_layer_id(base_id: str) -> str | None:
        _id = f"rl_{base_id}"
        return _id

    def generate_ids(self) -> dict:
        base_id = self.create_base_id()
        return {
            "base_id": base_id,
            "raw_layer_id": self.create_raw_layer_id(base_id=base_id),
            "results_id": self.create_results_id(base_id=base_id),
        }