import os
import json
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_smorest import Api
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)

env = os.environ.get('APP_ENV', 'development')

load_dotenv()

if os.environ.get('APP_ENV') == 'production':
    CORS(app, 
         origins=["https://runacos-nu.vercel.app"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=['GET','POST','PUT','PATCH','DELETE','OPTIONS'])
else: 
    CORS(app, origins="*")

# # Setting up the credentials for the database(Firestore)
# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# key_path = os.path.join(base_dir, 'config', 'key.json')

# if not firebase_admin._apps:
#     try:
#         if os.environ.get('APP_ENV') == 'production':
#             firebase_admin.initialize_app(options={
#                 'storageBucket': "runacos-cef4c.firebasestorage.app"
#             })
#             print("Firebase initialised with application default credentials")
#         else: 
#             with open(key_path) as f:
#                 key_data = json.load(f)
#                 key_data['private_key'] = key_data['private_key'].replace('\\n', '\n')
#                 cred = credentials.Certificate(key_data)
#                 firebase_admin.initialize_app(cred, {'storageBucket': "gs://runacos-cef4c.firebasestorage.app"})
#                 print("Firebase successfully initialised")
#     except Exception as e:
#         print(f"Failed to initialise Firebase: {e}")
# # cred = credentials.Certificate("config/keys.json")
# # firebase_admin.initialize_app()
# db = firestore.client()


# if not firebase_admin._apps:
#     try: 
#         if os.environ.get('APP_ENV') == 'production':
#             firebase_admin.initialize_app(
#                 options={
#                     'storageBucket': "runacos-cef4c.firebasestorage.app"
#                 }
#             )
#         print("firebase initialised via cloud run service account")
#     except Exception as cloud_err:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        local_key_path = os.path.join(current_dir, "..", 'config', 'keys.json')

        if os.path.exists(local_key_path):
            cred = credentials.Certificate(local_key_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    except Exception as local_err:
        print("CRITICALLITY CHAI!!!!")
        print(f"local error: {local_err}")
        raise local_err


db = firestore.client()



#configuring smorest(SWAGGER_UI)
app.config["API_TITLE"]= "RUNACOS API"
app.config["API_VERSION"]= "v1"
app.config["OPENAPI_VERSION"]= "3.0.3"
app.config["OPENAPI_URL_PREFIX"]= "/"
app.config["OPENAPI_SWAGGER_UI_PATH"]= "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"]= "https://unpkg.com/swagger-ui-dist@3.25.0/"

from api import UserBlueprint, ResourceBlueprint, FaqsBlueprint, JobsBlueprint, PostsBlueprint, EventsBlueprint, FaultsBlueprint, MentorshipBlueprint, AuthBlueprint, SubscribersBlueprint


api = Api(app)
api.register_blueprint(UserBlueprint)
api.register_blueprint(ResourceBlueprint)
api.register_blueprint(FaqsBlueprint)
api.register_blueprint(FaultsBlueprint)
api.register_blueprint(PostsBlueprint)
api.register_blueprint(EventsBlueprint)
api.register_blueprint(JobsBlueprint)
api.register_blueprint(MentorshipBlueprint)
api.register_blueprint(AuthBlueprint)
api.register_blueprint(SubscribersBlueprint)



