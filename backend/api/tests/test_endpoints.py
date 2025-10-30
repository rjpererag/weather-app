import time
import unittest

import requests
from .cases import *

class WeatherAPIEndpointsTest(unittest.TestCase):

    def setUp(self):
        self.db_url = "http://localhost:5001"

    def test_successful_get_coordinates(self):
        coordinates = requests.get(
            f'{self.db_url}/coordinates/madrid'
        )
        self.assertEqual(coordinates.status_code, 200)
        self.assertEqual(coordinates.json().get('latitude'), real_coordinates.get('latitude'))
        self.assertEqual(coordinates.json().get('longitude'), real_coordinates.get('longitude'))

    def test_failed_get_coordinates(self):
        coordinates = requests.get(
            f'{self.db_url}/coordinates/notexisting'
        )

        self.assertEqual(coordinates.status_code, 400)
        self.assertEqual(coordinates.json().get("error"), "coordinates not found")

    def test_post_weather_data(self):
        monitor_id = requests.post(
            f'{self.db_url}/weather-data/40.4165/-3.70256/2024-01-01/2024-01-02'
        )

        status = self._get_status(monitor_id=monitor_id.json())
        results = self._wait_for_results(monitor_id=monitor_id.json(), status=status.json())

        self.assertEqual(monitor_id.status_code, 200)
        self.assertIsInstance(monitor_id.json(), dict)

        self.assertEqual(status.status_code, 200)
        self.assertEqual(results.status_code, 200)

        self.assertEqual(results.json().get('general_statistics'), real_stats.get('general_statistics'))
        self.assertEqual(results.json().get('precipitation_statistics'), real_stats.get('precipitation_statistics'))
        self.assertEqual(results.json().get('weather_statistics'), real_stats.get('weather_statistics'))

    def test_get_city_stats(self):
        data = requests.get(
            f'{self.db_url}/city-stats/lisboa/2024-01-01/2024-01-02'
        )
        self.assertIsNone(data.json().get('error'))
        self.assertEqual(data.status_code, 200)

    def _get_status(self, monitor_id: dict):
        status = requests.get(
            f'{self.db_url}/get-status/{monitor_id.get("id_to_monitor")}')
        return status

    def _get_results(self, monitor_id: dict):
        results = requests.get(
            f'{self.db_url}/search-results/{monitor_id.get("id_to_monitor")}'
        )
        return results

    def _wait_for_results(self, monitor_id: dict, status: dict):
        while True:

            if (status.get("status") == "ready") or (status.get("status") == "error"):
                break

            time.sleep(1)
            status_response = self._get_status(monitor_id=monitor_id)
            status = status_response.json()

        results = self._get_results(monitor_id=monitor_id)
        return results

if __name__ == '__main__':
    unittest.main()
