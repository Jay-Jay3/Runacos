from flask import request, jsonify
from api.schemas import userSchema, loginSchema
from services.auth_service import login_user
from services.user_svc import user_service
from flask_smorest import Blueprint
from api.middleware import require_role


blp = Blueprint("auth", "auth", description="AUTHENTICATION AND AUTHORISATION OPERATIONS")

@blp.route("/login", methods=['POST'])
@blp.arguments(loginSchema)
def login(data):
    data = request.get_json()
    email = data.get('email')
    print(email)
    password = data.get('password')
    print(password)
    result, status = login_user(email, password)

    return jsonify(result), status


@blp.route("/signup", methods=['POST'])
@blp.arguments(userSchema)
@blp.response(201, userSchema(many=True))
def post(user_data):
    result, status_code = user_service.create_user_account(user_data, False)
    return jsonify(result), status_code


@blp.route("/admin/signup", methods=['POST'])
@require_role(['admin'])
@blp.arguments(userSchema)
@blp.response(201, userSchema(many=True))
def post(user_data):
    result, status_code = user_service.create_user_account(user_data, True)
    return jsonify(result), status_code
