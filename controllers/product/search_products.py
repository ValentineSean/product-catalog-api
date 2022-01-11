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

    search_path = search_product["search_path"]
    search_index = search_product["search_index"]
    search_string = search_product["search_string"]

    if search_criteria == "product_name":
        products = mongo.db.product.aggregate([
            {
                "$search": {
                    "index": search_index,
                    "text": {
                        "query": search_string,
                        "path": search_path
                    }
                }
            }
        ])

        searchd_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

        if searchd_product:
            searchd_product = json.loads(dumps(searchd_product))

            return jsonify({
                "status": "200",
                "message": "product_searchd_ok",
                "data": searchd_product
            })

        else:
            return jsonify({
                "status": "404",
                "message": "product_not_found",
                "data": {}
            })