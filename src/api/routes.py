"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        # Obtener datos del cuerpo de la solicitud
        body = request.json
        email = body.get("email", None)
        password = body.get("password", None)

        
        
        # Validar que email y password estén presentes
        if email is None or password is None:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Verificar si el email ya está registrado
        email_is_taken = User.query.filter_by(email=email).first() 
        if email_is_taken:
            return jsonify({"error": "Email already exists"}), 400
        
        # Generar el hash de la contraseña
        password_hash = generate_password_hash(password)
        
        # Crear el nuevo usuario
        user = User(email=email, password=password_hash, is_active=True)
        print("User:-----------------------------------------------------------------------------")
        print(user)
        print("User:-----------------------------------------------------------------------------")
        # Guardar el usuario en la base de datos
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully!"}), 201
        
    except Exception as error:
        # Agregar el print del error para ver más detalles en los logs
        print(f"Error occurred: {error}")
        return jsonify({"error": f"Internal server error: {error}"}), 500
    

@api.route("/signup", methods=["POST"])
def signup():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)

    if email is None or password is None:
        return jsonify({"error": "Email and password required"}), 400
    
    password_hash = generate_password_hash(password)

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already taken"}), 400
    
    try:
        new_user = User(email=email, password=password_hash, is_active=True)
        db.session.add(new_user)
        db.session.commit()

        # Genera un token de acceso
        user_token = create_access_token(identity={"id": new_user.id, "email": new_user.email})

        # Devuelve el token y un mensaje
        return jsonify({"message": "User created", "token": user_token}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}), 500

@api.route("/signin", methods=["POST"])
def signin():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)
    if email is None or password is None:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Error while loggin in"})
    
    user_token = create_access_token({"id": user.id, "email": user.email})
    return jsonify({"token": user_token})