# jupiter_embed.py

import json
import uuid
import faiss
import numpy as np
from ollama import embeddings

# Parameters
qa_json_path = "jupiter_help_qas.json"
faiss_index_path = "jupiter_kb.index"
faiss_metadata_path = "jupiter_kb_docs.json"
chunk_size = 300  # characters
chunk_overlap = 50
embedding_dim = 768  # Nomic embed size

def chunk_text(text, size=chunk_size, overlap=chunk_overlap):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def load_qa_chunks(json_file):
    """Load Q&A pairs and create chunks with metadata"""
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunked_entries = []
    for item in data:
        qa_text = f"Q: {item['question']}\nA: {item['answer']}"
        chunks = chunk_text(qa_text)
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            metadata = {
                "id": chunk_id,
                "chunk_index": i,
                "source": "jupiter_help_qas.json",
                "category": "customer-support",
                "tags": ["Jupiter", "Support", "Banking", "FAQ"]
            }
            chunked_entries.append({
                "id": chunk_id,
                "text": chunk,
                "metadata": metadata
            })
    return chunked_entries

def get_embeddings(texts):
    """Call Ollama Nomic embedding API"""
    vectors = []
    for text in texts:
        try:
            result = embeddings(model="nomic-embed-text", prompt=text)
            vectors.append(result["embedding"])
        except Exception as e:
            print(f"❌ Error embedding: {e}")
            vectors.append([0.0] * embedding_dim)
    return vectors

# Main pipeline
entries = load_qa_chunks(qa_json_path)
texts = [entry["text"] for entry in entries]
metadatas = [entry["metadata"] for entry in entries]

print(f"📚 Loaded and chunked {len(entries)} Q&A chunks.")

embedding_matrix = np.array(get_embeddings(texts)).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)
faiss.write_index(index, faiss_index_path)

# Save metadata
with open(faiss_metadata_path, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print("✅ Saved FAISS index and metadata.")
