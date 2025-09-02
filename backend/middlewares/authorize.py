import json
from werkzeug.wrappers import Request, Response, ResponseStream

from utils.token import validate_token

class Authorize:
    """
        Middleware to authorize users by verifying the tokens
    """

    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        public_apis = ["/auth/register", "/auth/login"]

        if any([api in request.url for api in public_apis]):
            return self.app(environ, start_response)
        
        token = request.cookies.get("COLLAB_TOKEN", None)
        if not token:
            res = Response(json.dumps({
                "message": "Authorization failed", 
                "details": "No valid token found in the request cookie", 
                "code": 401
            }), mimetype= 'application/json', status=401)
            return res(environ, start_response)
        
        payload, err = validate_token(token)
        if err:
            res = Response(json.dumps({
                "message": "Authorization failed", 
                "details": err, 
                "code": 401
            }), mimetype= 'application/json', status=401)
            return res(environ, start_response)
        
        environ["user"] = payload
        return self.app(environ, start_response)
        