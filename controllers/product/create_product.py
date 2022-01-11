import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

create_product_blueprint = Blueprint("create_product_blueprint", __name__)

@create_product_blueprint.route("/create-product", methods=["POST"])
def create_product():
    product = request.json

    product_name = product["product_name"]
    category = product["category"]
    quantity_available = product["quantity_available"]
    supplier = product["supplier"]
    rating = product["rating"]
    image_url = product["image_url"]
    created_at = datetime.now()
    record_status = "ACTIVE"

    new_product_id = mongo.db.product.insert_one({
        "product_name": product_name,
        "category": {
            "$ref": "category",
            "$id": ObjectId(category)
        },
        "quantity_available": quantity_available,
        "supplier": supplier,
        "rating": rating,
        "created_at": created_at,
        "image_url": image_url,
        "record_status": record_status
    }).inserted_id

    new_product = mongo.db.product.find_one({
        "$and":[
            {"_id": ObjectId(new_product_id)},
            {"record_status": record_status}
        ],

        "category": {
            "$ref": "category",
            "$id": ObjectId(category)
        },
    })

    if new_product:
        new_product = json.loads(dumps(new_product))

        return jsonify({
            "status": "200",
            "message": "product_created_ok",
            "data": new_product
        })

    else:
        return jsonify({
            "status": "404",
            "message": "product_created_not_found",
            "data": {}
        })