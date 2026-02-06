import joblib
import re
import string

# تحميل الموديل و الـ vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("preprocessor.pkl")


# تنظيف النص
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


# تحليل منطقي (Rule-Based) لإعطاء أسباب
def heuristic_analysis(text):
    reasons = []
    text_lower = text.lower()

    # نص قصير جداً
    if len(text.strip()) < 12:
        reasons.append("النص قصير وغير شائع في رسائل التصيد الاحتيالي")

    # روابط
    if "http" in text_lower or "www" in text_lower:
        reasons.append("يحتوي على رابط خارجي قد يكون مشبوهاً")

    # كلمات حساسة
    phishing_words = [
        "verify", "account", "login", "password",
        "bank", "urgent", "confirm", "security",
        "click", "update"
    ]

    for word in phishing_words:
        if word in text_lower:
            reasons.append(f"يحتوي على كلمة مشبوهة: {word}")

    return reasons


# الدالة الرئيسية للتنبؤ
def predict(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])

    # احتمال الفيشينغ من الموديل
    phishing_probability = model.predict_proba(vec)[0][1]

    # تحليل منطقي
    reasons = heuristic_analysis(text)

    # قرار ذكي (مش أعمى)
    if phishing_probability < 0.4 and not reasons:
        label = "safe"
        reasons.append("لا توجد مؤشرات تصيد واضحة في النص")

    elif phishing_probability >= 0.75:
        label = "phishing"
        if not reasons:
            reasons.append("النموذج الإحصائي صنّف النص كتصيد احتيالي")

    else:
        label = "suspicious"
        reasons.append("النص يحتوي مؤشرات غير حاسمة ويتطلب الحذر")

    return {
        "label": label,
        "score": round(float(phishing_probability), 3),
        "reasons": reasons
    }
