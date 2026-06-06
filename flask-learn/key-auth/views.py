from flask import Blueprint, make_response, request


bp = Blueprint("views", __name__)

api_keys = {
    "123456": "Application A",
    "abcdef": "Application B",
}

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or not api_key in api_keys:
            return make_response({"message": "Unauthorized"}, 401)
        
        return f(*args, **kwargs)
    return decorated_function


@bp.route("/public")
def public_route():
    return make_response({"message": "No API key is needed"}, 200)


@bp.route("/private")
@require_api_key
def private_route():
    return make_response({"message": "Valid API key is provided"}, 200)