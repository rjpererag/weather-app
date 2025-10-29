import pandas as pd
from typing import Callable


class StatisticsGenerator:

    def __init__(self):
        self.df = pd.DataFrame()
        self.is_df_loaded = False
        self.is_valid_df = False


    @staticmethod
    def _validate_api_data(api_data: dict) -> bool:

        time = api_data.get("time", [])
        precipitation = api_data.get("precipitation", [])
        temperature = api_data.get("temperature_2m", [])

        if (len(time) == len(precipitation)) and (len(precipitation) == len(temperature)):
            return True
        return False

    def _load_df(self, data: dict) -> pd.DataFrame:
        try:
            api_response = data.get("raw_layer", {}).get("api_response", {})
            api_data = api_response.get("hourly")

            if (not api_data) or (not self._validate_api_data(api_data)):
                self.is_df_loaded = True
                return pd.DataFrame()

            df = pd.DataFrame(api_data)
            df["day"] = df["time"].apply(lambda row: row.split("T")[0])

            self.is_df_loaded = True
            self.is_valid_df = True
            return df

        except Exception as e:
            print(f"API response is not valid. {str(e)}")
            return pd.DataFrame()

    def _handle_df_loading(self, data: dict):
        if not self.is_df_loaded:
            self.df = self._load_df(data=data)

    @staticmethod
    def _get_weather_stats(
            df: pd.DataFrame,
            max_threshold: float | int = 30,
            min_threshold: float | int = 0,
    ) -> dict:

        try:
            average_temp = df["temperature_2m"].mean()
            daily_avg_temp = df.groupby("day")["temperature_2m"].mean().to_dict()

            max_temp = df["temperature_2m"].max()
            max_temp_day_df = df.loc[df["temperature_2m"] == max_temp].reset_index(drop=True)
            max_temp_day = {
                "value": max_temp_day_df.loc[0, "temperature_2m"],
                "date": max_temp_day_df.loc[0, "time"]
            }

            min_temp = df["temperature_2m"].min()
            min_temp_day_df = df.loc[df["temperature_2m"] == min_temp].reset_index(drop=True)
            min_temp_day = {
                "value": min_temp_day_df.loc[0, "temperature_2m"],
                "date": min_temp_day_df.loc[0, "time"]
            }

            hours_above = df.loc[df["temperature_2m"] >= max_threshold].shape[0]
            hours_below = df.loc[df["temperature_2m"] <= min_threshold].shape[0]

            return{
                "average": average_temp,
                "average_by_day": daily_avg_temp,
                "max": max_temp_day,
                "min": min_temp_day,
                "hours_above_threshold": hours_above,
                "hours_below_threshold": hours_below,
            }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _get_precipitation_stats(
            df: pd.DataFrame,
    ) -> dict:

        try:
            total = df.loc[df["precipitation"] > 0].shape[0]
            daily_total = df.groupby("day")["precipitation"].sum().to_dict()
            days_with_precipitation = len([val for val in daily_total.values() if val > 0])

            max_pre = df["precipitation"].max()
            max_pre_df = df.loc[df["precipitation"] == max_pre].reset_index(drop=True)
            max_pre_day = {
                "value": max_pre_df.loc[0, "precipitation"],
                "date": max_pre_df.loc[0, "time"]
            }

            average_pre = df["precipitation"].mean()

            return{
                "total": total,
                "total_by_day": daily_total,
                "days_with_precipitation": days_with_precipitation,
                "max": max_pre_day,
                "average": average_pre,
            }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _get_general_stats(
            data: dict,
            weather_stats: dict,
            precipitation_stats: dict
    ) -> dict:

        try:
            if not weather_stats.get("error"):
                weather_formatted = {
                    "temperature_average": weather_stats.get("average"),
                    "temperature_max": weather_stats.get("max"),
                    "temperature_min": weather_stats.get("min"),
                }
            else:
                weather_formatted = {}

            if not precipitation_stats.get("error"):
                precipitation_formatted = {
                    "precipitation_total": precipitation_stats.get("total"),
                    "days_with_precipitation": precipitation_stats.get("days_with_precipitation"),
                    "precipitation_max": precipitation_stats.get("max"),
                }
            else:
                precipitation_formatted = {}

            return {
                "start_date": data.get("start_date"),
                "end": data.get("end_date"),
                **weather_formatted,
                **precipitation_formatted
            }
        except Exception as e:
            return {"error": str(e)}


    def _get_stats(self, data: dict, func: Callable, **kwargs) -> dict:
        self._handle_df_loading(data=data)
        if not self.is_valid_df:
            return {"data": "Not available"}

        results = func(self.df, **kwargs)
        return results


    def get_weather(self, data) -> dict:
        max_threshold = data.get("max_threshold", 30)
        min_threshold = data.get("min_threshold", 2)

        results = self._get_stats(
            data=data,
            func=self._get_weather_stats,
            max_threshold=max_threshold,
            min_threshold=min_threshold,
        )
        return results

    def get_precipitation(self, data) -> dict:
        results = self._get_stats(
            data=data,
            func=self._get_precipitation_stats,
        )
        return results

    def get_general(self, data) -> dict:
        weather_stats = self.get_weather(data=data)
        precipitation_stats = self.get_precipitation(data=data)

        general_stats = self._get_general_stats(
            data=data,
            weather_stats=weather_stats,
            precipitation_stats=precipitation_stats
        )

        return general_stats
