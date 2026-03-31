from flask import Flask, render_template, request, session, jsonify
import pickle
import re
import nltk
from nltk.corpus import stopwords
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ---------------- Gemini Setup ----------------
genai.configure(api_key="AIzaSyBjL8OtN-d0WH24luaZfDMf67SWtYztnkM")  # 🔑 replace with your key
model_gemini = genai.GenerativeModel("gemini-1.5-pro")

# ---------------- Load ML Model ----------------
model = pickle.load(open("fake_news_model.pkl", "rb"))
vectorizer = pickle.load(open("fake_news_vectorizer.pkl", "rb"))

# ---------------- Stopwords ----------------
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ---------------- Preprocessing ----------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = ' '.join([w for w in text.split() if w not in stop_words])
    return text

# ---------------- Highlight Suspicious Words ----------------
def highlight_suspicious(text):
    words = text.split()
    highlighted = []

    for w in words:
        if w.lower() not in stop_words and len(w) > 6:
            highlighted.append(f"<span class='suspicious'>{w}</span>")
        else:
            highlighted.append(w)

    return " ".join(highlighted)

# ---------------- Simple Explanation ----------------
def explain_prediction(text):
    fake_keywords = ["shocking", "breaking", "secret", "exposed", "viral"]
    found = [w for w in fake_keywords if w in text.lower()]

    if found:
        return f"⚠️ Suspicious keywords detected: {', '.join(found)}"
    return "✅ No strong fake indicators found."

# ---------------- Gemini AI Analysis ----------------
def gemini_analysis(text):
    try:
        prompt = f"""
        Analyze the following news article:

        1. Is it likely fake or real?
        2. Give reasoning
        3. Highlight suspicious patterns
        4. Provide a short summary

        News:
        {text}
        """

        response = model_gemini.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini API Error: {str(e)}"

# ---------------- Main Route ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    confidence = None
    explanation = None
    gemini_output = None
    news_text = ""
    highlighted_text = ""

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        news_text = request.form.get("news_text")

        if news_text:
            # ---------- ML Prediction ----------
            processed = preprocess(news_text)
            vect = vectorizer.transform([processed])

            pred = model.predict(vect)[0]
            pred_proba = model.predict_proba(vect)[0]

            confidence = round(max(pred_proba) * 100, 2)
            prediction = "Fake News" if pred == 1 else "Real News"

            # ---------- Custom Explanation ----------
            explanation = explain_prediction(news_text)

            # ---------- Highlight ----------
            highlighted_text = highlight_suspicious(news_text)

            # ---------- Gemini AI ----------
            gemini_output = gemini_analysis(news_text)

            # ---------- Save History ----------
            session["history"].append({
                "text": news_text,
                "prediction": prediction
            })
            session.modified = True

    return render_template(
        "real_time.html",
        prediction=prediction,
        confidence=confidence,
        explanation=explanation,
        news_text=news_text,
        highlighted_text=highlighted_text,
        gemini_output=gemini_output,
        history=session.get("history", [])
    )

# ---------------- API Endpoint ----------------
@app.route("/predict", methods=["POST"])
def api_predict():
    data = request.json.get("text")

    processed = preprocess(data)
    vect = vectorizer.transform([processed])
    pred = model.predict(vect)[0]

    return jsonify({"prediction": int(pred)})

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)