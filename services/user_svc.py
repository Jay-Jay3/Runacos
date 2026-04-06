from .base_svc import BaseServiceClass
from firebase_admin import auth, firestore
from flask import abort
from google.cloud.firestore_v1.base_query import FieldFilter

class UserServiceClass(BaseServiceClass):
    def __init__(self):
        super().__init__("users")

    # def get_user_by_id(self, user_id):
    #     docs = self.collection.where()
    #     return ""

    def create_user_account(self, data, authorised):
        valid_roles = ['student', 'alumni', 'admin']
        if data['role'].strip() not in valid_roles:
            return {
                "success": False,
                "error": f"Invalid role. Must be one of {valid_roles}"
            }, 400
        if data['role'] == 'admin' and not authorised:
            data['role'] = 'student'
        
        try:
            user_resord = auth.create_user(
                email= data['email'],
                password= data['password']
                )
            uid = user_resord.uid

            auth.set_custom_user_claims(uid, {'role': data['role']})

            user_data = {
                'username': data['username'],
                'email': data['email'],
                'role': data['role'],
                'createdAt': firestore.SERVER_TIMESTAMP,
                'studentInfo': {
                    'department':data['studentInfo']['department'],
                    'matricNumber': data['studentInfo']['matricNumber']
                }
            }
            self.collection.document(uid).set(user_data)
            return {
                "success": True,
                "message": f"Successfully created {data['role']} account", 
                "uid": uid
            }, 201
        except Exception as e:
            return {
                "Success": False,
                "error": str(e)
                }, 500
        
    def to_update(self, data, doc_id):
        try:
            doc_ref = self.collection.document(doc_id)
            if not doc_ref.get().exists:
                abort(404, description=f"document not found")

            doc_ref.update(data)
            return {
                "message": "User updated successfully",
                "updated_fields": list(data.keys())
            }
        except Exception as e:
            return {"error": str(e)}
        
    def to_promote(self, data):
        query = self.collection
        email = data['email']
        new_role = data['role']
        doc = query.where(filter=FieldFilter("email", "==", email)).limit(1).stream()
        user_doc = next(doc, None)
        if not user_doc:
            return {"error": "User Not Found"}
        user_doc.reference.update({"role": new_role})

        uid = user_doc.id
        auth.set_custom_user_claims(uid, {"role": new_role})

        return {"message": f"User promoted to {new_role}"}


    def get_id_from_user(self, data):
        query = self.collection
        email = data
        doc = query.where(filter=FieldFilter("email", "==", email)).limit(1).stream()
        user_doc = next(doc, None)
        if not user_doc:
            return {"error": "User Not Found"}
        return user_doc.id
        

user_service = UserServiceClass()
