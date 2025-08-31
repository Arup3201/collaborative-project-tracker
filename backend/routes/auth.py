from keycloak import KeycloakOpenID
from flask import Blueprint, redirect, request, jsonify

from services.auth import AuthService
from config import Env

from validation.payload import UserCreatePayload, UserLoginPayload

auth_blueprint = Blueprint("auth", __name__)

# Keycloak Configuration
KEYCLOAK_SERVER_URL = "http://localhost:8080/"
KEYCLOAK_REALM = "collab"
KEYCLOAK_CLIENT_ID = "arup"
KEYCLOAK_CLIENT_SECRET = Env.SECRET_KEY
REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback"


# Configure client
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_SERVER_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    try:
        token = keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=REDIRECT_URI
        )
        return token
    except Exception as e:
        print(f"Token exchange error: {e}")
        return None

def verify_token(token):
    """Verify and decode access token"""
    try:
        # Introspect token to check if it's valid
        token_info = keycloak_openid.introspect(token)
        if token_info.get('active'):
            # Get user info
            userinfo = keycloak_openid.userinfo(token)
            return userinfo
        return None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def login():
    auth_url = keycloak_openid.auth_url(redirect_uri=REDIRECT_URI,
                                        scope="email",
                                        state="your_state_info")
    
    return redirect(auth_url)

def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        return jsonify({'error': f'Authorization failed: {error}'}), 400
    
    if not code:
        return jsonify({'error': 'Authorization code not provided'}), 400
    
    # Exchange code for token
    token_data = exchange_code_for_token(code)
    if not token_data:
        return jsonify({'error': 'Failed to exchange code for token'}), 400
    
    # Get user info
    access_token = token_data['access_token']
    user_info = verify_token(access_token)
    
    if user_info:
        return jsonify({
            'message': 'Login successful',
            'user': user_info,
            'token': access_token,
            'expires_in': token_data.get('expires_in')
        })
    else:
        return jsonify({'error': 'Failed to get user information'}), 400


auth_blueprint.add_url_rule("/login", endpoint="login", view_func=login, methods=['POST'])
auth_blueprint.add_url_rule("/callback", endpoint="callback", view_func=callback, methods=['POST'])