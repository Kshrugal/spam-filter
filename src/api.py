from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)  # 🚀 allow requests from Chrome extension

# Load model and vectorizer
model = joblib.load("logistic_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data["message"]
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)[0]
    confidence = model.predict_proba(vector).max() * 100

    return jsonify({
        "prediction": "spam" if prediction == 1 else "ham",
        "confidence": round(confidence, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
