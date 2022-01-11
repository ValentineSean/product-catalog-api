import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

rate_product_blueprint = Blueprint("rate_product_blueprint", __name__)

@rate_product_blueprint.route("/rate-product", methods=["PUT"])
def rate_product():
    product = request.json

    product_id = product["product_id"]
    product_id = product_id["$oid"]
    rating = product["rating"]

    mongo.db.product.update_one({
            "_id": ObjectId(product_id),
        },

        {"$set": {
            "rating": rating,
        }
    })

    rated_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

    if rated_product:
        rated_product = json.loads(dumps(rated_product))

        return jsonify({
            "status": "200",
            "message": "product_rated_ok",
            "data": rated_product
        })

    else:
        return jsonify({
            "status": "404",
            "message": "product_not_found",
            "data": {}
        })