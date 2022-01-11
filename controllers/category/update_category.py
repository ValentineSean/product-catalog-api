import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

update_category_blueprint = Blueprint("update_category_blueprint", __name__)

@update_category_blueprint.route("/update-category", methods=["PUT"])
def update_category():
    category = request.json

    category_id = category["category_id"]
    category_id = category_id["$oid"]
    category_name = category["category_name"]
    updated_at = datetime.now()

    mongo.db.category.update_one({
            "_id": ObjectId(category_id),
        },

        {"$set": {
            "category_name": category_name,
            "updated_at": updated_at
        }
    })

    updated_category = mongo.db.category.find_one({"_id": ObjectId(category_id)}, {"password": 0})
    updated_category = json.loads(dumps(updated_category))

    return jsonify({
        "status": "200",
        "message": "category_created_ok",
        "data": updated_category
    })