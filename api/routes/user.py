from services.user_svc import user_service
from flask.views import MethodView
from api.middleware import require_role
from flask_smorest import Blueprint
from api.schemas import userSchema, ResourcesSchema, loginSchema
from flask import request, jsonify
from services.imagekit_svc import imageKit_service
from services.resource_svc import resource_service
from services.auth_service import login_user
import requests
from firebase_admin import auth, firestore


blp = Blueprint("user", "user", description="User operations")


@blp.route("/user")
class UserProfile(MethodView):
    @require_role(['admin'])
    @blp.response(200)
    def get(self):
        data = user_service.get_all()
        return data
    
    # @require_role(['admin'])
    @blp.arguments(userSchema)
    @blp.response(201, userSchema(many=True))
    def post(self, data):
        # user_data = request.get_json()
        result, status_code = user_service.create_user_account(data)
        return jsonify(result), status_code
    
@blp.route("/user/<id>", methods=['PATCH'])
@require_role(['admin'])
def patch(id):
    data = request.get_json()
    if not data:
        return {"error": "No data was provided"}, 400
    allowed_fields = ['username', 'department', 'currentCompany', 'graduationYear', 'jobTitle']
    updates = {key: value for key, value in data.items() if key in allowed_fields}
    if not updates:
        return {"error": "No valid fields provided for update"}, 400
    message = user_service.to_update(updates, id)
    return message

@blp.route("/user/promote", methods=['PATCH'])
@require_role(['admin'])
def patch():
    data = request.get_json()
    if data['role'] and data['email'] is None:
        return {"error": "No data passed"}
    result = user_service.to_promote(data)
    return result

@blp.route("/user/<id>", methods=['DELETE'])
@require_role(['admin'])
def delete(id):
    if(id):
        auth.delete_user(id)
        message = user_service.delete(id)
        return message
    else:
        return {"error": "No ID was provided"}


@blp.route("/user/<email>", methods=['DELETE'])
@require_role(['admin'])
def delete(email):
    if(email):
        auth.delete_user(email)
        user_id = user_service.get_id_from_user(email)
        message = user_service.delete(user_id)
        return message
    else:
        return {"error": "No ID was provided"}


    
# @blp.route("/user/resource")
# @blp.response(200)
# def getResources():
#     data = resource_service.get_all()
#     return data


@blp.route("/user/resource/")
@blp.response(200)
def getResource():
    filters = {
        "courseCode": request.args.get("courseCode"),
        "title": request.args.get("title"),
        "type": request.args.get("type") }
    active_filters = {k: v for k, v in filters.items() if v is not None}
    return resource_service.search(active_filters)



@blp.response(200)
@blp.route("/user/<id>")
def get(id):
    return user_service.get_by_id(id)
