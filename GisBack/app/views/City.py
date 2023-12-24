from flask import Blueprint, jsonify
from app.models import City
from flasgger import swag_from

city_bp = Blueprint('city', __name__)

@city_bp.route('/cities', methods=['GET'])
@swag_from('get_cities.yml')
def get_cities():
    cities = City.query.all()
    return jsonify([city.to_dict() for city in cities])

@city_bp.route('/city/<int:adcode>', methods=['GET'])
@swag_from('get_city.yml')
def get_city(adcode):
    city = City.query.get(adcode)
    if city:
        return jsonify(city.to_dict())
    else:
        return jsonify({"error": "City not found"}), 404
