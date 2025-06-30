
# 🪐 JupiterHelp: Chainlit-Ollama FAQ Assistant

This is a conversational LLM app powered by [Chainlit](https://docs.chainlit.io/) and [Ollama](https://ollama.com/) that acts as a smart support bot for the Jupiter community forum. It uses FAISS for vector search and answers questions using `llama3:instruct` with helpful context from scraped user discussions.

---

## 📦 Setup Instructions

### 🔹 1. Create and activate a virtual environment

```bash
# Create a new Python virtual environment
python -m venv .venv

# Activate it
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 🔹 2. Install project dependencies

```bash
pip install requirements.txt
```

---

## 🔌 Install Ollama Suite

Ollama must be installed separately to use local LLM and embedding models.

1. Download and install Ollama from the official website:  
👉 [https://ollama.com/download](https://ollama.com/download)

2. After installation, verify Ollama is accessible:

```bash
ollama --version
```

3. Pull the required models:

```bash
ollama pull llama3:instruct
ollama pull nomic-embed-text
```

---

## 🛠️ Project Structure

```text
.
├── app.py                  # Main Chainlit app
├── chainlit.md             # Optional welcome screen
├── jupiter_scraper.py      # Web scraper for forum Q&A
├── jupiter_embed.py        # Embeds Q&A into FAISS
├── jupiter_help_qas.json   # Scraped raw Q&A data
├── jupiter_kb.index        # FAISS index (vector store)
├── jupiter_kb_docs.json    # Metadata for vector chunks
├── ques.txt                # Sample questions for testing
```

---

## 🚀 Run the App

### 1. Make sure Ollama is running

You can test it by running:

```bash
ollama run llama3:instruct
```

Let it load the model and stay active.

### 2. Launch the Chainlit app

```bash
chainlit run app.py
```

Then visit:  
🔗 [http://localhost:8000](http://localhost:8000)

---

## 🔄 Optional: Rebuild the Vector DB

To regenerate the FAISS database from fresh scraped data:

```bash
python jupiter_scraper.py      # Scrapes help forum
python jupiter_embed.py        # Embeds and stores vectors
```

This will update:

- `jupiter_help_qas.json`
- `jupiter_kb_docs.json`
- `jupiter_kb.index`

---

## 🧪 Sample Questions

Try asking the bot:

- What documents are needed to complete Jupiter KYC?
- How do I report an unauthorized transaction?
- What should I do if my card doesn’t work at an ATM?

Examples are also stored in `ques.txt`.

---

## ✅ Features

- 🔍 FAISS vector search using Nomic embeddings
- 🧠 Answers generated with local `llama3:instruct`
- 🤖 Interactive frontend with Chainlit
- 📥 Scraped data from Jupiter Community forum

---

## 🧠 Tips

- Ollama must stay running while using the app.
- ChromeDriver is required for `jupiter_scraper.py` (used via Selenium).

---

## 🫱 Community & Docs

- 📚 [Chainlit Documentation](https://docs.chainlit.io)
- 🤖 [Ollama Documentation](https://ollama.com)
- 💬 [Ollama Community](https://ollama.com/community)

---
