from ..pipeline.functions import fetch_coordinates

def get_coordinates_func(db_url: str, city_name: str) -> dict:
    if not isinstance(city_name, str):
        return {"error": "city_name must be a string"}

    coordinates = fetch_coordinates(
        db_url=db_url,
        payload={"city_name": city_name.lower().strip()}
    )
    return coordinates