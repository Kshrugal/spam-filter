import streamlit as st
import joblib

# Load the model and vectorizer
model = joblib.load("logistic_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Title of the app
st.title("📧 Spam Email Classifier")

# Text input box
user_input = st.text_area("Enter an email/message:", "")

# When the user clicks the button
if st.button("Classify"):
    if user_input.strip() == "":
        st.warning("Please type a message first!")
    else:
        #  using the same vectorizer
        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)[0]

        # result
        if prediction == 1:
            st.error("🚨 This looks like SPAM!")
        else:
            st.success("✅ This looks like HAM (not spam).")