import bcrypt
import jwt

from datetime import datetime, timedelta

from config import SECRET_KEY


def hash_password(password):

    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode('utf-8')


def verify_password(password, hashed_password):

    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def generate_token(user_data):

    payload = {
        "id_usuario": user_data["id_usuario"],
        "usuario": user_data["usuario"],
        "roles": user_data["roles"],
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None