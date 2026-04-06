from flask.views import MethodView
from api.middleware import require_auth
from flask_smorest import Blueprint
from api.schemas import MentorshipSchema
from flask import request
from services.mentorship_svc import mentorship_service

blp = Blueprint("mentorships", "mentorships", description="mentorships operations")



@require_auth
@blp.route("/mentorship")
@blp.response(200)
def get():
    data = mentorship_service.get_all()
    return data

@require_auth
@blp.route("/mentorship", methods=["POST"])    
@blp.arguments(MentorshipSchema)
@blp.response(201, MentorshipSchema(many=True))
def post(post_data):
    print("This is the data passed into the function ",post_data)
    faqs_data = mentorship_service.create(post_data)
    return faqs_data

@require_auth
@blp.route("/mentorship/<id>", methods=["PATCH"])
@blp.response(201)
def patch(id):
    data = request.get_json()
    if not data:
        return {"error": "No data was provided"}, 400
    allowed_fields = ['alumniId','message']
    updates = {key: value for key, value in data.items() if key in allowed_fields}
    if not updates:
        return {"error": "No valid fields provided for update"}, 400
    message = mentorship_service.to_update(updates, id)
    return message

@require_auth
@blp.route("/mentorship/<id>", methods=["DELETE"])
@blp.response(201)
def delete(id):
    if(id):
        message = mentorship_service.delete(id)
        return message
    else:
        return {"error": "No ID was provided"}
    
@require_auth
@blp.route("/mentorship/",  methods=["GET"])
@blp.response(200)
def get(paramet):
    filters = {
        "content":paramet.get("courseCode"),
        "title":paramet.get("title")
    }

    active_filters = {key: value for key, value in filters.items() if value is not None}
    
    message = mentorship_service.to_update(active_filters)
    return message


@blp.response(200)
@blp.route("/mentorship/<id>")
def get(id):
    return mentorship_service.get_by_id(id)



# @require_auth
# @blp.route("/mentorships")
# @blp.response(200, MentorshipSchema)
# def get(self):
#     data = mentorship_service.get_all()
#     return data

# @require_auth
# @blp.route("/mentorships", methods=["POST"])
# @blp.response(201)
# def post(self, post_data):
#     if 'file' not in request.files:
#         return {"message": "No file part"}, 400
    
#     mentorships_data = mentorship_service.create(post_data)
#     return mentorships_data

# @require_auth
# @blp.route("/mentorships", methods=["PATCH"])
# @blp.response(201)
# def patch(self, doc_id):
#     data = request.get_json()
#     if not data:
#         return {"error": "No data was provided"}, 400
#     allowed_fields = ['description', 'response', 'title', 'status']
#     updates = {key: value for key, value in data.items() if key in allowed_fields}
#     if not updates:
#         return {"error": "No valid fields provided for update"}, 400
#     message = mentorship_service.to_update(updates, doc_id)
#     return message

# @require_auth
# @blp.route("/mentorships/<id>", methods=["DELETE"])
# @blp.response(201)
# def delete(self, doc_id):
#     doc_id = request.args.get()
#     if(doc_id):
#         message = mentorship_service.delete(doc_id)
#         return message
#     else:
#         return {"error": "No ID was provided"}
