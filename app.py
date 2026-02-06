from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_model import predict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API is running",
        "name": "Phishing Email Detector API",
        "version": "1.0.0",
        "language_support": "Arabic & English"
    })

@app.route("/predict", methods=["POST", "GET"])
def predict_email():
    if request.method == "GET":
        return jsonify({
            "message": "Use POST method with JSON: {'text': 'email content', 'lang': 'ar/en'}"
        })
    
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if not data or "text" not in data:
            return jsonify({
                "error": "No text provided",
                "success": False,
                "code": 400
            }), 400
        
        text = data["text"]
        
        if not text or text.strip() == "":
            return jsonify({
                "error": "Empty text",
                "success": False,
                "code": 400
            }), 400
        
        # تحديد اللغة (افتراضي: عربي)
        lang = data.get("lang", "ar")
        if lang not in ["ar", "en"]:
            lang = "ar"
        
        # تحليل النص
        result = predict(text, lang)
        
        # إضافة معلومات إضافية
        result.update({
            "success": True,
            "text_length": len(text),
            "language": lang,
            "model_version": "1.0.0"
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False,
            "code": 500
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
