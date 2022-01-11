import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

create_user_blueprint = Blueprint("create_user_blueprint", __name__)

@create_user_blueprint.route("/create-user", methods=["POST"])
def create_user():
    user = request.json

    email = user["email"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    password = user["password"]
    role = user["role"]
    created_at = datetime.now()

    new_user_id = mongo.db.user.insert({
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "role": role,
        "created_at": created_at
    })

    new_user = mongo.db.user.find_one({"_id": ObjectId(new_user_id)}, {"password": 0})
    new_user = json.loads(dumps(new_user))

    return jsonify({
        "status": "200",
        "message": "user_created_ok",
        "data": new_user
    })