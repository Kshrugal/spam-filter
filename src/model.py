import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

df1 = pd.read_csv("data/mail_data.csv")
df2 = pd.read_csv("data/spam_ham_dataset.csv")
df3 = pd.read_csv("data/generated_emails.csv")

# combine data
combined_df = pd.concat([df1, df2, df3], ignore_index=True)
combined_df = combined_df.dropna()

# labels
X = combined_df["text"]
y = combined_df["label"]

#train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=13
)

#vectorize
vectorizer = TfidfVectorizer()
X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

#train logistic regression
model = LogisticRegression()
model.fit(X_train_vector, y_train)

#predict plis print results
y_pred = model.predict(X_test_vector)

print("Accuracy on combined dataset: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# save the model and vectorizer
joblib.dump(model, "src/logistic_model.pkl")
joblib.dump(vectorizer, "src/vectorizer.pkl")

