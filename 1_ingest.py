"""
PASO 1 — INGESTA (versión TF-IDF, sin torch)
Ejecutar UNA VEZ: python 1_ingest.py
"""

import os, json, pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

MIN_CHUNK  = 80    # ignore paragraphs shorter than this
DATA_DIR   = "data"
STORE_DIR  = "vector_store"

def load_documents():
    docs = []
    for path in Path(DATA_DIR).glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        docs.append({"source": path.name, "text": text})
        print(f"  ✓ {path.name}")
    return docs

def split_chunks(docs):
    """Split on blank lines so every chunk is a clean semantic paragraph."""
    chunks = []
    for doc in docs:
        paragraphs = [p.strip() for p in doc["text"].split("\n\n") if p.strip()]
        for para in paragraphs:
            if len(para) >= MIN_CHUNK:
                chunks.append({
                    "chunk_id": len(chunks),
                    "source": doc["source"],
                    "text": para,
                })
    return chunks

def main():
    os.makedirs(STORE_DIR, exist_ok=True)
    print("📁 Cargando documentos..."); docs = load_documents()
    print(f"\n✂️  Dividiendo en chunks..."); chunks = split_chunks(docs)
    print(f"  ✓ {len(chunks)} chunks")

    print(f"\n🔢 Creando índice TF-IDF...")
    texts = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
    matrix = vectorizer.fit_transform(texts)

    print(f"\n💾 Guardando...")
    with open(f"{STORE_DIR}/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(f"{STORE_DIR}/matrix.pkl", "wb") as f:
        pickle.dump(matrix, f)
    with open(f"{STORE_DIR}/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Listo! {len(chunks)} chunks indexados.")
    print("   Ahora ejecuta: streamlit run 2_app.py")

if __name__ == "__main__":
    main()
