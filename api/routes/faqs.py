from flask.views import MethodView
from api.middleware import require_auth
from flask_smorest import Blueprint
from api.schemas import FaqsSchema
from flask import request
from services.faqs_svc import faqs_service

blp = Blueprint("faqs", "faqs", description="faqs operations")

@require_auth
@blp.route("/faqs")
@blp.response(200)
def get():
    data = faqs_service.get_all()
    return data

@require_auth
@blp.route("/faqs", methods=["POST"])    
@blp.arguments(FaqsSchema)
@blp.response(201, FaqsSchema(many=True))
def post(post_data):
    print("This is the data passed into the function ",post_data)
    faqs_data = faqs_service.create(post_data)
    return faqs_data

@require_auth
@blp.route("/faqs/<id>", methods=["PATCH"])
@blp.response(201)
def patch(id):
    data = request.get_json()
    if not data:
        return {"error": "No data was provided"}, 400
    allowed_fields = ['content', 'title']
    updates = {key: value for key, value in data.items() if key in allowed_fields}
    if not updates:
        return {"error": "No valid fields provided for update"}, 400
    message = faqs_service.to_update(updates, id)
    return message

@require_auth
@blp.route("/faqs/<id>", methods=["DELETE"])
@blp.response(201)
def delete(id):
    if(id):
        message = faqs_service.delete(id)
        return message
    else:
        return {"error": "No ID was provided"}
    
@require_auth
@blp.route("/faqs/",  methods=["GET"])
@blp.response(200)
def get(paramet):
    filters = {
        "content":paramet.get("courseCode"),
        "title":paramet.get("title")
    }

    active_filters = {key: value for key, value in filters.items() if value is not None}
    
    message = faqs_service.to_update(active_filters)
    return message


@blp.response(200)
@blp.route("/faqs/<id>")
def get(id):
    return faqs_service.get_by_id(id)