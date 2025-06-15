# llm-flashcard-generator
A lightweight and efficient application that leverages Hugging Face Transformers to automatically generate question-answer flashcards from educational PDFs or text files. Built using Python and Streamlit, this tool enables students, educators, and self-learners to convert dense study material into bite-sized, interactive Q&amp;A flashcards in seconds.
## ✨ Features

- 📄 Upload `.pdf` or `.txt` educational content
- ⚡ Fast summarization using Hugging Face (`distilbart-cnn-12-6`)
- 🤖 Auto-generates 10–20 flashcards with Q&A format
- 🎯 Difficulty tagging (Easy, Medium, Hard)
- 🧠 Chunking of long texts for more accurate flashcards
- 💾 Download flashcards in `.csv` and `.json` formats
- 🎈 Clean and responsive UI using Streamlit

Tech Stack

- Python 3.9+
- Streamlit
- Hugging Face Transformers
- PyPDF2
- Torch

Installation
# Clone the repository
git clone https://github.com/ManasPandey2004/llm-flashcard-generator.git
cd llm-flashcard-generator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
