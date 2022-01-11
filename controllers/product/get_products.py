import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

get_products_blueprint = Blueprint("get_products_blueprint", __name__)

@get_products_blueprint.route("/get-products", methods=["GET"])
def get_products():

    products = mongo.db.product.find()

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