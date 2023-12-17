from flask import Blueprint

bp = Blueprint('users', __name__)

@bp.route('/users/<username>')
def get_user(username):
    # 获取用户逻辑
    pass

@bp.route('/users', methods=['POST'])
def create_user():
    # 创建用户逻辑
    pass
