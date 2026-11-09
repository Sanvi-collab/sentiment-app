import re
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

st.set_page_config(page_title="Sentiment Analysis Tool", page_icon="😊")
st.title("😊 Sentiment Analysis Tool")
st.write("Type a sentence and find out if it sounds Positive, Negative or Neutral.")

if "history" not in st.session_state:
    st.session_state.history = []


def classify(score):
    if score >= 0.05:
        return "Positive", "😊"
    if score <= -0.05:
        return "Negative", "😠"
    return "Neutral", "😐"


text = st.text_area("Your sentence:", placeholder="e.g. I love this school!")

if st.button("Analyze"):
    if not text.strip():
        st.warning("Please type a sentence first.")
    else:
        score = analyzer.polarity_scores(text)["compound"]
        label, emoji = classify(score)

        st.subheader(f"{emoji} {label}")
        st.write(f"Score: *{score:.2f}* (from -1 very negative to +1 very positive)")
        st.progress((score + 1) / 2)

        pos_words, neg_words = [], []
        for word in re.findall(r"[A-Za-z']+", text.lower()):
            value = analyzer.lexicon.get(word)
            if value is not None:
                if value > 0:
                    pos_words.append(word)
                elif value < 0:
                    neg_words.append(word)

        if pos_words:
            st.success("Positive words: " + ", ".join(pos_words))
        if neg_words:
            st.error("Negative words: " + ", ".join(neg_words))

        st.session_state.history.append(
            {"Sentence": text, "Label": f"{emoji} {label}", "Score": round(score, 2)}
        )

if st.session_state.history:
    st.divider()
    st.subheader("History")
    st.dataframe(st.session_state.history, use_container_width=True)
    if st.button("Clear history"):
        st.session_state.history = []
        st.rerun()

with st.expander("Try these test sentences"):
    st.write("- I love this school!")
    st.write("- This food is terrible.")
    st.write("- The class starts at 9.")
    st.write("- The movie was not bad.")
    st.write("- Great, another Monday 🙄 (sarcasm: the tool may get this wrong!)")
