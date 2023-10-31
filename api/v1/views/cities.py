#!/usr/bin/python3
""" Module containing City View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

# Base urls
# city id url
idurl = "/cities/<string:city_id>"


@app_views.route("/states/<string:state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        List of dictionaries representing City objects in JSON format.
        Raise 404 error if `state_id` is not linked to any State object.
    """
    state_obj = storage.get(State, state_id)
    cities_ = []
    if state_obj is None:
        abort(404)
    cities = storage.all(City).values()
    for sc in cities:
        if sc.state_id == state_obj.id:
            cities_.append(sc.to_dict())
    # sc: state_cities
    res = jsonify(cities_)
    return res


@app_views.route(
    "{}".format(idurl),
    methods=["GET"],
)
def get_city(city_id):
    """Retrieves a City object based on `city_id`.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Dictionary represention of a City object in JSON format.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("{}".format(idurl), methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object based on `city_id`.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns an empty dictionary with the status code 200.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>/cities", methods=["POST"])
def add_city(state_id):
    """Creates a City object using `state_id` and HTTP body request fields.

    Args:
        state_id (str): The UUID4 string representing a State object.

    Returns:
        Returns the new City object as a  dictionary in JSON format
        with the status code 200.
        Raise 404 error if `state_id` is not linked to any State object.
    """
    state_obj = storage.get(State, state_id)
    req_json = request.get_json()
    if state_obj is None:
        abort(404)
    if req_json is None:
        return "Not a JSON", 400
    if req_json.get("name") is None:
        return "Missing name", 400
    req_json["state_id"] = state_id
    new_city = City(**req_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("{}".format(idurl), methods=["PUT"])
def edit_city(city_id):
    """Edit a City object using `city_id` and HTTP body request fields.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns the City object as a  dictionary in JSON format with the
        status code 200.
        Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key in ["id", "state_id", "created_at", "update_at"]:
            continue
        if hasattr(city_obj, key):
            setattr(city_obj, key, fields[key])
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
