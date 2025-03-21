from flask import Blueprint, jsonify
from models.user import User

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    return jsonify(["test","test1","test2","test3","test4","test5"])