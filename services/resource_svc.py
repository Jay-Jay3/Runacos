from .base_svc import BaseServiceClass
from google.cloud.firestore_v1.field_path import FieldPath
from flask import abort


class ResourceServiceClass(BaseServiceClass):
    def __init__(self):
        super().__init__("resource")

    def search(self, filters):
        print(filters)
        result = {}
        query = self.collection
        for key, value in filters.items():
            print(f"key: {key}, value: {value}")
            query = query.where(key, "==", value)
            docs = query.stream()

            for doc in docs:
                item = doc.to_dict()
                item["id"] = doc.id
                result[doc.id] = item

        print(result)
        return result
    
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
    
            



resource_service = ResourceServiceClass()