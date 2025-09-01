import json
from flask import Blueprint, request, make_response

from services.auth import AuthService
from utils.token import generate_token, TOKEN_EXIRES

from validation.payload import UserCreatePayload, UserLoginPayload

auth_blueprint = Blueprint(__name__, "auth")

def register():
    user_data: UserCreatePayload = request.get_json()

    try:
        AuthService().register(username=user_data.username, email=user_data.email, password=user_data.password)
        return make_response({
            "message": "user created"
        }, 201)
    except:
        return make_response("SERVER_ERROR", 500)

def login():
    user_data: UserLoginPayload = request.get_json()

    try:
        user = AuthService().login(email=user_data.email, password=user_data.password)
        response = make_response({
            "message": "login success", 
            "data": user
        })
        jwt_token, err = generate_token(user)
        if err:
            return make_response("SERVER_ERROR", 400)
        
        response.set_cookie("COLLAB_TOKEN", jwt_token, expires=TOKEN_EXIRES)
        return response
    except:
        return make_response("SERVER_ERROR", 500)

auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, method=['POST'])
auth_blueprint.add_url_rule("/login", endpoint="login", view_func=login, method=['POST'])