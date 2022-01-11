import os

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

# CONFIGURATIONS
from configurations.database import mongo, database_credentials
from configurations.auth import jwt, bcrypt

# BLUEPRINTS

# AUTH
from controllers.auth.login import login_blueprint

# USER
from controllers.user.create_user import create_user_blueprint
from controllers.user.get_users import get_users_blueprint
from controllers.user.update_user import update_user_blueprint

# CATEGORY
from controllers.category.create_category import create_category_blueprint
from controllers.category.get_categories import get_categories_blueprint
from controllers.category.update_category import update_category_blueprint

# PRODUCT
from controllers.product.create_product import create_product_blueprint
from controllers.product.get_products import get_products_blueprint
from controllers.product.update_product import update_product_blueprint

app = Flask(__name__)

def create_app():
    # Database Connection
    app.config["MONGO_URI"] = "mongodb+srv://{}:{}@{}.vfd0n.mongodb.net/{}?retryWrites=true&w=majority".format(
        database_credentials["user"],
        database_credentials["password"],
        database_credentials["cluster"],
        database_credentials["database"]
    )
    mongo.init_app(app)

    # JWT Token Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 604800

    jwt.init_app(app)
    bcrypt.init_app(app)

    # AUTH
    app.register_blueprint(login_blueprint)

    # USER
    app.register_blueprint(create_user_blueprint)
    app.register_blueprint(get_users_blueprint)
    app.register_blueprint(update_user_blueprint)

    # CATEGORY
    app.register_blueprint(create_category_blueprint)
    app.register_blueprint(get_categories_blueprint)
    app.register_blueprint(update_category_blueprint)

    # PRODUCT
    app.register_blueprint(create_product_blueprint)
    app.register_blueprint(get_products_blueprint)
    app.register_blueprint(update_product_blueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()