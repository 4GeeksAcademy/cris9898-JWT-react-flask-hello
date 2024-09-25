"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def register_new_user():
    try: 
        
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)

        
        if email is None or password is None:
            return jsonify({"error": "Email and password are required"}), 400
        
        
        email_is_taken = User.query.filter_by(email=email).first() 
        if email_is_taken:
            return jsonify({"error": "Email already exists"}), 400
        
        
        password_hash = generate_password_hash(password)
        
        
        user = User(email=email, password=password_hash, is_active=True)
        
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully!"}), 201
        
    except Exception as error:
        
        print(f"Error occurred: {error}")
        return jsonify({"error": f"Internal server error: {error}"}), 500


@api.route("/login", methods=["POST"])
def login():
    try:
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)
        
        if email is None or password is None:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        print(f"User: {user}, Password Valid: {check_password_hash(user.password, password)}")
        
        if user is None or not check_password_hash(user.password, password):
            return jsonify({"error": "Email or password is incorrect"}), 400

        # Crear el token
        auth_token = create_access_token(identity={"id": user.id, "email": user.email})

        return jsonify({
            "token": auth_token,
            "user": {
                "id": user.id,
                "email": user.email,
            }
        }), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500



@api.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()  
        return jsonify([user.serialize() for user in users]), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500  