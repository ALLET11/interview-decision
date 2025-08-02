# -*- coding: utf-8 -*-
import streamlit as st
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🌈 Styling
st.markdown("""
    <style>
    .stApp { background-color: #e6f2ff; }
    .result-box {
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .hire {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #155724;
    }
    .reject {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #721c24;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Interview Summarization & Hiring Decision App")

# Load model & encoder
pipeline = joblib.load('final_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Load CSV
try:
    summary_data = pd.read_csv(r"C:\Users\Allet\OneDrive\conversational_interviews_clean_final.csv")
except Exception as e:
    summary_data = pd.DataFrame()
    st.warning("Reference data file not found or failed to load.")

user_input = st.text_area("Paste the interview transcript here:")

if st.button("🔍 Predict Hiring Decision"):
    if user_input.strip() == "":
        st.warning("Please enter a transcript before predicting.")
    else:
        try:
            # Prediction
            prediction_encoded = pipeline.predict([user_input])[0]
            prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

            # Color-coded result
            if prediction_label.lower() == "hire":
                st.markdown(f'<div class="result-box hire">✅ Prediction: {prediction_label}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-box reject">❌ Prediction: {prediction_label}</div>', unsafe_allow_html=True)

            # Fuzzy match: vectorize all transcripts + find best match
            if 'interview_transcript' in summary_data.columns:
                vectorizer = TfidfVectorizer().fit(summary_data['interview_transcript'])
                transcript_vectors = vectorizer.transform(summary_data['interview_transcript'])
                user_vector = vectorizer.transform([user_input])

                similarity_scores = cosine_similarity(user_vector, transcript_vectors)
                best_match_index = similarity_scores.argmax()
                best_score = similarity_scores[0, best_match_index]

                if best_score > 0.7:  # confident match
                    matched_row = summary_data.iloc[best_match_index]
                    name = matched_row.get("name", "N/A")
                    designation = matched_row.get("designation", "N/A")

                    st.write(f"👤 **Candidate Name:** {name}")
                    st.write(f"🧑‍💼 **Applied Role:** {designation}")
                else:
                    st.info("Could not confidently match candidate details.")

            else:
                st.warning("Transcript column not found in CSV.")

        except Exception as e:
            st.error(f"Prediction error: {e}")
