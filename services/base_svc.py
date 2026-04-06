from firebase_admin import firestore, exceptions
from flask import abort
from services.imagekit_svc import imageKit_service



class BaseServiceClass():
    def __init__(self, collection_name):
        # try:
            # self.db = firestore.client()
            self.collection_name = collection_name
        # except Exception as e:
            # abort(500, description=f"Firebase Initialization Error: {str(e)}")

    @property
    def db(self):
        return firestore.client()
    
    @property
    def collection(self):
        return self.db.collection(self.collection_name)
        

    def get_all(self):
        try:
            docs = self.collection.stream()
            result = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                result.append(data)
            
            return result 
        except exceptions.FirebaseError as e:
            abort(500, description=f"Database Read Error: {e.code} - {str(e)}")

    def get_by_id(self, doc_id):
        try:
            doc_ref = self.collection.document(doc_id)
            doc = doc_ref.get()
            if not doc.exists:
                abort(404, description=f"Record with ID {doc_id} not found.")
            data = doc.to_dict()
            data["id"] = doc.id
            return data 
        except exceptions.FirebaseError as e:
            abort(500, description= f"Database Fetch Error: {str(e)}")

    def create(self, data):
        # """Remember to put the code that will fetch the user id from auth to ensure that the user is present"""
        # # doc = self.collection.document(doc_id).set(data)
        # # return {"message": "Success", "id": doc.id}
        print("It has entered inside the base_svc.py")
        doc_ref = self.collection.add(data)
        # Logic to send notification to admins
          
        return {"id": doc_ref[1].id, **data}

    def delete(self, doc_id):
        try:
            doc_ref = self.collection.document(doc_id)
            if not doc_ref.get().exists:
                abort(404, description="Cannot delete : Record does not exist.")
            doc_ref.delete()
            return {"message": f"Deleted {doc_id} successfully"}
        except exceptions.FirebaseError as e:
            abort(500, description=f"Database Delete Error: {str(e)}")

        return self.collection.document(doc_id).delete() 

  
    def create_with_Image(self, data_file):
        try:
            print("In the create Image in base_svc.py")
            image_url = imageKit_service.upload_image(data_file)
            if image_url is not None:
                print("This is the creat image tag")
                print(image_url)
                return image_url
        except Exception as e:
            abort(500, description=f"Image insertion to cloud failed: {str(e)}")