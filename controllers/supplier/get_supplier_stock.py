import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

get_supplier_stock_blueprint = Blueprint("get_supplier_stock_blueprint", __name__)

@get_supplier_stock_blueprint.route("/get-supplier-stock", methods=["GET"])
def get_supplier_stock():
    active = "ACTIVE"
    supplier = request.args.get("supplier")
    # products = mongo.db.product.find({"record_status": active})
    products = mongo.db.product.aggregate(
        [
            {"$match": {"supplier": ObjectId(supplier)}},

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

    if products:
        products = json.loads(dumps(products))

        return jsonify({
            "status": "200",
            "message": "products_retrieved_ok",
            "data": products
        })

    else:
        return jsonify({
            "status": "404",
            "message": "products_not_found",
            "data": []
        })