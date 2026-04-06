from services.resource_svc import resource_service
from flask.views import MethodView
from api.middleware import require_auth, require_role
from flask_smorest import Blueprint
from api.schemas import ResourcesSchema, ImagesResourcesSchema
from flask import request
from services.imagekit_svc import imageKit_service
from google.cloud.firestore_v1.field_path import FieldPath

blp = Blueprint("resources", "resources", description="Resources Operations")

@blp.route("/resources")
class ResourcesProfile(MethodView):
    @blp.response(200)
    def get(self):
        data = resource_service.get_all()
        return data


    # @blp.route("/resources/create", methods=['POST'])
    # @require_auth
    @blp.arguments(ResourcesSchema, location="form")
    @blp.arguments(ImagesResourcesSchema, location="files")
    @require_role(['admin'])
    def post(self, data, file):
        print("THIS IS THE POST METHOD!!!!!!!!!!!!!!!!!1")
        print(data)
        print(file)
        if not file:
            return {"message": "No file"}, 400
        print("validated successfully")
        fileUrl = resource_service.create_with_Image(file['file'])
        title = data['title'].replace(" ","").lower()
        data = {**data, "fileUrl": fileUrl, "title": title}
        posted_data = resource_service.create(data)
        return posted_data


    @blp.route("/resources/<id>", methods=["PATCH"])
    @require_role(['admin'])
    @blp.response(201)
    def patch(doc_id):
        data = request.get_json()
        if not data:
            return {"error": "No data was provided"}, 400
        allowed_fields = ['authorId', 'authorName', 'content', 'title']
        updates = {key: value for key, value in data.items() if key in allowed_fields}
        if not updates:
            return {"error": "No valid fields provided for update"}, 400
        title = updates['title'].replace(" ","").lower()
        updates = {**updates, "title": title}
        message = resource_service.to_update(updates, doc_id)
        return message
    
    @blp.route("/resources/<id>", methods=["DELETE"])
    @require_role(['admin'])
    @blp.response(201)
    def delete(self, id):
        doc_id = request.args.get()
        if(id):
            message = resource_service.delete(id)
            return message
        else:
            return {"error": "No ID was provided"}

    
@blp.response(200)
@blp.route("/resources/", methods=["GET"])
def get():
    paramet = request.args
    filters = {
        "courseCode":paramet.get("courseCode", "").strip(),
        "title":paramet.get("title", "").strip(),
        "type":paramet.get("type", "").strip(),
        "uploadedBy":paramet.get("uploadedBy", "").strip()
    }

    active_filters = {key: value for key, value in filters.items() if value and str(value).strip()}
    print(active_filters)
    return resource_service.search(active_filters)


@blp.response(200)
@blp.route("/resources/<id>")
def get(id):
    resource = resource_service.get_by_id(id)
    title = resource['title'].upper()
    resource = {**resource, 'title': title}
    return resource




