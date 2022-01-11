import json

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify

# Database
from configurations.database import mongo

get_users_blueprint = Blueprint("get_users_blueprint", __name__)

@get_users_blueprint.route("/get-users", methods=["GET"])
def get_users():

    users = mongo.db.user.find({}, {"password": 0})

    if users:
        users = json.loads(dumps(users))

        return jsonify({
            "status": "200",
            "message": "users_retrieved_ok",
            "data": users
        })

    else:
        return jsonify({
            "status": "404",
            "message": "users_not_found",
            "data": []
        })