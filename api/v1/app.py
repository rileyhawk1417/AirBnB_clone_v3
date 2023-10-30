#!/usr/bin/python3

from flask import Flask
from api.v1.views import app_views as blueprint_views

app = Flask(__name__)
app.register_blueprint(blueprint_views)

if __name__ == "__main__":
    app.run()
