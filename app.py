import spacy
import joblib
import numpy as np
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
model =joblib.load('model.pkl')

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

symptom_responses = {
    "fever": "It's important to rest, stay hydrated, and take over-the-counter fever reducers like acetaminophen.",
    "cold": "To manage a cold, get plenty of rest, drink fluids, and consider over-the-counter cold remedies.",
    "cough": "drink and sour hotwater.",
    "headache": "For a headache, try resting in a quiet, dark room and taking an over-the-counter pain reliever.",
    "body pain": "For body pain, consider rest and over-the-counter pain relievers like ibuprofen.",
    # Add more symptoms and responses as needed
}

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.json.get('user_input')
        response = get_chatbot_response(user_input)
        doc = nlp(user_input.lower())
        medi = []
        for token in doc:
            if token.text in symptom_responses:
                medi = medicine(user_input)
        return jsonify({"response": response, "medicine": str(medi)})  # No need to call .tolist() on medi
    return app.send_static_file('index.html')

def get_chatbot_response(user_input):
    # Process user input with spaCy for NLP
    doc = nlp(user_input.lower())

    for token in doc:
        if token.text in symptom_responses:
            return symptom_responses[token.text]

    return "I'm here to provide information. Please enter a symptom like fever, cold, headache, or body pain."

def medicine(user_input):
    # Process user input with spaCy for NLP
    doc = nlp(user_input.lower())

    # Extract symptoms from user input
    symptoms = []
    for token in doc:
        if token.text in symptom_responses:
            symptoms.append(token.text)

    # Create an array with symptoms and a placeholder for medicine
    symptom_array = [1 if symptom in symptoms else 0 for symptom in symptom_responses]
    symptom_array = np.array(symptom_array).reshape(1, -1) 
    medicine=model.predict(symptom_array)
    return medicine
# ... (the rest of your Flask app code)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
