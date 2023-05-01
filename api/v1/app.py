#!/usr/bin/python3
"""
This module contains a simple flask application
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


db_host = getenv("HBNB_API_HOST")
db_port = getenv("HBNB_API_PORT")
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.errorhandler(404)
def error_handler(error):
    """handle 404 errors"""
    return make_response(jsonify({'error': "Not found"}), 404)


@app.teardown_appcontext
def close_db(error):
    """handle exit"""
    storage.close()


if __name__ == "__main__":
    app.run(host=db_host or "0.0.0.0", port=db_port or 5000, threaded=True, debug=True)
