import streamlit as st
import pickle
from utils.features import extract_features
import datetime

# Load model
with open("model/phishing_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🔐 Phishing URL Detector")
st.markdown("Enter a URL to check if it's phishing or legitimate.")

# Initialize session history if it doesn't exist
if "history" not in st.session_state:
    st.session_state.history = []

url = st.text_input("🌐 Enter URL", placeholder="https://example.com")

if st.button("Predict"):
    if url:
        features = extract_features(url)
        prediction = model.predict([features])[0]

        # Prepare prediction message
        if prediction == 1:
            result_message = "🟢 This website is **Legitimate**."
            st.success(result_message)
        else:
            result_message = "🔴 This website is **Phishing**."
            st.error(result_message)

        # Generate report
        report = f"""
        🔍 Phishing URL Detection Report  
        ====================================  
        📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

        🌐 URL Checked: {url}  

        📊 Detection Result: {'Legitimate' if prediction == 1 else 'Phishing'}  

        📈 Model Used: RandomForestClassifier  
        📑 Total Features Extracted: {len(features)}  

        ✅ Suggestion: Always double-check URLs before entering sensitive information.  
        """

        # Show and download report
        st.markdown("### 📄 Detection Report")
        st.text(report)
        st.download_button(
            label="📥 Download Report",
            data=report,
            file_name=f"phishing_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # Add to session history
        st.session_state.history.append({
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "url": url,
            "result": "Legitimate" if prediction == 1 else "Phishing"
        })

    else:
        st.warning("Please enter a valid URL.")

# Sidebar session history tab
with st.sidebar:
    st.title("📜 Session History")
    if st.session_state.history:
        for record in reversed(st.session_state.history):
            st.markdown(f"""
            **🕒 {record['timestamp']}**
            - 🌐 `{record['url']}`
            - 📊 **{record['result']}**
            ---
            """)
    else:
        st.info("No URLs checked yet this session.")
