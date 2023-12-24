from flask import Blueprint, jsonify
from app.models import Province
from flasgger import swag_from

province_bp = Blueprint('province', __name__)

@province_bp.route('/provinces', methods=['GET'])
@swag_from('get_provinces.yml')
def get_provinces():
    provinces = Province.query.all()
    return jsonify([province.to_dict() for province in provinces])

@province_bp.route('/province/<int:adcode>', methods=['GET'])
@swag_from('get_province.yml')
def get_province(adcode):
    province = Province.query.get(adcode)
    if province:
        return jsonify(province.to_dict())
    else:
        return jsonify({"error": "Province not found"}), 404