import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

add_favorite_blueprint = Blueprint("add_favorite_blueprint", __name__)

@add_favorite_blueprint.route("/add-favorite", methods=["POST"])
def add_favorite():
    customer = request.json

    customer_id = customer["customer_id"]
    product_id = customer["product_id"]

    mongo.db.user.update_one({
            "_id": ObjectId(customer_id),
        },

        {"$push": {"favorites": product_id}
    })

    updated_user = mongo.db.user.find_one({"_id": ObjectId(customer_id)}, {"password": 0})

    if updated_user:
        updated_user = json.loads(dumps(updated_user))

        return jsonify({
            "status": "200",
            "message": "user_updated_ok",
            "data": updated_user
        })

    else:
        return jsonify({
            "status": "404",
            "message": "user_not_found",
            "data": {}
        })