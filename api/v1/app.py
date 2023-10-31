#!/usr/bin/python3
"""The main app file to launch API"""
from flask import Flask, jsonify
from api.v1.views import app_views as blueprint_views
from models import storage
import os
from flask_cors import CORS
import json

app = Flask(__name__)
app.register_blueprint(blueprint_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_context(exception):
    """Close storage after use"""
    storage.close()


@app.errorhandler(Exception)
def error_page_handler(e):
    """404 Page handler"""
    error = {"error": "Not found"}
    res = jsonify(error)
    # Add new line per dump
    res.data = json.dumps(error, indent=2) + "\n"
    res.content_type = "application/json"
    res.status_code = 404
    return res


# Setup vars
api_host = "HBNB_API_HOST"
api_port = "HBNB_API_PORT"
if __name__ == "__main__":
    if api_host in os.environ:
        host = os.environ[api_host]
    else:
        host = "0.0.0.0"
    if api_port in os.environ:
        port = int(os.environ[api_port])
    else:
        port = int("5000")

    app.run(host=host, port=port, threaded=True)
