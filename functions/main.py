from firebase_functions import firestore_fn
from firebase_admin import initialize_app, firestore

initialize_app()

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os

# INITIALISING BREVO CONFIGURATION
configuration = sib_api_v3_sdk.Configuration()

configuration.api_key['api-key'] = os.environ.get("BRAVO_API_KEY")

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

@firestore_fn.on_document_created(document="faultReporting/{id}", secrets=["BRAVO_API_KEY"])
def send_admin_email_fault_creationII(event:firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
        if event.data is None:
            return 
        fault_data = event.data.to_dict() 
        title = fault_data.get("title", "Unknown Fault")
        description = fault_data.get("description", "No description added")

        # admin_emails = ["johndictguru@gmail.com", "johnmamudauni@gmail.com"]

        db = firestore.client()
        admins_query = db.collection("user").where("role", "==", "admin").stream()
        admin_emails = [admin.to_dict().get("email") for admin in admins_query if admin.to_dict().get("email")]

        if not admin_emails:
            print("No admin email found")
            return 
        
        send_stmp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=admin_emails,
            html_content=f"""                    
                <h2> New Fault Detected</h2>
                <p><strong>Title : </strong>{title}</p>
                <p><strong>Description : </strong>{description}</p>
                <p>Please log in to the admin dashboard to review.</p>
                """,
            subject="New Fault Reported",
            sender={'name': "Fault Reports", "email": "mamudajohn3@gmail.com"})
        try:
             api_response = api_instance.send_transac_email(send_stmp_email)
             print(f"Email sent successfully. ID: {api_response.message_id}")
             
        except ApiException as e:
             print(f"Exception when calling TransactionalEmailsApi \n Send_transac_email: {e}")




# import resend
# import os

# # REMEMBER TO CONFIGURE THIS ON THE CLOUD ENVIRONMENT 
# resend.api_key = os.environ.get("RESEND_API_KEY")

# @firestore_fn.on_document_created(document="faultReporting/{id}", secrets=["RESEND_API_KEY"])
# def send_admin_email_fault_creation(event:firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
#     if event.data is None:
#         return 
#     fault_data = event.data.to_dict() 
#     title = fault_data.get("title", "Unknown Fault")
#     description = fault_data.get("description", "No description added")

#     admin_emails = ["johndictguru@gmail.com", "johnmamudauni@gmail.com"]

#     # db = firestore.client()
#     # admins_query = db.collection("user").where("role", "==", "admin").stream()
#     # admin_emails = [admin.to_dict().get("email") for admin in admins_query if admin.to_dict().get("email")]

#     if not admin_emails:
#         print("No admin email found")
#         return 
#     try:
#         response = resend.Emails.send({
#             "from": "Runacos<onboarding@resend.dev>",
#             "to": "mamudajohn3@gmail.com",
#             "subject": f"New Fault Reported: {title}",
#             "html": f"""
#                 <h2> New Fault Detected</h2>
#                 <p><strong>Title:</strong>{title}</p>
#                 <p><strong>Description</strong>{description}</p>
#                 <p>Please log in to the admin dashboard to review.</p>
#                 """
#         })
#         print(f"Email sent successfully. Response: {response}")

#     except Exception as e:
#         print(f"Failed to send email: {e}")



# @firestore_fn.on_document_created(document="events/{id}", secrets=["RESEND_API_KEY"])
# def send_admin_email_event_creation(event:firestore_fn.Event[firestore_fn.DocumentSnapshot | None]) -> None:
#     if event.data is None:
#         return
    
#     data = event.data.to_dict()

#     title = data.get("title", "Unknown Title")
#     time = data.get("eventTime", "Event Time")
#     description = data.get("description", "Event Description")
#     image = data.get("fileUrl", "The Event Theme Images")

#     admin_emails = ["johndictguru@gmail.com", "johnmamudauni@gmail.com"]

#     # db = firestore.client()
#     # admins_query = db.collection("user").where("role", "==", "admin").stream()
#     # admin_emails = [admin.to_dict().get("email") for admin in admins_query if admin.to_dict().get("email")]


#     if not admin_emails:
#         print("No admin email found")
#         return 
#     try:
#         response = resend.Emails.send({
#             "from": "Runacos<onboarding@resend.dev>",
#             "to": "mamudajohn3@gmail.com",
#             "subject": f"New Event : {title} !!! !!!",
#             "html": f"""
#                 <img src={image}>
#                 <h2> New Upcoming Event</h2>
#                 <p><strong>Title : </strong>{title}</p>
#                 <p><strong>Time : </strong>{time}</p>
#                 <p><strong>Description </strong>{description}</p>
#                 <p>Please we will be ernestly expecting your gracious presence .</p>
#                 """
#         })
#         print(f"Email sent successfully. Response: {response}")

#     except Exception as e:
#         print(f"Failed to send email: {e}")


