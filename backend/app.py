from flask import Flask

from env import load_dotenv
load_dotenv()

from middlewares.authorize import Authorize
from routes.auth import auth_blueprint
from routes.projects import projects_blueprint

app = Flask(__name__)
app.wsgi_app = Authorize(app.wsgi_app)

app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
app.register_blueprint(projects_blueprint, url_prefix="/api/v1/projects")

if __name__=='__main__':
    app.run(port=8000, debug=True)