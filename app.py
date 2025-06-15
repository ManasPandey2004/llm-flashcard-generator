import streamlit as st
st.set_page_config(page_title="LLM Flashcard Generator", layout="wide")
from transformers import pipeline
import PyPDF2
import json
import csv
import os
import textwrap

# Load summarization model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

# Extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Chunk large text into smaller parts
def chunk_text(text, chunk_size=3000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Generate flashcards from summarized text
def generate_flashcards(text, difficulty="Medium"):
    flashcards = []
    chunks = chunk_text(text)

    for chunk in chunks:
        summary = summarizer(chunk, max_length=512, min_length=100, do_sample=False)[0]['summary_text']
        sentences = summary.split(". ")

        for i in range(0, len(sentences) - 1, 2):
            question = f"What is meant by: {sentences[i].strip()}?"
            answer = sentences[i + 1].strip()
            flashcards.append({"question": question, "answer": answer, "difficulty": difficulty})
            if len(flashcards) >= 20:
                return flashcards

    return flashcards

# Export to CSV and JSON
def export_flashcards(flashcards):
    os.makedirs("output", exist_ok=True)

    with open("output/flashcards.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["question", "answer", "difficulty"])
        writer.writeheader()
        for card in flashcards:
            writer.writerow(card)

    with open("output/flashcards.json", "w", encoding="utf-8") as jsonfile:
        json.dump(flashcards, jsonfile, indent=4)

# Flashcard display component
def display_flashcard(card, index):
    st.markdown(f"### ❓ Flashcard {index+1}")
    st.markdown(f"**Q:** {card['question']}")
    st.markdown(f"**A:** {card['answer']}")
    st.markdown(f"🟩 **Difficulty:** {card['difficulty']}")
    st.markdown("---")

# Streamlit UI
st.title("📚 LLM-Powered Flashcard Generator")
st.markdown("Generate quick study flashcards from educational content using Hugging Face summarization models.")

uploaded_file = st.file_uploader("📄 Upload Educational PDF or TXT", type=["pdf", "txt"], help="Upload textbook chapters or notes")
difficulty = st.selectbox("🎯 Select Flashcard Difficulty", ["Easy", "Medium", "Hard"], index=1)

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    st.subheader("📖 Extracted Text Preview")
    st.text_area("Content", value=textwrap.shorten(text, width=1000, placeholder="..."), height=200)

    if st.button("🚀 Generate Flashcards"):
        with st.spinner("Generating flashcards using Hugging Face model..."):
            flashcards = generate_flashcards(text, difficulty)
            st.success(f"✅ {len(flashcards)} flashcards generated!")

            for idx, card in enumerate(flashcards):
                display_flashcard(card, idx)

            export_flashcards(flashcards)

            with open("output/flashcards.csv", "rb") as f:
                st.download_button("⬇️ Download as CSV", f, file_name="flashcards.csv")

            with open("output/flashcards.json", "rb") as f:
                st.download_button("⬇️ Download as JSON", f, file_name="flashcards.json")