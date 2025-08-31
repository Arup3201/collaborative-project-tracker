import json, datetime
from flask import Blueprint, request, make_response

from services.auth import AuthService

from validation.payload import UserCreatePayload, UserLoginPayload

auth_blueprint = Blueprint("auth", __name__)

def register():
    user_data = UserCreatePayload(**request.get_json())

    AuthService().register(username=user_data.username, email=user_data.email, password=user_data.password)
    return make_response({
        "message": "user created"
    }, 201)

def login():
    user_data = UserLoginPayload(**request.get_json())

    try:
        user = AuthService().login(email=user_data.email, password=user_data.password)
        response = make_response({
            "data": user
        }, 200)
        response.set_cookie("auth_token", "secret", 
                            expires=datetime.datetime.now()+datetime.timedelta(seconds=30), 
                            secure=True, 
                            httponly=True)
        return response
    except Exception as e:
        return make_response({
            "message": "SERVER_ERROR", 
            "details": str(e)
        }, 500)

auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, methods=['POST'])
auth_blueprint.add_url_rule("/login", endpoint="login", view_func=login, methods=['POST'])