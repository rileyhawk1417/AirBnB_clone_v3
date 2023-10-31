#!/usr/bin/python3
""" Module containing Amenity View """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity

@app_views.route('/places/<string:place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects associated with a Place
        object.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        If retrieving from db storage, a list of dictionaries representing
        Amenity objects in JSON format is returned.
        If retrieving from file storage, a list of amenity ids in JSON format
        is returned.
        404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place_obj.amenities]
    else:
        amenities = place_obj.amenity_ids
    return jsonify(amenities)

@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def unlink_amenity(place_id, amenity_id):
    """ Remove an Amenity object from a Place object.

    Args:
        place_id (str): The UUID4 string representing a Place object.
        amenity_id (str): The UUID4 string representing an Amenity object.

    Returns:
        Returns an empty dictionary with the status code 200.
        404 error if:
            `place_id` is not linked to any Place object.
            `amenity_id` is not linked to any Amenity object.
            The Amenity object associated with `amenity_id` is not linked to
            the Place object associated with `place_id`.
    """
    place_obj = storage.get("Place", place_id)
    amenity_obj = storage.get("Amenity", amenity_id

