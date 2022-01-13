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
    # product_id = product_id["$oid"]
    rating = product["rating"]

    product = mongo.db.product.find_one({"$and": [{"_id": ObjectId(product_id)}, {"record_status": "ACTIVE"}]})

    if product:
        product = json.loads(dumps(product))

        votes = product["votes"]
        new_votes = product["votes"] + 1
        old_rating = product["rating"]

        new_rating = ((old_rating * votes) + rating) / (new_votes)

        mongo.db.product.update_one({
            "_id": ObjectId(product_id),
            },

            {"$set": {
                "rating": new_rating,
                "votes": new_votes
            }
        })

        # rated_product = mongo.db.product.find_one({"_id": ObjectId(product_id)})

        rated_product = mongo.db.product.aggregate(
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

        if rated_product:
            rated_product = json.loads(dumps(rated_product))

            if len(rated_product) > 0:
                return jsonify({
                    "status": "200",
                    "message": "product_rated_ok",
                    "data": rated_product
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

    else:
        return jsonify({
            "status": "404",
            "message": "product_not_found",
            "data": []
        })