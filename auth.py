import jwt
from flask import request
from db import get_db

SECRET = "invoicehub-secret"

def generate_token(user):
    payload = {
        "user_id": user["id"],
        "role": user["role"],
        "org_id": user["org_id"]
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def get_current_user():
    token = request.headers.get("Authorization")
    if not token:
        return None

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (decoded["user_id"],)
    ).fetchone()

    return user
