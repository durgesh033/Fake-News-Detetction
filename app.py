import streamlit as st
import pickle
import re
import string
import trafilatura

# Load Models

model = pickle.load(open("Models\logistic_model.pkl", "rb"))
vectorizer = pickle.load(open("Models/tfidf_vectorizer.pkl", "rb"))

# Clean Text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# Page Details

st.set_page_config(
    page_title="Fake News Detection",
    page_icon="📰",
    layout="centered"
)

# Title

st.title("📰 Fake News Detection System")
st.write("Analyze news articles using Machine Learning and NLP")
st.divider()  # draw a horizontal line

# SideBar

st.sidebar.title("About Project")
st.sidebar.write(
    """
    This project uses NLP and Machine Learning
    to analyze news articles based on linguistic
    patterns and source credibility.

    Features:
    - TF-IDF Vectorization
    - Logistic Regression
    - URL-based Analysis
    - Source Credibility Detection
    """
)

# Input Mode

option = st.radio("Choose Input Mode", ["Paste Text", "News URL"])
news = ""

# Text Input

if option == "Paste Text":

    news = st.text_area("Enter News Article", height=250)

#URL Input

elif option == "News URL":
    url = st.text_input("Enter News URL")
    if url:
        try:
            downloaded = trafilatura.fetch_url(url)
            news = trafilatura.extract(downloaded)

            if not news:
                st.error("Could not extract article")

            #Source Credibility Check
            else: 
                trusted_sources = [
                "reuters.com",
                "bbc.com",
                "apnews.com",
                "nasa.gov",
                "thehindu.com",
                "indiatoday.in",
                "ndtv.com",
                "who.int"
            ]

            source_found = False
            
            for source in trusted_sources:
                if source in url:
                    st.success(f"Trusted Source Detected: {source}")
                    source_found = True
                    break

            if not source_found:
                st.warning("Unknown or Unverified News Source")

            st.subheader("Extracted Article")
            st.write(news[:1500])

        except:
            st.error("Could not extract article from URL")


#PREDICTION

if st.button("Predict"):
    if not news or news.strip() == "":
        st.warning("Please enter text or URL")

    else:
        cleaned_news = clean_text(news)
        vectorized_news = vectorizer.transform([cleaned_news])
        prediction = model.predict(vectorized_news)
        probability = model.predict_proba(vectorized_news)
        confidence = max(probability[0]) * 100
        st.divider()
        
        st.subheader("Prediction Result")
        real_prob = probability[0][1]

        if real_prob > 0.6:
            st.success("Real News")
        else :
            st.error("Fake News")

        st.write(f"Confidence Scoree: {confidence:.2f}%")
        st.progress(int(confidence))

        # Extra Analysis

        word_count = len(news.split())
        st.write(f"Word Count: {word_count}")

# DISCLAIMER

st.info(
    "This system performs NLP-based classification "
    "using linguistic patterns and source analysis. "
    "Predictions may not represent factual verification."
)

#FOOTER

st.divider()
st.caption("Developed using Maachine Learning, NLP, and StreamLit")