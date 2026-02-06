from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_model import predict
import request

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API is running"})

@app.route("/predict", methods=["POST"])
def predict_email():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]

    if text.strip() == "":
        return jsonify({"error": "Empty text"}), 400

    result = predict(text)
    return jsonify(result)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
