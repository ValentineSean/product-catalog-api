import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

delete_category_blueprint = Blueprint("delete_category_blueprint", __name__)

@delete_category_blueprint.route("/delete-category", methods=["DELETE"])
def delete_category():
    category = request.json

    category_id = category["category_id"]
    category_id = category_id["$oid"]
    record_status = "DELETED"
    updated_at = datetime.now()

    mongo.db.category.update_one({
            "_id": ObjectId(category_id),
        },

        {"$set": {
            "record_status": record_status,
            "updated_at": updated_at
        }
    })
    
    deleted_category = mongo.db.category.find_one({"_id": ObjectId(category_id)})

    if deleted_category:
        deleted_category = json.loads(dumps(deleted_category))

        return jsonify({
            "status": "200",
            "message": "category_deleted_ok",
            "data": deleted_category
        })

    else:
        return jsonify({
            "status": "404",
            "message": "category_not_found",
            "data": []
        })