import os

def load_dotenv():
    with open(".env") as file:
        for line in file:
            line = line.strip()
            line = line.split("=")
            name, value = line[0].strip(), line[1].strip()

            os.environ[name] = value

