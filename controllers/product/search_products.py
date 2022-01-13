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
                        "path": "product_name",
                        "fuzzy": {}
                    }
                }
            },

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
        ])

        # searchd_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

        if products:
            products = json.loads(dumps(products))

            if len(products) > 0:

                return jsonify({
                    "status": "200",
                    "message": "products_searched_ok",
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
        categories = mongo.db.category.aggregate([
            {
                "$search": {
                    "index": "category_index",
                    "text": {
                        "query": search_string,
                        "path": "category_name",
                        "fuzzy": {}
                    }
                }
            }
        ])

        if categories:
            categories = json.loads(dumps(categories))

            if len(categories) > 0:

                category = categories[0]
                category = category["_id"]["$oid"]

                products = mongo.db.product.aggregate([
                    {"$match": {"category": ObjectId(category)}},

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
                ])

                if products:
                    products = json.loads(dumps(products))

                    return jsonify({
                        "status": "200",
                        "message": "products_searched_ok",
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
                    "message": "category_not_found",
                    "data": []
                })

        else:
            return jsonify({
                "status": "404",
                "message": "category_not_found",
                "data": []
            })



    elif search_criteria == "supplier":
        suppliers= mongo.db.user.aggregate([
            {"$match": {"role": "SUPPLIER"}},

            {
                "$search": {
                    "index": "supplier_index",
                    "text": {
                        "query": search_string,
                        "path": ["first_name", "last_name"],
                        "fuzzy": {}
                    }
                }
            }
        ])

        if suppliers:
            suppliers = json.loads(dumps(suppliers))

            if len(suppliers) > 0:

                supplier = suppliers[0]
                supplier = supplier["_id"]["$oid"]

                products = mongo.db.product.aggregate([
                    {"$match": {"category": ObjectId(supplier)}},

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
                ])

                if products:
                    products = json.loads(dumps(products))

                    return jsonify({
                        "status": "200",
                        "message": "products_searched_ok",
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
                    "message": "supplier_not_found",
                    "data": []
                })

        else:
            return jsonify({
                "status": "404",
                "message": "supplier_not_found",
                "data": []
            })