from flask.views import MethodView
from api.middleware import require_auth, require_role
from flask_smorest import Blueprint
from api.schemas import PostSchema, postPostSchema, ImagesSchema
from flask import request
from services.posts_svc import posts_service

blp = Blueprint("posts", "posts", description="posts operations")



@blp.route("/posts")
@blp.response(200)
def get():
    data = posts_service.get_all()
    return data

@blp.route("/posts", methods=["POST"])
@require_role(["admin"])
@blp.arguments(postPostSchema, location="form")
@blp.arguments(ImagesSchema, location="files")
def post(post_data, post_file):
    # print("This is the data passed into the function ",post_data)
    # faqs_data = posts_service.create(post_data)
    # return faqs_data
    print("This is the data passed into the function ",post_file)
    if post_file['file'] is not None:
        fileUrl = posts_service.create_with_Image(post_file["file"])
        post_data = {**post_data, "fileUrl": fileUrl}
    # post_data.pop("file", None)
    posts_data = posts_service.create(post_data)
    return posts_data 

@blp.route("/posts/<id>", methods=["PATCH"])
@require_role(['admin'])
@blp.response(201)
def patch(id):
    data = request.get_json()
    if not data:
        return {"error": "No data was provided"}, 400
    allowed_fields = ['title', 'content']
    updates = {key: value for key, value in data.items() if key in allowed_fields}
    if not updates:
        return {"error": "No valid fields provided for update"}, 400
    message = posts_service.to_update(updates, id)
    return message

@require_auth
@blp.route("/posts/<id>", methods=["DELETE"])
@blp.response(201)
def delete(id):
    if(id):
        message = posts_service.delete(id)
        return message
    else:
        return {"error": "No ID was provided"}
    
@require_auth
@blp.route("/posts/",  methods=["GET"])
@blp.response(200)
def get(paramet):
    filters = {
        "content":paramet.get("courseCode"),
        "title":paramet.get("title")
    }

    active_filters = {key: value for key, value in filters.items() if value is not None}
    
    message = posts_service.to_update(active_filters)
    return message


@blp.response(200)
@blp.route("/posts/<id>")
def get(id):
    return posts_service.get_by_id(id)




# @require_auth
# @blp.route("/posts")
# @blp.response(200)
# def get():
#     data = posts_service.get_all()
#     return data

# @require_auth
# @blp.route("/posts", methods=["POST"])
# @blp.response(201)
# def post(post_data):
#     if 'file' not in request.files:
#         return {"message": "No file part"}, 400
    
#     posts_data = posts_service.create(post_data)

#     return posts_data

# @require_auth
# @blp.route("/posts", methods=["PATCH"])
# @blp.response(201)
# def patch(doc_id):
#     data = request.get_json()
#     if not data:
#         return {"error": "No data was provided"}, 400
#     allowed_fields = ['authorId', 'authorName', 'content', 'title']
#     updates = {key: value for key, value in data.items() if key in allowed_fields}
#     if not updates:
#         return {"error": "No valid fields provided for update"}, 400
#     message = posts_service.to_update(updates, doc_id)
#     return message

# @require_auth
# @blp.route("/posts/<id>", methods=["DELETE"])
# @blp.response(201)
# def delete(doc_id):
#     doc_id = request.args.get()
#     if(doc_id):
#         message = posts_service.delete(doc_id)
#         return message
#     else:
#         return {"error": "No ID was provided"}
