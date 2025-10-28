from pydantic import BaseModel


class GeolocationData(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    elevation: float | None = None
    country_code: str | None = None
    timezone: str | None = None
    population: int | None = None
    postcodes: list[str] | None = None
    country: str | None = None