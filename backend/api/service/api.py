from flask import Flask,jsonify


app = Flask(__name__)

# GET METHODS -------------------------------------------------------------------------------
@app.route('/coordinates/<str:city_name>', methods=["GET"])
def get_coordinates(city_name: str):
    return ...

# POST METHODS ------------------------------------------------------------------------------
@app.route(
    '/statistics/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
    methods=['POST']
)
def post_statistics():
    return ...

@app.route(
    '/statistics/weather/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
    methods=['POST']
)
def post_statistics_weather():
    return ...

@app.route(
    '/statistics/precipitation/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
    methods=['POST']
)
def post_statistics_precipitation():
    return ...

@app.route(
    '/statistics/general/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>',
    methods=['POST']
)
def post_statistics_general():
    return ...
