Fake News Detection using Machine Learning and Gemini AI

This project is a web application that classifies news articles as fake or real using a machine learning model. To make the predictions more understandable, it also uses Gemini AI to provide explanations and insights.

Key Features
Classifies news articles as fake or real using a trained machine learning model
Displays a confidence score for each prediction
Highlights suspicious or unusual words in the input text
Uses Gemini AI to generate explanations and reasoning for the prediction
Combines machine learning with language models to improve interpretability
Stores recent analyses for reference


Tech Stack
Backend: Flask (Python)
Machine Learning: Scikit-learn
NLP Processing: NLTK
AI Model: Gemini AI
Frontend: HTML, CSS


How It Works
The user enters a news article into the application
The text is preprocessed by:
Converting to lowercase
Removing special characters
Eliminating stopwords
The cleaned text is converted into numerical features using TF-IDF
The machine learning model predicts whether the news is fake or real and provides a confidence score


Gemini AI analyzes the same input to:
Understand context
Identify suspicious patterns
Provide a short explanation


The final output includes:
Prediction result
Confidence score
Explanation
Highlighted suspicious words
Running the Project Locally


Install the required dependencies:
pip install flask nltk scikit-learn google-generativeai


Set your Gemini API key:
set GEMINI_API_KEY=your_api_key


Run the application:
python app.py


Open the application in your browser:
http://127.0.0.1:5000/

Demo:


<img width="929" height="856" alt="image" src="https://github.com/user-attachments/assets/72c78367-7d1a-4033-8021-3b501e344846" />
<img width="915" height="683" alt="image" src="https://github.com/user-attachments/assets/771a511b-a2c0-436d-bcc7-01a537ed2950" />
