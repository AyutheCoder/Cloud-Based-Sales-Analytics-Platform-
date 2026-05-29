import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from google.cloud import storage
import firebase_admin
from firebase_admin import auth

app = Flask(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins_list = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]
CORS(app, resources={r"/api/*": {"origins": allowed_origins_list or "*"}})

# Configure the GCS bucket name
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "bkt-sales-data")

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
if firebase_project_id:
    firebase_admin.initialize_app(options={"projectId": firebase_project_id})
else:
    firebase_admin.initialize_app()


def _verify_firebase_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Missing bearer token"}), 401)

    token = auth_header.replace("Bearer ", "", 1).strip()
    try:
        decoded = auth.verify_id_token(token)
        return decoded, None
    except Exception:
        return None, (jsonify({"error": "Invalid or expired token"}), 401)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


@app.route("/api/upload", methods=["POST"])
def upload_file_api():
    _, error_response = _verify_firebase_token()
    if error_response:
        return error_response

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    return jsonify({"message": f"File {file.filename} uploaded to {GCS_BUCKET_NAME}."})


@app.route("/", methods=["GET"]) 
def upload_file_form():
    return render_template("index.html")

if __name__ == "__main__":
    # Ensure the environment variable for the GCS service account key is set
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
