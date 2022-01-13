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
    category = product["category"]
    quantity_available = product["quantity_available"]
    unit_price = product["unit_price"]
    supplier = product["supplier"]
    # image_url = product["image_url"]
    updated_at = datetime.now()

    mongo.db.product.update_one({
            "_id": ObjectId(product_id),
        },

        {"$set": {
            "product_name": product_name,
            "category": ObjectId(category),
            "quantity_available": int(quantity_available),
            "unit_price": float(unit_price),
            "supplier": ObjectId(supplier),
            "updated_at": updated_at
        }
    })

    # updated_product = mongo.db.product.find_one({"_id": ObjectId(product_id)}, {"password": 0})

    updated_product = mongo.db.product.aggregate(
        [
            {"$match": {"$and": [{"_id": ObjectId(product_id)}, {"record_status": "ACTIVE"}]}},

            {"$lookup": {
                "from": "category",
                "localField": "category",
                "foreignField": "_id",
                "as": "category"
            }},

            {"$unwind": "$category"},

            {"$lookup": {
                "from": "user",
                "localField": "supplier",
                "foreignField": "_id",
                "as": "supplier"
            }},

            {"$unwind": "$supplier"}
        ]
    )

    if updated_product:
        updated_product = json.loads(dumps(updated_product))

        if len(updated_product) > 0:
            return jsonify({
                "status": "200",
                "message": "product_updated_ok",
                "data": updated_product
            })

        else:
            return jsonify({
                "status": "404",
                "message": "product_not_found",
                "data": []
            })

    else:
        return jsonify({
            "status": "404",
            "message": "product_not_found",
            "data": []
        })