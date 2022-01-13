import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

delete_user_blueprint = Blueprint("delete_user_blueprint", __name__)

@delete_user_blueprint.route("/delete-user", methods=["DELETE"])
def delete_user():
    user = request.json

    user_id = user["user_id"]
    user_id = user_id["$oid"]
    record_status = "DELETED"
    updated_at = datetime.now()

    mongo.db.user.update_one({
            "_id": ObjectId(user_id),
        },

        {"$set": {
            "record_status": record_status,
            "updated_at": updated_at
        }
    })

    deleted_user = mongo.db.user.find_one({"_id": ObjectId(user_id)}, {"password": 0})

    if deleted_user:
        deleted_user = json.loads(dumps(deleted_user))

        return jsonify({
            "status": "200",
            "message": "user_deleted_ok",
            "data": deleted_user
        })

    else:
        return jsonify({
            "status": "404",
            "message": "user_not_found",
            "data": []
        })