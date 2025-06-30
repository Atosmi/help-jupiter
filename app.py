import chainlit as cl
import faiss
import numpy as np
import json
from ollama import chat, embeddings

# === Load FAISS and documents ===
INDEX_PATH = "jupiter_kb.index"
DOCS_PATH = "jupiter_kb_docs.json"
EMBED_DIM = 768
TOP_K = 5

# Load FAISS index
faiss_index = faiss.read_index(INDEX_PATH)

# Load corresponding chunks and metadata
with open(DOCS_PATH, "r", encoding="utf-8") as f:
    kb_docs = json.load(f)

# === Semantic search helper ===
def search_context(query, top_k=TOP_K):
    try:
        result = embeddings(model="nomic-embed-text", prompt=query)
        query_vec = np.array(result["embedding"], dtype="float32").reshape(1, -1)
    except Exception as e:
        return f"⚠️ Embedding failed: {e}", []

    scores, indices = faiss_index.search(query_vec, top_k)
    matched_chunks = [kb_docs[i]["text"] for i in indices[0] if i < len(kb_docs)]
    return None, matched_chunks

# === LLM inference helper ===
def ask_llm(question, context_chunks):
    context_block = "\n\n---\n\n".join(context_chunks)
    system_prompt = (
        f"You are an expert banking assistant trained on Jupiter's help articles.\n"
        f"Use the context below to answer user questions.\n"
        f"Answer concisely and helpfully.\n\n"
        f"Context:\n{context_block}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    response = chat(model="llama3:instruct", messages=messages)
    return response["message"]["content"].strip()

# === Chainlit app ===
@cl.on_chat_start
async def start():
    await cl.Message("👋 Hello! This is JupiterHelp. How can I help you today?").send()

@cl.on_message
async def handle_message(msg: cl.Message):
    query = msg.content.strip()

    # Show "thinking" message
    thinking_msg = await cl.Message("🤖 Thinking...").send()

    # Perform embedding + search
    error, context_chunks = search_context(query)
    if error:
        thinking_msg.content = error
        await thinking_msg.update()
        return

    if not context_chunks:
        thinking_msg.content = "❌ No relevant context found for your query."
        await thinking_msg.update()
        return

    # Get LLM response
    response = ask_llm(query, context_chunks)

    # Update the thinking message with the actual answer
    thinking_msg.content = response
    await thinking_msg.update()


