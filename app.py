import streamlit as st
import pickle
import re
import string

model = pickle.load(open("logistic_model.pkl", "rb"))

vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

st.title("📰 Fake News Detection System")
st.write("Enter a news article below to check whether it is Fake or Real.")
news = st.text_area("Enter News Article")

if st.button("Predict"):
    cleaned_news = clean_text(news)
    vectorized_news = vectorizer.transform([cleaned_news])
    prediction = model.predict(vectorized_news)
    if prediction[0] == 0:
        st.error("Fake News")

    else:
        st.success("Real News")