import os

class Env:
    KEYCLOAK_SECRET_KEY = os.getenv('KEYCLOAK_SECRET_KEY')

    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PORT = os.getenv('DB_PORT')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')