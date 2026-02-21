import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("train.csv")

X_text = data["comment_text"]
y = data["toxic"]

# Convert text to numbers
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)
X = vectorizer.fit_transform(X_text)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# ---- TEST PART ----
test_comment = ["you are stupid"]

test_vector = vectorizer.transform(test_comment)
prediction = model.predict(test_vector)

if prediction[0] == 1:
    print("❌ Toxic comment detected")
else:
    print("✅ Normal comment")