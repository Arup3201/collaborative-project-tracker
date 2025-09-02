import os

class Env:
    SECRET_KEY = os.environ['SECRET_KEY']

    DB_HOST = os.environ['DB_HOST']
    DB_USER = os.environ['DB_USER']
    DB_PORT = os.environ['DB_PORT']
    DB_PASS = os.environ['DB_PASS']
    DB_NAME = os.environ['DB_NAME']