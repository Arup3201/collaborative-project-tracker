from flask import Flask
from middlewares.authorize import Authorize

from env import load_dotenv
load_dotenv()

from routes.auth import auth_blueprint

app = Flask(__name__)
app.wsgi_app = Authorize(app.wsgi_app)

app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")

if __name__=='__main__':
    app.run(port=8000)