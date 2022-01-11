import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

update_user_blueprint = Blueprint("update_user_blueprint", __name__)

@update_user_blueprint.route("/update-user", methods=["PUT"])
def update_user():
    user = request.json

    user_id = user["user_id"]
    user_id = user_id["$oid"]
    email = user["email"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    password = user["password"]
    role = user["role"]
    updated_at = datetime.now()

    mongo.db.user.update_one({
            "_id": ObjectId(user_id),
        },

        {"$set": {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "role": role,
            "updated_at": updated_at
        }
    })

    updated_user = mongo.db.user.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    updated_user = json.loads(dumps(updated_user))

    return jsonify({
        "status": "200",
        "message": "user_created_ok",
        "data": updated_user
    })