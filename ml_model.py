import joblib
import re
import string

# تحميل الموديل و الـ vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("preprocessor.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def heuristic_analysis(text, lang='ar'):
    reasons = []
    text_lower = text.lower()

    # نص قصير جداً
    if len(text.strip()) < 12:
        if lang == 'ar':
            reasons.append("النص قصير جداً")
        else:
            reasons.append("Text is very short")

    # روابط مشبوهة
    if "http://" in text_lower or "https://" in text_lower or "www." in text_lower:
        if lang == 'ar':
            reasons.append("يحتوي على رابط ويب خارجي")
        else:
            reasons.append("Contains external web link")

    # كلمات حساسة حسب اللغة
    if lang == 'ar':
        phishing_keywords = ["تحقق", "حساب", "تسجيل", "كلمة سر", "بنك", "عاجل", 
                           "تأكيد", "أمن", "انقر", "تحديث", "باي بال", "معلق", 
                           "محدود", "تحذير", "مطلوب", "فوري"]
    else:
        phishing_keywords = ["verify", "account", "login", "password", "bank", "urgent",
                           "confirm", "security", "click", "update", "paypal", "suspended",
                           "limited", "alert", "action required", "immediately"]
    
    found_keywords = []
    for keyword in phishing_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    if found_keywords:
        if lang == 'ar':
            reasons.append(f"يحتوي على كلمات مشبوهة: {', '.join(found_keywords[:3])}")
        else:
            reasons.append(f"Contains suspicious words: {', '.join(found_keywords[:3])}")

    return reasons

def predict(text, lang='ar'):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    
    phishing_prob = model.predict_proba(vec)[0][1]
    reasons = heuristic_analysis(text, lang)
    
    if phishing_prob < 0.3:
        label = "safe"
        if not reasons:
            if lang == 'ar':
                reasons.append("لا توجد مؤشرات تصيد واضحة")
            else:
                reasons.append("No clear phishing indicators")
                
    elif phishing_prob < 0.7:
        label = "suspicious"
        if not reasons:
            if lang == 'ar':
                reasons.append("يحتوي على بعض العلامات المشبوهة")
            else:
                reasons.append("Contains some suspicious signs")
                
    else:
        label = "phishing"
        if not reasons:
            if lang == 'ar':
                reasons.append("احتمال عالي للتصيد الاحتيالي")
            else:
                reasons.append("High probability of phishing")
    
    return {
        "label": label,
        "score": round(float(phishing_prob), 3),
        "reasons": reasons[:5]
    }
