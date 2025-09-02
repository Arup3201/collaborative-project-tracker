from flask import Blueprint, request, make_response, jsonify
import pydantic

from services.auth import AuthService
from utils.token import generate_token, TOKEN_NAME, TOKEN_EXIRES
from validation.payload import UserCreatePayload, UserLoginPayload
from exceptions import BadPayloadError, DBOverloadError, NotFoundError, AlreadyExistError
from exceptions.auth import IncorrectPasswordError, JWTError

auth_blueprint = Blueprint("auth", __name__)

def register():
    try:
        user_data = UserCreatePayload(**request.get_json())
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })

        return jsonify({
            "error": {
                "message": "Input validation failed",
                "details": "Please make sure your input has required fields with their correct type",  
                "errors": errors, 
                "code": "INVALID_INPUT"
            }
        }), 422
    
    if not user_data.username:
        return jsonify({
            "error": {
                "message": "Invalid value in the input field",
                "details": "Field 'username' can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400
    if not user_data.email:
        return jsonify({
            "error": {
                "message": "Invalid value in the input field",
                "details": "Field 'email' can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400
    if not user_data.password:
        return jsonify({
            "error": {
                "message": "Invalid value in the input field",
                "details": "Field 'password' can't be empty",  
                "code": "BAD_REQUEST"
            }
        }), 400
    
    try:
        user_id = AuthService().register(username=user_data.username, email=user_data.email, password=user_data.password)
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201
    except BadPayloadError as e:
        return jsonify({
            "error": {
                "message": "Invalid input value",
                "details": str(e),  
                "code": "BAD_REQUEST"
            }
        }), 400
    except AlreadyExistError as e:
        return jsonify({
            "error": {
                "message": "User already exists",
                "details": str(e),  
                "code": "BAD_REQUEST"
            }
        }), 409
    except DBOverloadError as e:
        print(str(e))
        return jsonify({
            "message": "Database failed", 
            "details": "There are too many requests, please try again later", 
            "code": "DB_FAILURE"
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "message": "Server failed to process the request", 
            "details": "Something bad happened in the server, please try again later", 
            "code": "SERVER_FAILURE"
        }), 500

def login():
    try:
        user_data = UserLoginPayload(**request.get_json())
    except pydantic.ValidationError as e:
        errors = []
        for err in e.errors():
            errors.append({
                "message": err["msg"], 
                "input": err["input"], 
                "loc": err["loc"]
            })

        return jsonify({
            "error": {
                "message": "Input validation failed",
                "details": "Please make sure your input has required fields with their correct type",  
                "errors": errors, 
                "code": "INVALID_INPUT"
            }
        }), 422

    try:
        user = AuthService().login(email=user_data.email, password=user_data.password)
        response = make_response({
            "user": user
        })
        jwt_token = generate_token(user)
        response.set_cookie(TOKEN_NAME, jwt_token, expires=TOKEN_EXIRES, httponly=True, secure=True)
        return response
    except NotFoundError as e:
        return jsonify({
            "error": {
                "message": "Value not found",
                "details": str(e),  
                "code": "NOT_FOUND"
            }
        }), 404
    except IncorrectPasswordError as e:
        return jsonify({
            "error": {
                "message": "Password is incorrect",
                "details": str(e),  
                "code": "WRONG_PASSWORD"
            }
        }), 400
    except JWTError as e:
        return jsonify({
            "error": {
                "message": "Failed to create JWT token",
                "details": str(e),  
                "code": "TOKEN_ERROR"
            }
        }), 500
    except Exception as e:
        print(str(e))
        return jsonify({
            "message": "Server failed to process the request", 
            "details": "Something bad happened in the server, please try again later", 
            "code": "SERVER_FAILURE"
        }), 500

auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, methods=['POST'])
auth_blueprint.add_url_rule("/login", endpoint="login", view_func=login, methods=['POST'])