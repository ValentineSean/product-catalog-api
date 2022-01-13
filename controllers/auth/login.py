import json

from bson.json_util import dumps

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity
)
from flask_bcrypt import check_password_hash

from configurations.database import mongo

login_blueprint = Blueprint("login_blueprint", __name__)

@login_blueprint.route("/login", methods=["POST"])
def login():
    try:
        user = request.json

        email = user["email"]
        password = user["password"]

        # user = User.objects(record_status="ACTIVE",email=email).first()

        user = mongo.db.user.find_one({"$and": [{"email": email}, {"record_status": "ACTIVE"}]})

        if user:
            user = json.loads(dumps(user))

            if user["password"] == password:
                user.pop("password")
                access_token = create_access_token(identity=user)
                # print(user)

                return jsonify({
                    "status": "200",
                    "message": "user_authenticated_ok",
                    "token": access_token,
                })

            else:
                return jsonify({
                    "status": "401",
                    "message": "Incorrect credentials."
                })

        else:
            return jsonify({
                "status": "401",
                "message": "Incorrect credentials."
            })

    finally:
        pass