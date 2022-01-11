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
    favorites = []
    created_at = datetime.now()
    record_status = "ACTIVE"

    new_user_id = mongo.db.user.insert_one({
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "role": role,
        "favorites": favorites,
        "created_at": created_at,
        "updated_at": created_at,
        "record_status": record_status
    }).inserted_id

    new_user = mongo.db.user.find_one({"_id": ObjectId(new_user_id)}, {"password": 0})

    if new_user:
        new_user = json.loads(dumps(new_user))

        return jsonify({
            "status": "200",
            "message": "user_created_ok",
            "data": new_user
        })

    else:
        return jsonify({
            "status": "404",
            "message": "user_created_not_found",
            "data": {}
        })