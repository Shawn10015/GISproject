from flask import Blueprint, jsonify
from app.models import Info
from flasgger import swag_from

info_bp = Blueprint('info', __name__)

@info_bp.route('/info/<int:adcode>', methods=['GET'])
@swag_from('get_info.yml')
def get_info(adcode):
    info = Info.query.get(adcode)
    if info:
        return jsonify(info.to_dict())
    else:
        return jsonify({"error": "Info not found"}), 404
