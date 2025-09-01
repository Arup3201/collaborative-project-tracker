import json
from werkzeug.wrappers import Request, Response, ResponseStream

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
        if token:
            print(token)
            return self.app(environ, start_response)

        res = Response(json.dumps({
            "message": "Authorization failed", 
            "details": "No valid token found in the request cookie", 
            "code": 401
        }), mimetype= 'application/json', status=401)
        return res(environ, start_response)