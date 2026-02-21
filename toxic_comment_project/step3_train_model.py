import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("train.csv")

# Input (comments)
X_text = data["comment_text"]

# Output (labels)
y = data["toxic"]

# Convert text to numbers
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X = vectorizer.fit_transform(X_text)

# Create ML model
model = LogisticRegression(max_iter=1000)

# Train model
model.fit(X, y)

print("✅ Model training completed")