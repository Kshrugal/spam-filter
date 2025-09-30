import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


model = joblib.load("logistic_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

new_df = pd.read_csv("data/testing_emails.csv", encoding="latin1")

X_new = new_df['text']
y_new = new_df['label']
X_new_vector = vectorizer.transform(X_new) 
predictions = model.predict(X_new_vector)

print("Accuracy:", accuracy_score(y_new, predictions))
print(confusion_matrix(y_new, predictions))
print(classification_report(y_new, predictions))