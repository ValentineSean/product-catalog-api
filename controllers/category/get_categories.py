import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

get_categories_blueprint = Blueprint("get_categories_blueprint", __name__)

@get_categories_blueprint.route("/get-categories", methods=["GET"])
def get_categories():

    categories = mongo.db.category.find()

    if categories:
        categories = json.loads(dumps(categories))

        return jsonify({
            "status": "200",
            "message": "categories_retrieved_ok",
            "data": categories
        })

    else:
        return jsonify({
            "status": "404",
            "message": "categories_not_found",
            "data": []
        })