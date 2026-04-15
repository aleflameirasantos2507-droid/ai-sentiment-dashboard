import pandas as pd
import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator


def analyze_polarity(text):
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)
    analysis = TextBlob(translated_text)
    return analysis.sentiment.polarity, translated_text


def classify_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

#TYPING SENTENCES

st.title("AI Sentiment Analyzer")
st.write("Analyze sentiment from text or files.")

st.header("Analyze a sentence")

user_text = st.text_area("Type your sentence:")

if st.button("Analyze Text"):
    if user_text.strip() == "":
        st.warning("Please enter a sentence.")
    else:
        score, translated = analyze_polarity(user_text)
        sentiment = classify_sentiment(score)

        st.subheader("Result")

        if sentiment == "Positive":
            st.success(f"Sentiment: {sentiment}")
        elif sentiment == "Negative":
            st.error(f"Sentiment: {sentiment}")
        else:
            st.info(f"Sentiment: {sentiment}")

        st.write(f"Score: {score:.2f}")
        st.write(f"Translated: {translated}")

#.TXT FILE

positive = []
negative = []
neutral = []

st.header("Analyze a .txt file")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    lines = content.split("\n")

    st.subheader("File Analysis")

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        score, _ = analyze_polarity(line)
        sentiment = classify_sentiment(score)

        st.write(f"{line} → {sentiment} ({score:.2f})")
        if sentiment == 'Positive':
            positive.append(line)
        elif sentiment == 'Negative':
            negative.append(line)
        else:
            neutral.append(line)

    total = len(positive) + len(negative) + len(neutral)
    st.subheader(' FINAL REPORT ')
    st.success(f"--> Positive sentences: {len(positive)} [{(len(positive) / total) * 100:.2f}%]")
    st.error(f"--> Negative sentences: {len(negative)} [{(len(negative) / total) * 100:.2f}%]")
    st.info(f"--> Neutral sentences: {len(neutral)} [{(len(neutral) / total) * 100:.2f}%]")

    chart_data = pd.DataFrame({
        'Sentiment': ['Positive','Negative','Neutral'],
        'Count': [len(positive), len(negative), len(neutral)]
    })

    st.subheader('Sentiment Distribuction')
    st.bar_chart(chart_data.set_index('Sentiment'))