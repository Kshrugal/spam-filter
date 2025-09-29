from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd



df = pd.read_csv("data/spam_ham_dataset.csv")

useful = df.iloc[:, [1, 2]]
X = useful.iloc[:, 1]
y = useful.iloc[:, 0]


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=13)

vector = TfidfVectorizer()
X_train_vector = vector.fit_transform(X_train)
X_test_vector = vector.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vector, y_train)

output = model.predict(X_test_vector)

print(accuracy_score(y_test, output))
print(confusion_matrix(y_test, output))