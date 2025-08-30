import json
from flask import Blueprint, request, make_response

from services.auth import AuthService

from validation.payload import UserCreatePayload

auth_blueprint = Blueprint("auth", __name__)

def register():
    user_data = UserCreatePayload(**request.get_json())

    AuthService().register(username=user_data.username, email=user_data.email, password=user_data.password)
    return make_response({
        "message": "user created"
    }, 201)

auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, methods=['POST'])