from flask import Blueprint, jsonify
from app.models import Scenic_spots
from flasgger import swag_from

scenic_spots_bp = Blueprint('scenic_spots_bp', __name__)

@scenic_spots_bp.route('/all_scenic_spots', methods=['GET'])
@swag_from('get_scenics.yml')
def get_all_scenics():
    scenic_spots = Scenic_spots.query.all()
    return jsonify([scenic_spots.to_dict() for scenic_spots in scenic_spots])

@scenic_spots_bp.route('/scenic/id/<int:id>', methods=['GET'])
@swag_from('get_scenic.yml')
def get_scenic_id(id):
    scenic_spots = Scenic_spots.query.get(id)
    if scenic_spots:
        return jsonify(scenic_spots.to_dict())
    else:
        return jsonify({"error": "City not found"}), 404

@scenic_spots_bp.route('/scenic/adcode/<int:adcode>', methods=['GET'])
@swag_from('get_scenic_by_adcode.yml')
def get_scenic_adcode(adcode):
    scenic_spots = Scenic_spots.query.get(adcode)
    if scenic_spots:
        return jsonify(scenic_spots.to_dict())
    else:
        return jsonify({"error": "City not found"}), 404