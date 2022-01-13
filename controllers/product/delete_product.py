import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash

# Database
from configurations.database import mongo

delete_product_blueprint = Blueprint("delete_product_blueprint", __name__)

@delete_product_blueprint.route("/delete-product", methods=["DELETE"])
def delete_product():
    product = request.json

    product_id = product["product_id"]
    product_id = product_id["$oid"]
    record_status = "DELETED"
    updated_at = datetime.now()

    mongo.db.product.update_one({
            "_id": ObjectId(product_id),
        },

        {"$set": {
            "record_status": record_status,
            "updated_at": updated_at
        }
    })
    
    deleted_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

    if deleted_product:
        deleted_product = json.loads(dumps(deleted_product))

        return jsonify({
            "status": "200",
            "message": "product_deleted_ok",
            "data": deleted_product
        })

    else:
        return jsonify({
            "status": "404",
            "message": "product_not_found",
            "data": []
        })