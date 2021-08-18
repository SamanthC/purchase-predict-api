import jwt

from flask import request
from datetime import datetime, timedelta

JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

def decode_token(token):
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms="HS256"
        )
    except Exception:
        print("Jeton JWT invalide.")
        return

def generate_token():
    return jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "user": "blentie"
        },
        JWT_SECRET,
        algorithm="HS256"
    )
    
def require_authentication(f):
    def wrapper(**kwargs):
        token = request.headers.get("Authorization", "0")
        if not decode_token(token):
            return {"error": "Jeton d'accès invalide."}, 403
        return f(**kwargs)
    return wrapper
