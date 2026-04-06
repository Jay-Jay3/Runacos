from services.subscribe_svc import subscribe_service
from flask.views import MethodView
from flask_smorest import Blueprint
from api.schemas import SubscribersEmail
from services.imagekit_svc import imageKit_service
from google.cloud.firestore_v1.field_path import FieldPath

blp = Blueprint("subscribe", "subscribe", description="Subscribe Operations")

@blp.route("/subscribe")
class SubscribeProfile(MethodView):    
    @blp.response(200)
    @blp.arguments(SubscribersEmail)
    def get(self, email):
        data = subscribe_service.getEach(email)
        return data
    
    @blp.response(201)
    @blp.arguments(SubscribersEmail)
    def post(self, email):
        data = subscribe_service.save(email)
        return data
    
    @blp.response(200)
    @blp.arguments(SubscribersEmail)
    def delete(self, email):
        data = subscribe_service.delete(email['email'])
        return data

@blp.route('/subscribe/')
@blp.response(200)
def getAll():
    data = subscribe_service.get_all()
    return data
