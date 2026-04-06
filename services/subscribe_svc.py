from .base_svc import BaseServiceClass
from google.cloud.firestore_v1.field_path import FieldPath
from flask import abort


class SubscribeServiceClass(BaseServiceClass):
    def __init__(self):
        super().__init__("subscribe")

    def save(self, email):
        doc_ref = self.collection.document(email['email'])
        try:
            return doc_ref.create(email)
            # return {"message": "Email registered successfully"}
        except:
            {"message": "This email is already registered"}

    def getEach(self, email):
        return self.collection.document(email['email'])


    def delete(self, email):
        return self.collection.document(email).delete()
        # try:
        #     doc = self.collection.where('email', '==', email).limit(1).get()

        #     if not doc:
        #         abort(404, description="Cannot Email : Record does not exist.")
        #     doc.reference.delete()
        #     return {"message": f"Deleted {doc} successfully"}
        # except Exception as e:
        #     abort(500, description=f"Database Delete Error: {str(e)}")

        # return self.collection.document(doc).delete() 

subscribe_service = SubscribeServiceClass()