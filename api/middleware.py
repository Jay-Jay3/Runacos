from functools import wraps
from flask import request, abort, jsonify
from firebase_admin import auth


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request.user = {
            "uid": "faculty_001",
            "role": "faculty",
            "name": "Dr Smith"
        }
        return f(*args, **kwargs)
    return decorated_function


def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_functions(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            print("In the auth Middleware")
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Authorisation token is missing or invalid"}), 401
            try: 
                id_token = auth_header.split("Bearer ")[1]
                decoded_token = auth.verify_id_token(id_token)
                user_role = decoded_token.get('role')
                if user_role not in allowed_roles:
                    # abort(403)
                    return jsonify({"error": "Forbidden",
                        "message": f"Require one of: {','.join(allowed_roles)}. you are {user_role}"}), 403
                request.user = decoded_token
            except auth.ExpiredIdTokenError:
                return jsonify({
                    "error": "Token has expired"
                }), 401
            except Exception as e:
                return jsonify({
                    "error": "Authentication failed",
                    "details": str(e)
                }), 500
            return f(*args, **kwargs)
        return decorated_functions
    return decorator
        