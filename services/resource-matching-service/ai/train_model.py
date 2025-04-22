# ai/train_model.py

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from .data_loader import load_data
from config.settings import settings

# Load the data
X_raw, y_train = load_data()

# Vectorize the input text
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_raw)

# === DEBUG: inspect the learned vocabulary ===
print("Vocabulary size:", len(vectorizer.vocabulary_))
# print first 10 terms
print("First 10 feature names:", list(vectorizer.get_feature_names_out())[:10])
# =============================================

# Train the KNN model
knn = KNeighborsClassifier(n_neighbors=settings.knn_n_neighbors,  metric="cosine", algorithm="brute")
knn.fit(X_train, y_train)

# Save the trained model and vectorizer
with open(settings.model_path, 'wb') as f:
    pickle.dump(knn, f)

with open(settings.transformer_path, 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and transformer saved successfully.")

