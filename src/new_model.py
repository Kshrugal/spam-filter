from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import joblib

df = pd.read_csv("data/emails.csv")
df = df.dropna()
X = df["text"]
y = df["spam"]



X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=9)

vector = TfidfVectorizer()
X_train_vector = vector.fit_transform(X_train)
X_test_vector = vector.transform(X_test)

dd = MultinomialNB()
dd.fit(X_train_vector, y_train)

output = dd.predict(X_test_vector)

joblib.dump(dd, "logistic_model2.pkl")
joblib.dump(vector, "vectorizer2.pkl")

print("Accuracy:", accuracy_score(y_test, output))