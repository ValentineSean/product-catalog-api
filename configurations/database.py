import os

from flask_pymongo import PyMongo
from dotenv import load_dotenv

# ENV VARIABLES
load_dotenv()

user = os.getenv("DATABASEUSER")
password = os.getenv("DATABASEPASSWORD")
cluster = os.getenv("CLUSTER")
database = os.getenv("DATABASE")

database_credentials = {
    "user": user,
    "password": password,
    "cluster": cluster,
    "database": database
}

mongo = PyMongo()