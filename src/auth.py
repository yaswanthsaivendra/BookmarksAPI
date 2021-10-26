from os import access
from flask import Blueprint, request
from flask.json import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from src.database import User, db
from flask_jwt_extended import create_access_token, create_refresh_token


auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']


    if len(password)<6:
        return jsonify({'error':"password is too short"}), 400

    if len(username)<3:
        return jsonify({'error':"username is too short"}), 400

    if not username.isalnum():
        return jsonify({'error':"username should contain alphanumeric characters only"}), 400

    if " " in username:
        return jsonify({'error':"username should not contain any spaces"}), 400

    if not validators.email(email):
        return jsonify({'error':"Email is not valid"}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is already registered"}), 409

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username is already taken"}), 409

    pwd_hash = generate_password_hash(password)
    user = User(username=username, email=email,password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            'message':"User created",
            'user':{
                'username':username,
                'email':email
            }
        }
    ), 201






@auth.post("/login")
def login():
    email = request.json.get('email','')
    password = request.json.get('password','')


    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)


            return jsonify({
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'email':user.email
                }
            }), 200

    return jsonify({'error':"wrong credentials"}), 401
