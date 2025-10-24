from pydantic import BaseModel


class HourlyUnits(BaseModel):
    precipitation: str
    temperature_2m: str
    time: str

class Hourly(BaseModel):
    time: list[str] | None = None
    precipitation: list[float] | None = None
    temperature_2m: list[float] | None = None

class WeatherData(BaseModel):
    hourly_units: HourlyUnits
    hourly: Hourly | None = None