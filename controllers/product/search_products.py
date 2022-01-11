import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

search_products_blueprint = Blueprint("search_products_blueprint", __name__)

@search_products_blueprint.route("/search-products", methods=["POST"])
def search_product():
    search_criteria = request.args.get("search_criteria")
    search_product = request.json

    search_string = search_product["search_string"]

    if search_criteria == "product":
        products = mongo.db.product.aggregate([
            {
                "$search": {
                    "index": "product_index",
                    "text": {
                        "query": search_string,
                        "path": "product_name"
                    }
                }
            }
        ])

        # searchd_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

        if products:
            products = json.loads(dumps(products))

            if len(products) > 0:

                return jsonify({
                    "status": "200",
                    "message": "product_searched_ok",
                    "data": products
                })

            else:
                return jsonify({
                    "status": "404",
                    "message": "products_not_found",
                    "data": []
                })

        else:
            return jsonify({
                "status": "404",
                "message": "products_not_found",
                "data": []
            })

    elif search_criteria == "category":
        category = mongo.db.category.aggregate([
            {
                "$search": {
                    "index": "category_index",
                    "text": {
                        "query": search_string,
                        "path": "category_name"
                    }
                }
            }
        ])

    elif search_criteria == "supplier":
        supplier = mongo.db.user.aggregate([
            {
                "$search": {
                    "index": "supplier_index",
                    "text": {
                        "query": search_string,
                        "path": "supplier_first_name"
                    }
                }
            }
        ])