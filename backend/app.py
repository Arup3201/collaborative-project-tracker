from flask import Flask

from env import load_dotenv
load_dotenv()

app = Flask(__name__)

if __name__=='__main__':
    app.run(port=8000)