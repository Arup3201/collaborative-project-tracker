import json
from flask import Blueprint, request, make_response

from services.auth import AuthService

from pydantic.payload import UserCreatePayload

auth_blueprint = Blueprint(__name__, "auth")

def register():
    user_data: UserCreatePayload = json.load(request.get_json())

    try:
        AuthService().register(username=user_data.username, email=user_data.email, password=user_data.password)
        return make_response({
            "message": "user created"
        }, 201)
    except:
        return make_response("SERVER_ERROR", 500)

auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, method=['POST'])