import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
data = pd.read_csv("train.csv")

# Take ONLY comment_text column
comments = data["comment_text"]

# Create TF-IDF object
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

# Convert text to numbers
X = vectorizer.fit_transform(comments)

print("Text converted to numbers!")
print("Shape of data:", X.shape)