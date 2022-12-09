#!/usr/bin/python3
"""route /places"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_city_id(city_id):
    """Method that retrieve a list of all places by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Method that retrieve a list of all places by id"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)

    return (jsonify(place.to_dict()))


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Method that delete a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Method that post a new place by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data_place = request.get_json()
    if type(data_place) != dict:
        abort(400, description="Not a JSON")
    if not data_place.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, data_place.get("user_id"))
    if user is None:
        abort(404)
    if not data_place.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**data_place)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """This method update city by id"""
    current_place = storage.get(Place, place_id)
    if (current_place is None):
        abort(404)

    update_place = request.get_json(silent=True)
    if (type(update_place) is dict):
        update_place.pop('id', None)
        update_place.pop('created_at', None)
        update_place.pop('updated_at', None)

        for key, value in update_place.items():
            setattr(current_place, key, value)
        current_place.save()
        return (jsonify(current_place.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
