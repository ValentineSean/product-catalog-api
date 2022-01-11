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

# CATEGORY
from controllers.category.create_category import create_category_blueprint

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

    # CATEGORY
    app.register_blueprint(create_category_blueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()