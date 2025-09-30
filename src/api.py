from flask import Flask, request, jsonify
import joblib

# Load model and vectorizer
model = joblib.load("logistic_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Spam Classifier API is running 🚀"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("message", "")

        if not text.strip():
            return jsonify({"error": "Message is empty"}), 400

        # Transform text using vectorizer
        input_vector = vectorizer.transform([text])
        prediction = model.predict(input_vector)[0]

        result = "spam" if prediction == 1 else "ham"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
