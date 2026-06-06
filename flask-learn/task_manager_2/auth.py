from flask import Blueprint, make_response

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/sign_up")
def sign_up():
    return make_response({"message": "Not implemented"}, 501)

@bp.post("/login")
def login():
    return make_response({"message": "Not implemented"}, 501)