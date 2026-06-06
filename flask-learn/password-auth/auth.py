from functools import wraps
from hashlib import sha1

from flask import Blueprint, make_response, request, Response

from db import users

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/sign_up")
def sign_up():
    username = request.json.get("username")
    password = request.json.get("password")
    error = None
    
    status_code = 204
    
    if not username:
        error, status_code = "Username is required!", 400
    elif not password:
        error, status_code = "Password is required!", 400
    elif username in users:
        error, status_code = "Username already exists!", 400
        
    if error:
        return make_response({"message": error}, status_code)
    
    users[username] = sha1(password.encode()).hexdigest()
    
    return Response(status=status_code)


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        
        if not auth:
            return make_response({"message": "Unauthorized"}, 401)
        
        username = auth.username
        password = auth.password
        
        if username not in users or sha1(password.encode()).hexdigest() != users[username]:
            return make_response({"message": "Unauthorized"}, 401)
        
        return func(*args, **kwargs)
    
    return wrapper

