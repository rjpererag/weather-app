from time import sleep
from datetime import datetime, timedelta

from .coordinates import get_coordinates_func
from .weather_data import post_weather_data_func
from .transactions import get_transaction_status_func
from .results import search_results_func

from ..utils import logger


def _get_coordinates(db_url: str, city_name: str) -> dict :
    coordinates = get_coordinates_func(db_url=db_url, city_name=city_name)
    if coordinates.get("error"):
        return coordinates

    return coordinates


def _get_transaction_monitor_id(
        db_url: str,
        latitude: str,
        longitude: str,
        start_date: str,
        end_date: str,
) -> str | dict:

    monitor_id = None
    if latitude and longitude:
        transaction = post_weather_data_func(
            db_url=db_url,
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
        )

        if transaction.get("error"):
            return transaction

        monitor_id = transaction.get("id")

    return monitor_id


def _monitor_transaction(
        db_url: str,
        monitor_id: str,
        **kwargs,
):
    results = None

    if monitor_id:
        logger.error("Waiting for results")
        start = datetime.now()

        while True:
            try:
                status_json = get_transaction_status_func(
                    db_url=db_url,
                    transaction_id=monitor_id
                )

                status = status_json.get("status", "failed")

                if status == "failed":
                    break

                elif status == "ready":
                    logger.info("Collecting results")
                    results = search_results_func(
                        db_url=db_url,
                        transaction_id=monitor_id
                    )
                    break

                if datetime.now() - start > timedelta(minutes=kwargs.get("wait_time", 1)):
                    break

                sleep(1)
            except:
                results = {"error": "error getting results"}

    return results if results else {"error": "results not found"}


def get_city_stats_func(
        db_url: str,
        city_name: str,
        start_date: str,
        end_date: str,
        **kwargs
) -> dict:
    coordinates = _get_coordinates(db_url=db_url, city_name=city_name)
    latitude = coordinates.get("latitude")
    longitude = coordinates.get("longitude")

    monitor_id = _get_transaction_monitor_id(
        db_url=db_url,
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
    )

    results = _monitor_transaction(
        db_url=db_url,
        monitor_id=monitor_id,
        wait_time=kwargs.get("wait_time", 1),
    )

    return results

def handle_statistics_filtering(stats: str, city_stats: dict) -> dict:
    if stats == "general":
        city_stats_filtered = city_stats.get("general_statistics", {})

    elif stats == "weather":
        city_stats_filtered = city_stats.get("weather_statistics", {})

    elif stats == "precipitation":
        city_stats_filtered = city_stats.get("precipitation_statistics", {})
    else:
        city_stats_filtered = {"error": "not valid statistics"}

    return city_stats_filtered

