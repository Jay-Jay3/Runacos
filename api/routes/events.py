from flask.views import MethodView
from api.middleware import require_auth, require_role
from flask_smorest import Blueprint
from api.schemas import EventSchema, postEventSchema, ImagesSchema
from flask import request
from services.event_svc import events_service

blp = Blueprint("events", "events", description="events operations")


@require_auth
@blp.route("/events")
@blp.response(200)
def get():
    data = events_service.get_all()
    return data

@blp.route("/events", methods=["POST"])    
@require_role(['admin'])
@blp.arguments(postEventSchema, location="form")
@blp.arguments(ImagesSchema, location="files")
@blp.response(201)
def post(post_data, post_file):
    print("This is the data passed into the function ",post_data)
    if post_file is not None:
        fileUrl = events_service.create_with_Image(post_file["file"])
        post_data = {**post_data, "fileUrl": fileUrl}
    # post_data.pop("file", None)
    events_data = events_service.create(post_data)
    return events_data 

@require_role(["admin"])
@blp.route("/events/<id>", methods=["PATCH"])
@blp.response(201)
def patch(id):
    data = request.get_json()
    if not data:
        return {"error": "No data was provided"}, 400
    allowed_fields = ['description', 'eventType', 'title', 'eventTime', 'date', 'response']
    updates = {key: value for key, value in data.items() if key in allowed_fields}
    if not updates:
        return {"error": "No valid fields provided for update"}, 400
    message = events_service.to_update(updates, id)
    return message

@require_role(["admin"])
@blp.route("/events/<id>", methods=["DELETE"])
@blp.response(201)
def delete(id):
    if(id):
        message = events_service.delete(id)
        return message
    else:
        return {"error": "No ID was provided"}
    
@require_auth
@blp.route("/events/",  methods=["GET"])
@blp.response(200)
def get(paramet):
    filters = {
        "content":paramet.get("courseCode"),
        "title":paramet.get("title")
    }
    active_filters = {key: value for key, value in filters.items() if value is not None}
    
    message = events_service.to_update(active_filters)
    return message


@blp.response(200)
@blp.route("/events/<id>")
def get(id):
    return events_service.get_by_id(id)


# @require_auth
# @blp.route("/events")
# @blp.response(200, EventSchema)
# def get(self):
#     data = events_service.get_all()
#     return data

# @require_auth
# @blp.route("/events", methods=["POST"])
# @blp.response(201)
# def post(self, post_data):
#     if 'file' not in request.files:
#         return {"message": "No file part"}, 400
    
#     events_data = events_service.create(post_data)
#     return events_data

# @require_auth
# @blp.route("/events", methods=["PATCH"])
# @blp.response(201)
# def patch(self, doc_id):
#     data = request.get_json()
#     if not data:
#         return {"error": "No data was provided"}, 400
#     allowed_fields = ['description', 'type', 'title', 'eventTime', 'date']
#     updates = {key: value for key, value in data.items() if key in allowed_fields}
#     if not updates:
#         return {"error": "No valid fields provided for update"}, 400
#     message = events_service.to_update(updates, doc_id)
#     return message

# @require_auth
# @blp.route("/events/<id>", methods=["DELETE"])
# @blp.response(201)
# def delete(self, doc_id):
#     doc_id = request.args.get()
#     if(doc_id):
#         message = events_service.delete(doc_id)
#         return message
#     else:
#         return {"error": "No ID was provided"}
