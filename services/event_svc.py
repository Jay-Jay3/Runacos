from .base_svc import BaseServiceClass
from flask import abort


class EventsServiceClass(BaseServiceClass):
    def __init__(self):
        super().__init__("events")

    # def get_user_by_id(self, user_id):
    #     docs = self.collection.where()
    #     return ""

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


events_service = EventsServiceClass()