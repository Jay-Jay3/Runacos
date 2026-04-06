import requests
import os

FIREBASE_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    payload = {
        "email":email,
        "password":password,
        "returnSecureToken":True 
    }

    response = requests.post(url, json=payload)
    return response.json(), response.status_code