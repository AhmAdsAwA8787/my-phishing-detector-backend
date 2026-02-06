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

    text = data["text"].strip()

    if text == "":
        return jsonify({"error": "Empty text"}), 400

    # 1️⃣ تحليل داخلي بالذكاء الاصطناعي
    local_result = predict(text)

    # 2️⃣ إرسال الإيميل إلى موقعك الخارجي
    external_api_url = "https://رهقعسفخفشم/predict"

    try:
        external_response = requests.post(
            external_api_url,
            json={"email_text": text},
            timeout=10
        )

        external_report = external_response.json()

    except Exception as e:
        external_report = {"error": "External site not reachable"}

    # 3️⃣ دمج التقريرين وإرجاعهم
    return jsonify({
        "local_ai_result": local_result,
        "external_site_report": external_report
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
