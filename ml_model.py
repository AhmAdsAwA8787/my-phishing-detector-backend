import joblib
import re
import string

model = joblib.load("model.pkl")
vectorizer = joblib.load("preprocessor.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def predict(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])

    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0][1]

    return {
        "label": "phishing" if prediction == 1 else "safe",
        "score": round(float(probability), 3)
    }
    