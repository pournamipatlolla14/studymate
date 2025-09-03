import streamlit as st
import PyPDF2
import nltk
import re
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import random

nltk.download("punkt", quiet=True)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

def summarize_text(text, num_sentences=5):
    """Simple bullet point summary (frequency-based)"""
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text.lower())
    freq = nltk.FreqDist(words)
    ranked_sentences = sorted(
        sentences, key=lambda s: sum(freq[w] for w in nltk.word_tokenize(s.lower()) if w in freq), reverse=True
    )
    return ranked_sentences[:num_sentences]

def generate_mindmap(text):
    """Generate a simple mindmap graph of keywords"""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq = nltk.FreqDist(words)
    common_words = [w for w, _ in freq.most_common(10)]

    G = nx.Graph()
    for word in common_words:
        G.add_node(word)
    for i in range(len(common_words)):
        for j in range(i+1, len(common_words)):
            if random.random() > 0.5:  # Random connections for visualization
                G.add_edge(common_words[i], common_words[j])

    # Plot the mindmap
    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000, font_size=10, ax=ax)
    return fig

def generate_quiz(text, num_q=5):
    """Generate quiz questions from text"""
    sentences = nltk.sent_tokenize(text)
    quiz = []
    for _ in range(min(num_q, len(sentences))):
        sent = random.choice(sentences)
        words = sent.split()
        if len(words) > 5:
            blank_idx = random.randint(0, len(words)-1)
            answer = words[blank_idx]
            words[blank_idx] = "____"
            quiz.append((" ".join(words), answer))
    return quiz


st.title("📘 StudyMate: AI-Powered Study Assistant")
st.write("Upload a PDF to get **summaries, mindmaps, and quiz questions** 🎯")

pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

if pdf_file:
    text = extract_text_from_pdf(pdf_file)

    st.subheader("📌 Summary (Bullet Points)")
    summary = summarize_text(text)
    for s in summary:
        st.markdown(f"- {s}")

    st.subheader("🧠 Mindmap")
    fig = generate_mindmap(text)
    st.pyplot(fig)

    st.subheader("❓ Quiz Questions")
    quiz = generate_quiz(text)
    for idx, (q, ans) in enumerate(quiz, 1):
        st.markdown(f"**Q{idx}.** {q}")
        with st.expander("Show Answer"):
            st.write(ans)
