from keycloak import KeycloakOpenID, KeycloakAdmin
from flask import Blueprint, redirect, request, jsonify

from config import Env

auth_blueprint = Blueprint("auth", __name__)

# Keycloak Configuration
KEYCLOAK_SERVER_URL = "http://localhost:8080/"
KEYCLOAK_REALM = "collab"
KEYCLOAK_CLIENT_ID = "arup"
KEYCLOAK_CLIENT_SECRET = Env.KEYCLOAK_SECRET_KEY
REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback"


# Configure client
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_SERVER_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)

# Admin client for user management
keycloak_admin = KeycloakAdmin(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    realm_name=KEYCLOAK_REALM
)


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

def register_user(username, email, password, first_name=None, last_name=None):
        """Register a new user directly through Keycloak Admin API"""
        try:
            user_data = {
                "username": username,
                "email": email,
                "enabled": True,
                "emailVerified": False,
                "firstName": first_name or "",
                "lastName": last_name or "",
                "credentials": [{
                    "type": "password",
                    "value": password,
                    "temporary": False
                }]
            }
            
            user_id = keycloak_admin.create_user(user_data)
            return {"success": True, "user_id": user_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

def register():
    """Direct user registration through Keycloak Admin API"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields: username, email, password'}), 400
    
    
    result = register_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    
    if result['success']:
        return jsonify({
            'message': 'User registered successfully',
            'user_id': result['user_id'],
            'next_step': 'Please login using /login endpoint'
        }), 201
    else:
        return jsonify({'error': f'Registration failed: {result["error"]}'}), 400

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


auth_blueprint.add_url_rule("/register", endpoint="register", view_func=register, methods=['POST'])
auth_blueprint.add_url_rule("/login", endpoint="login", view_func=login, methods=['POST'])
auth_blueprint.add_url_rule("/callback", endpoint="callback", view_func=callback, methods=['POST'])