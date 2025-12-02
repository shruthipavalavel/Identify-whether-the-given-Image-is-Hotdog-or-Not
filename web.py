# web.py
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("HUGGING_FACE_API_URL")
API_TOKEN = os.getenv("HUGGING_FACE_API_KEY")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

app = Flask(__name__)

def query(image_bytes: bytes):
    # Send the raw image bytes to Hugging Face
    response = requests.post(API_URL, headers=headers, data=image_bytes)

    # Debug prints – super useful if something goes wrong
    print("HF status:", response.status_code)
    print("HF body:", response.text[:500])  # first 500 chars

    # Raise an error if the status code is not 2xx
    response.raise_for_status()

    # Parse JSON safely
    return response.json()


@app.route("/")
def index():
    # Assuming templates/index.html
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file1" not in request.files:
        return jsonify({"error": "No file part 'file1' in request"}), 400

    file = request.files["file1"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Read the image into bytes
    image_bytes = file.read()

    modeldata = query(image_bytes)
    return jsonify(modeldata)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
