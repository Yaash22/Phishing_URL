# train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

df = pd.read_csv("data/phishing.csv")
if 'Index' in df.columns:
    df.drop(columns=['Index'], inplace=True)

X = df.drop(columns=["class"])
y = df["class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
with open("model/phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to model/phishing_model.pkl")
