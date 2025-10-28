from flask import Flask,jsonify

from .pipeline.functions import (fetch_coordinates, generate_ids, create_new_transaction, get_transaction_by_id)
from .db_manager.settings import DBSettings, create_db_url


app = Flask(__name__)

db_settings = DBSettings(host="localhost")
db_url = create_db_url(settings=db_settings)

# GET METHODS -------------------------------------------------------------------------------
@app.route('/coordinates/<string:city_name>', methods=["GET"])
def get_coordinates(city_name: str):
    try:
        if not isinstance(city_name, str):
            return jsonify({"error": "city_name must be a string"}), 400

        coordinates = fetch_coordinates(
            db_url=db_url,
            payload={"city_name": city_name.lower().strip()}
        )
        return jsonify(coordinates), 200
    except Exception:
        return jsonify({"error": f"{city_name} coordinates unavailable."}), 500


@app.route('/get-status/<string:transaction_id>', methods=["GET"])
def get_transaction_status(transaction_id: str):

    try:

        if not isinstance(transaction_id, str):
            return jsonify({"error": "transaction_id must be a string"}), 400

        transaction = get_transaction_by_id(
            db_url=db_url,
            id_=transaction_id
        )

        t_status = str(transaction.status_id)

        if  t_status == "0":
            status = "processing"
        elif t_status == "1":
            status = "ready"
        elif t_status == "2":
            status = "failed"
        else:
            status = "unknown"
        return jsonify({"status": status}), 200
    except Exception:
        return jsonify({"error": f"{transaction_id} status unavailable."}), 500

# POST METHODS ------------------------------------------------------------------------------
@app.route(
    '/weather-data/<string:latitude>/<string:longitude>/<string:start_date>/<string:end_date>',
    methods=['POST']
)
def post_weather_data(latitude: str, longitude: str, start_date: str, end_date: str):

    try:
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date
        }

        ids = generate_ids(payload=payload)
        payload = {**payload, **ids}

        transaction = create_new_transaction(db_url=db_url, payload=payload)

        if not transaction:
            return jsonify({"error": "bad request, no transaction created"}), 400

        payload = {**payload, **transaction}
        return jsonify({"id_to_monitor": payload.get("id")}), 200

    except Exception:
        return jsonify({"error": f"Error creating new transaction"}), 500

# @app.route(
#     '/statistics/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
#     methods=['POST']
# )
# def post_statistics():
#     return ...
#
# @app.route(
#     '/statistics/weather/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
#     methods=['POST']
# )
# def post_statistics_weather():
#     return ...
#
# @app.route(
#     '/statistics/precipitation/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
#     methods=['POST']
# )
# def post_statistics_precipitation():
#     return ...
#
# @app.route(
#     '/statistics/general/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
#     methods=['POST']
# )
# def post_statistics_general():
#     return ...
