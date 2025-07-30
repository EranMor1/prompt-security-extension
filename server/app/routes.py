# Routes for handling PDF upload and inspection requests
"""
Flask routes for handling PDF inspection and health checks.
"""
import os

from flask import Blueprint, request, jsonify
import tempfile
from .services.inspect_pdf import inspect_pdf
from .logger import logger

routes = Blueprint("routes", __name__)

@routes.route("/inspect", methods=["POST"])
def inspect():
    print("got request")
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file_storage = request.files['file']
    filename = file_storage.filename

    # Save the uploaded file to a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            file_storage.save(tmp.name)
            tmp_path = tmp.name
    except Exception as e:
        logger.exception("Failed to save uploaded file to temp")
        return jsonify({"error": f"Failed to save file: {e}"}), 500

    try:
        # Re-open the temporary file for inspection
        with open(tmp_path, 'rb') as tmp_file:
            result = inspect_pdf(tmp_file)
    except Exception as e:
        logger.exception("Error processing PDF")
        return jsonify({"error": f"Inspection error: {e}"}), 500
    finally:
        # Clean up temp file
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    return jsonify(result)

