# 🧠 Fake News Detection using Machine Learning + Gemini AI

An intelligent web application that classifies news articles as **Fake or Real** using Machine Learning, enhanced with **Gemini AI-powered reasoning** for explainability.

---

## 🚀 Key Features

- 📰 **Fake vs Real Classification** using trained ML model  
- 📊 **Confidence Score** to measure prediction reliability  
- 🔍 **Suspicious Word Highlighting** for quick pattern detection  
- 🤖 **Gemini AI Analysis** for human-like explanation and reasoning  
- 🧠 **Explainable AI System** combining ML + LLM insights  
- 📜 **Session History Tracking** of recent analyses  

---

## 🛠️ Tech Stack

| Layer              | Technology |
|-------------------|-----------|
| Backend            | Flask (Python) |
| Machine Learning   | Scikit-learn |
| NLP Processing     | NLTK |
| AI Model           | Gemini AI |
| Frontend           | HTML, CSS |

---

## ⚙️ How It Works

1. User inputs a news article  
2. Text is preprocessed:
   - Lowercasing  
   - Removing special characters  
   - Stopword removal  
3. Data is vectorized using ML pipeline  
4. ML model predicts:
   - Fake / Real  
   - Confidence score  
5. Gemini AI analyzes:
   - Context  
   - Writing style  
   - Suspicious language patterns  
6. Final output shows:
   - Prediction  
   - Confidence  
   - Explanation  
   - Highlighted suspicious words  

---

## ▶️ Run Locally

### 1️⃣ Install dependencies
```bash
pip install flask nltk scikit-learn google-generativeai

2️⃣ Set Gemini API Key
set GEMINI_API_KEY=your_api_key

3️⃣ Run the application
python app.py

4️⃣ Open in browser
http://127.0.0.1:5000/

📸 Demo
<img width="929" height="856" alt="image" src="https://github.com/user-attachments/assets/72c78367-7d1a-4033-8021-3b501e344846" />
<img width="915" height="683" alt="image" src="https://github.com/user-attachments/assets/771a511b-a2c0-436d-bcc7-01a537ed2950" />
