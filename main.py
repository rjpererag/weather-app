import os
if not os.path.exists('logs'):
    os.mkdir('logs')

import requests
from backend.api.service.api import create_app

def main():

    app = create_app()

    print("TEST COORDINATES")
    coordinates = requests.get('http://localhost:5001/coordinates/madrid')
    print(coordinates.json())
    print("-"*45)

    print("TEST MONITOR ID")
    monitor_id = requests.post(
        'http://localhost:5001/weather-data/40.4165/-3.70256/2024-01-01/2024-01-02'
    )
    monitor_id_json = monitor_id.json()
    print(monitor_id.json())
    print("-"*45)

    print("TEST STATUS")
    status = requests.get(f'http://localhost:5001/get-status/{monitor_id_json["id_to_monitor"]}')
    print(status.json())
    print("-"*45)

    print("TEST SEARCH RESULTS")
    results = requests.get(
        f'http://localhost:5001/search-results/{monitor_id_json["id_to_monitor"]}'
    )
    print(results.json())
    print("-"*45)


    print("TEST CITY-STATS")
    data = requests.get(
        'http://localhost:5001/city-stats/lisboa/2024-01-01/2024-01-02'
    )
    print(data.json())
    print("-"*45)

if __name__ == '__main__':
    main()