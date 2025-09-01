import os

def load_dotenv(filename=".env"):
    with open(filename) as file:
        for line in file:
            line = line.strip()
            line = line.split("=")
            name, value = line[0].strip(), line[1].strip()

            os.environ[name] = value

