import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

create_category_blueprint = Blueprint("create_category_blueprint", __name__)

@create_category_blueprint.route("/create-category", methods=["POST"])
def create_category():
    category = request.json
    category_name = category["category_name"]
    created_at = datetime.now()
    record_status = "ACTIVE"

    new_category_id = mongo.db.category.insert_one({
        "category_name": category_name,
        "created_at": created_at,
        "updated_at": created_at,
        "record_status": record_status
    }).inserted_id

    new_category = mongo.db.category.find_one({"$and": [{"_id": ObjectId(new_category_id)}, {"record_status": record_status}]})

    if new_category:
        new_category = json.loads(dumps(new_category))

        return jsonify({
            "status": "200",
            "message": "category_created_ok",
            "data": new_category
        })

    else:
        return jsonify({
            "status": "404",
            "message": "category_created_not_found",
            "data": []
        })