import os
import json

import cloudinary
import cloudinary.uploader
import cloudinary.api

from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Database
from configurations.database import mongo

create_product_blueprint = Blueprint("create_product_blueprint", __name__)

@create_product_blueprint.route("/create-product", methods=["POST"])
def create_product():
    product = request.json

    product = request.form
    product_image = request.files["product_image"]

    product_name = product["product_name"]
    category = product["category"]
    quantity_available = product["quantity_available"]
    supplier = product["supplier"]
    rating = 0
    # image_url = product["image_url"]
    created_at = datetime.now()
    record_status = "ACTIVE"

    # UPLOADING PRODUCT IMAGE
    load_dotenv()

    try:
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        cloudinary.config( 
            cloud_name = cloud_name, 
            api_key = api_key, 
            api_secret = api_secret,
            secure = True
        )

        product_image = cloudinary.uploader.upload(product_image, use_filename=True, folder="product-catalog")
        image_url = product_image["url"]

        new_product_id = mongo.db.product.insert_one({
            "product_name": product_name,
            "category": {
                "$ref": "category",
                "$id": ObjectId(category)
            },
            "quantity_available": quantity_available,
            "supplier": supplier,
            "rating": rating,
            "created_at": created_at,
            "image_url": image_url,
            "record_status": record_status
        }).inserted_id

        new_product = mongo.db.product.find_one({
            "$and":[
                {"_id": ObjectId(new_product_id)},
                {"record_status": record_status}
            ],

            "category": {
                "$ref": "category",
                "$id": ObjectId(category)
            },
        })

        if new_product:
            new_product = json.loads(dumps(new_product))

            return jsonify({
                "status": "200",
                "message": "product_created_ok",
                "data": new_product
            })

        else:
            return jsonify({
                "status": "404",
                "message": "product_created_not_found",
                "data": {}
            })

    except:
        return jsonify({
            "status": "500",
            "message": "product_image_upload_error",
            "data": {}
        })