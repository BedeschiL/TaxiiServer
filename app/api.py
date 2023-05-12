import json
import os
import re
import traceback

import yaml
from flask import Flask, Response, request, jsonify
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth

from api_error import CustomException
from database import data_handling
from database.data_handling import DataHandler


def read_config_file():
    file_directory = os.path.dirname(os.path.abspath(__file__))
    try:
        with open('{}/api_config.yaml'.format(file_directory)) as f:
            config = yaml.safe_load(f)
            return config
        # end with
    except Exception:
        print(traceback.format_exc())
        return None


config = read_config_file()
print(config)
users = {
    config.get("USER"): config.get("PASSWORD")
}

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config["MONGO_URI"] = "mongodb://mongo:password@mongodb:27017/mydatabase"
mongo = PyMongo(app)
p = DataHandler(app.config["MONGO_URI"], "mongo", "password")


@auth.verify_password
def verify_password(username, password):
    # Vérifiez si le nom d'utilisateur et le mot de passe sont valides
    if username in users and password == users[username]:
        return username
    else:
        raise CustomException('The client needs to authenticate', 401)


def validate_version_parameter_in_accept_header():
    """All endpoints need to check the Accept Header for the correct Media Type"""
    accept_header = request.headers.get("accept", "").replace(" ", "").split(",")
    found = False
    for item in accept_header:
        result = re.match(r"^application/taxii\+json(;version=(\d\.\d))?$", item)
        if result:
            if len(result.groups()) >= 1:
                version_str = result.group(2)
                if version_str != "2.1":  # The server only supports 2.1
                    raise CustomException('This serveur only support 2.1 STIX', 404)
            found = True
            break

    if found is False:
        raise CustomException('The media type provided in the Accept header is invalid', 406)

    return True


def api_root_exist(api_root):
    exist = p.api_root_exist(api_root)
    if exist is False:
        raise CustomException('The API Root is not found, or the client does not have access to the ressource '
                              'resource', 404)


def taxii_col_exist(api_root, col):
    exist = p.taxii_col_exist(api_root, col)
    if exist is False:
        raise CustomException('The collections is not found, or the client does not have access to the collections '
                              'resource', 404)


@app.errorhandler(CustomException)
def handle_exception(error):
    # Récupérer le code d'erreur et le message de l'exception personnalisée
    code = error.code
    message = str(error)
    # Renvoyer une réponse JSON avec le code d'erreur et le message personnalisé
    response = jsonify({'error': message})
    response.status_code = code
    return response


@app.route("/taxii2/", methods=["GET"])
@auth.login_required
def discovery():
    validate_version_parameter_in_accept_header()

    x = p.discovery()
    x = json.dumps(x)
    return Response(
        response=x,
        status=200,
        mimetype="application/taxii+json;version=2.1",
    )


@app.route("/<string:api_root>/", methods=["GET"])
@auth.login_required
def get_api_root_information(api_root):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)

    x = p.get_root_information(api_root)
    x = json.dumps(x)

    return x


@app.route("/<string:api_root>/collections/", methods=["GET"])
@auth.login_required
def get_api_root_collections(api_root):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)

    x = p.get_api_root_collections(api_root)
    x = json.dumps(x)
    return x


@app.route("/<string:api_root>/collections/<string:id_col>/", methods=["GET"])
@auth.login_required
def get_api_root_collection_by_id(api_root, id_col):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)

    taxii_col_exist(api_root, id_col)
    x = p.get_api_root_collection_by_id(api_root, id_col)
    x = json.dumps(x)

    return x


@app.route("/<string:api_root>/collections/<string:id_col>/objects/", methods=["GET"])
@auth.login_required
def get_api_root_collections_objects(api_root, id_col):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)
    taxii_col_exist(api_root, id_col)

    x = p.get_api_root_collections_objects(api_root, id_col, request.args.to_dict())
    x = json.dumps(x)

    return x


@app.route("/<string:api_root>/collections/<string:id_col>/objects/<string:id_obj>/", methods=["GET", "DELETE"])
@auth.login_required
def get_api_root_collections_object_by_id(api_root, id_col, id_obj):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)
    taxii_col_exist(api_root, id_col)

    if request.method == "GET":
        x = p.get_api_root_collections_object_by_id(api_root, id_col, id_obj, request.args.to_dict())
        x = json.dumps(x)
    if request.method == "DELETE":
        x = p.delete_api_root_collections_object_by_id(api_root, id_col, id_obj, request.args.to_dict())

    return x


@app.route("/<string:api_root>/collections/<string:id_col>/objects/<string:id_obj>/versions/", methods=["GET"])
@auth.login_required
def get_api_root_collections_object_by_id_versions(api_root, id_col, id_obj):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)
    taxii_col_exist(api_root, id_col)

    x = p.get_api_root_collections_object_by_id_versions(api_root, id_col, id_obj, request.args.to_dict())

    return x


@app.route("/<string:api_root>/collections/<string:id_col>/objects/", methods=["POST"])
@auth.login_required
def add_api_root_collections_object(api_root, id_col):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)
    taxii_col_exist(api_root, id_col)

    obj = request.get_json()
    x = p.add_api_root_collections_object(api_root, id_col, obj)

    return x


@app.route("/<string:api_root>/collections/<string:id_col>/manifest/", methods=["GET"])
@auth.login_required
def get_api_root_collections_manifest(api_root, id_col):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)
    taxii_col_exist(api_root, id_col)

    x = p.get_api_root_collections_manifest(api_root, id_col, request.args.to_dict())

    return x


@app.route("/<string:api_root>/status/<string:id_status>/", methods=["GET"])
@auth.login_required
def get_api_root_status_by_id(api_root, id_status):
    validate_version_parameter_in_accept_header()
    api_root_exist(api_root)

    x = p.get_api_root_status_by_id(api_root, id_status)

    return x


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6100, debug=True)
