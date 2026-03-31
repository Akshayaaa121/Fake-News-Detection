from flask import Flask, render_template, request, session, jsonify
import pickle
import re
import nltk
from nltk.corpus import stopwords
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Configure Gemini with your API key and choose the model
genai.configure(api_key="AIzaSyBjL8OtN-d0WH24luaZfDMf67SWtYztnkM")  
model_gemini = genai.GenerativeModel("gemini-1.5-pro")

# Configure Gemini with your API key and choose the model
model = pickle.load(open("fake_news_model.pkl", "rb"))
vectorizer = pickle.load(open("fake_news_vectorizer.pkl", "rb"))


nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Clean and prepare input text before feeding it to the ML model

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = ' '.join([w for w in text.split() if w not in stop_words])
    return text
-
def highlight_suspicious(text):
    words = text.split()
    highlighted = []

    for w in words:
        if w.lower() not in stop_words and len(w) > 6:
            highlighted.append(f"<span class='suspicious'>{w}</span>")
        else:
            highlighted.append(w)

    return " ".join(highlighted)

def explain_prediction(text):
    fake_keywords = ["shocking", "breaking", "secret", "exposed", "viral"]
    found = [w for w in fake_keywords if w in text.lower()]

    if found:
        return f"⚠️ Suspicious keywords detected: {', '.join(found)}"
    return "✅ No strong fake indicators found."

# Load the trained fake news classification model and vectorizer
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

# Use Gemini AI to generate a deeper explanation and summary
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
            # Prediction
            processed = preprocess(news_text)
            vect = vectorizer.transform([processed])

            pred = model.predict(vect)[0]
            pred_proba = model.predict_proba(vect)[0]

            confidence = round(max(pred_proba) * 100, 2)
            prediction = "Fake News" if pred == 1 else "Real News"

            
            explanation = explain_prediction(news_text)

            
            highlighted_text = highlight_suspicious(news_text)

            
            gemini_output = gemini_analysis(news_text)

           
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
