from flask import Flask,jsonify
from time import sleep

from backend.api.service.celery_config import celery as celery_app

from .db_manager.settings import DBSettings, create_db_url
from .api_funcs import *

def create_app() -> Flask:
    app = Flask(__name__)

    db_settings = DBSettings()
    db_url = create_db_url(settings=db_settings)

    def init_celery(app, celery):
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask
        return celery

    # celery_app = init_celery(app, celery_app)

    # GET METHODS -------------------------------------------------------------------------------

    @app.route('/test', methods=["GET"])
    def get_test():
        result = get_test_func()
        return jsonify(result), 200


    @app.route('/coordinates/<string:city_name>', methods=["GET"])
    def get_coordinates(city_name: str):
        try:
            coordinates = get_coordinates_func(db_url=db_url, city_name=city_name)
            if coordinates.get("error"):
                return jsonify(coordinates), 400

            return jsonify(coordinates), 200
        except Exception as e :
            return jsonify({"error": f"{city_name} coordinates unavailable. {str(e)}"}), 500


    @app.route('/get-status/<string:transaction_id>', methods=["GET"])
    def get_transaction_status(transaction_id: str):
        try:
            status = get_transaction_status_func(db_url=db_url, transaction_id=transaction_id)
            if status.get("error"):
                return jsonify(status), 400

            return jsonify(status), 200
        except Exception:
            return jsonify({"error": f"{transaction_id} status unavailable."}), 500


    @app.route('/search-results/<string:transaction_id>', methods=["GET"])
    def search_results(transaction_id: str):
        try:
            results = search_results_func(db_url=db_url, transaction_id=transaction_id)
            if results.get("error"):
                return jsonify(results), 400
            return jsonify(results), 200

        except Exception:
            return jsonify({"error": f"{transaction_id} results unavailable."}), 500

    @app.route(
        '/city-stats/<string:city_name>/<string:start_date>/<string:end_date>',
        methods=['GET']
    )
    def get_city_stats(
            city_name: str,
            start_date: str,
            end_date: str
    ):
        try:
            city_stats = get_city_stats_func(
                db_url=db_url,
                city_name=city_name,
                start_date=start_date,
                end_date=end_date,
            )

            if city_stats.get("error"):
                return jsonify(city_stats), 400

            return jsonify(city_stats), 200

        except Exception as e :
            return jsonify({"error": f"error getting stats for {city_name} city stats. {str(e)}"}), 500


    # POST METHODS ------------------------------------------------------------------------------
    @app.route(
        '/weather-data/<string:latitude>/<string:longitude>/<string:start_date>/<string:end_date>',
        methods=['POST']
    )
    def post_weather_data(latitude: str, longitude: str, start_date: str, end_date: str):
        try:
            transaction = post_weather_data_func(
                db_url=db_url,
                latitude=latitude,
                longitude=longitude,
                start_date=start_date,
                end_date=end_date
            )

            if transaction.get("error"):
                return jsonify(transaction), 400

            return {"id_to_monitor": transaction.get("id")}, 200

        except Exception as e:
            return jsonify({"error": f"Error creating new transaction. {str(e)}"}), 500

    return app