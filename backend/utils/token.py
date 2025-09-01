import jwt
from datetime import datetime, timedelta, timezone

from config import Env

TOKEN_EXIRES = datetime.now(tz=timezone.utc)+timedelta(minutes=30)

def generate_token(payload: dict) -> tuple[str, str|None]:
    try:
        token = jwt.encode(payload={
            **payload, 
            "exp": TOKEN_EXIRES, 
            }, key=Env.SECRET_KEY, algorithm="HS256")
        return token, None
    except jwt.exceptions.InvalidKeyError:
        return "", "encoding key is invalid"
    except Exception as e:
        print(str(e))
        return "", "unknown error while encoding jwt token"

def validate_token(token: str) -> tuple[dict, str|None]:
    try:
        payload = jwt.decode(jwt=token, key=Env.SECRET_KEY, algorithms="HS256")
        return payload, None
    except jwt.exceptions.ExpiredSignatureError:
        return dict(), "jwt token signature expired"
    except jwt.exceptions.InvalidSignatureError:
        return dict(), "jwt token signature invalid"
    except jwt.exceptions.InvalidTokenError:
        return dict(), "jwt token invalid"
    except jwt.exceptions.InvalidKeyError:
        return dict(), "decoding key is invalid"
    except Exception:
        return dict(), "unknown error while decoding jwt token"