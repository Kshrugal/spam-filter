import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

model = joblib.load("src/logistic_model.pkl")
vectorizer = joblib.load("src/vectorizer.pkl")

# Load new dataset
new_df = pd.read_csv("data/testing_emails.csv")

#labels
X_new = new_df['text']
y_new = new_df['label']

# same vectorizer
X_new_vector = vectorizer.transform(X_new)

# Predict
y_pred = model.predict(X_new_vector)

# Accuracy and reports
print("Accuracy on new dataset: {:.2f}%".format(accuracy_score(y_new, y_pred) * 100))
print("\nConfusion Matrix:\n", confusion_matrix(y_new, y_pred))
print("\nClassification Report:\n", classification_report(y_new, y_pred))