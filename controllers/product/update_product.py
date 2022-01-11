import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

update_product_blueprint = Blueprint("update_product_blueprint", __name__)

@update_product_blueprint.route("/update-product", methods=["PUT"])
def update_product():
    product = request.json

    product_id = product["product_id"]
    product_id = product_id["$oid"]
    product_name = product["product_name"]
    image_url = product["image_url"]
    updated_at = datetime.now()

    mongo.db.product.update_one({
            "_id": ObjectId(product_id),
        },

        {"$set": {
            "product_name": product_name,
            "image_url": image_url,
            "updated_at": updated_at
        }
    })

    updated_product = mongo.db.product.find_one({"_id": ObjectId(product_id)}, {"password": 0})
    updated_product = json.loads(dumps(updated_product))

    return jsonify({
        "status": "200",
        "message": "product_created_ok",
        "data": updated_product
    })