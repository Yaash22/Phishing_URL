import streamlit as st
import joblib
import os
import re
import tldextract

# Load model
model_path = os.path.join("model", "phishing_model.pkl")
model = joblib.load(model_path)

# Define feature extraction function
def extract_features(url):
    features = {}

    # Length of URL
    features['url_length'] = len(url)

    # Presence of IP address
    ip_regex = re.compile(
        r"^(http://|https://)?(\d{1,3}\.){3}\d{1,3}(/|:\d+)?([/?].*)?$")
    features['has_ip'] = 1 if ip_regex.match(url) else 0

    # Presence of '@' symbol
    features['has_at_symbol'] = 1 if '@' in url else 0

    # Count of dots
    features['count_dots'] = url.count('.')

    # Count of hyphens
    features['count_hyphens'] = url.count('-')

    # Count of slashes
    features['count_slashes'] = url.count('/')

    # Count of subdirectories
    features['count_subdirs'] = url.count('/')

    # Length of domain
    domain = tldextract.extract(url).domain
    features['domain_length'] = len(domain)

    return list(features.values())

# Streamlit UI
st.set_page_config(page_title="Phishing URL Detector", layout="centered")
st.title("🔍 Phishing URL Detector")
st.markdown("Enter a URL below to check whether it's **legitimate** or a **phishing** attempt.")

url_input = st.text_input("Enter URL:", "")

if url_input:
    try:
        features = extract_features(url_input)
        prediction = model.predict([features])[0]

        if prediction == 1:
            st.error("⚠️ The URL appears to be **phishing**. Do not click!")
        else:
            st.success("✅ The URL appears to be **safe**.")
    except Exception as e:
        st.error(f"Error: {e}")
