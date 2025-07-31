# Routes for handling PDF upload and inspection requests
from flask import Blueprint, request, jsonify

from .services.inspect_pdf import inspect_pdf
from .logger import logger

routes = Blueprint("routes", __name__)

@routes.route("/inspect", methods=["POST"])
def inspect():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file_storage = request.files['file']
    filename = file_storage.filename
    result = inspect_pdf(file_storage, filename)



    return jsonify(result)

