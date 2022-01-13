# product-catalog-api

## Steps to run the API:
- create _.env_ file and define the following variables:
  - DATABASEUSER (MongoDB user)
  - DATABASEPASSWORD (MongoDB password)
  - CLUSTER (MongoDB cluster)
  - DATABASE (MongoDB database)
  - JWT_SECRET_KEY (JWT secret key)
  - CLOUDINARY_API_KEY (Cloudinary API key)
  - CLOUDINARY_API_SECRET (Cloudinary API secret)
  - CLOUDINARY_CLOUD_NAME (Cloudinary cloud name)
- Open command prompt:
- create virtual environment using the command: `python -m venv [environment_name]`
- active virtual environment using the command: `[environment_name]\Scripts\activate`
- install all libraries using the command: `pip install -r requirements.txt`
- set flask app using command: `set FLASK_APP=app.py`
- if on development server, set flask app using command: `set FLASK_ENV=development`
- run the application using command `flask run`

_Please note: This is a Windows 10 set up_
