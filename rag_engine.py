import json, pickle, re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

STORE_DIR = "vector_store"
TOP_K     = 5

_vectorizer = None
_matrix     = None
_chunks     = None

def load_rag():
    global _vectorizer, _matrix, _chunks
    if _vectorizer is None:
        with open(f"{STORE_DIR}/vectorizer.pkl", "rb") as f:
            _vectorizer = pickle.load(f)
        with open(f"{STORE_DIR}/matrix.pkl", "rb") as f:
            _matrix = pickle.load(f)
        with open(f"{STORE_DIR}/chunks.json", "r", encoding="utf-8") as f:
            _chunks = json.load(f)
    return _vectorizer, _matrix, _chunks

def retrieve(query):
    vectorizer, matrix, chunks = load_rag()
    query_vec = vectorizer.transform([query])
    scores    = cosine_similarity(query_vec, matrix).flatten()
    top_idx   = np.argsort(scores)[::-1][:TOP_K]
    return [
        {**chunks[i], "score": float(scores[i])}
        for i in top_idx if scores[i] > 0
    ]

# ── Language detection ────────────────────────────────────────────
def _detect_language(query):
    q = query.lower()
    spanish = ["qué", "cómo", "cuál", "habla", "tiene", "trabaja", "puede",
               "está", "disponible", "experiencia", "hola", "¿", "español",
               "proyectos", "habilidades", "contrata"]
    italian = ["che", "come", "parla", "ha", "può", "lavora", "italiano",
               "ciao", "quali", "sei", "progetti", "competenze"]
    if any(m in q for m in spanish):
        return "es"
    if any(m in q for m in italian):
        return "it"
    return "en"

# ── Response templates ────────────────────────────────────────────
def _not_found(lang):
    if lang == "es":
        return ("No tengo ese detalle específico en mi base de conocimiento. "
                "Puedes contactar a Rossana directamente en **rossanadero@hotmail.it** "
                "o en [LinkedIn](https://linkedin.com/in/rossana-derose).")
    if lang == "it":
        return ("Non ho quel dettaglio specifico nella mia base di conoscenza. "
                "Puoi contattare Rossana direttamente a **rossanadero@hotmail.it** "
                "o su [LinkedIn](https://linkedin.com/in/rossana-derose).")
    return ("I don't have that specific detail in my knowledge base. "
            "You can contact Rossana directly at **rossanadero@hotmail.it** "
            "or on [LinkedIn](https://linkedin.com/in/rossana-derose).")

def _contact_footer(lang):
    if lang == "es":
        return "\n\nNo dudes en contactarla directamente en LinkedIn o por email."
    if lang == "it":
        return "\n\nNon esitare a contattarla direttamente su LinkedIn o via email."
    return "\n\nFeel free to reach out to Rossana directly on LinkedIn or by email."

# ── Extract the answer part from FAQ chunks ───────────────────────
def _extract_faq_answer(text):
    match = re.search(r'\bA:\s*(.+)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# ── Main answer builder (no external API) ────────────────────────
def answer(query, history=None, api_key=None):
    hits = retrieve(query)
    lang = _detect_language(query)

    if not hits or hits[0]["score"] < 0.03:
        return _not_found(lang), []

    parts = []

    # 1. FAQ chunks have clean, complete answers — use them first
    for hit in hits:
        if hit["source"] == "faqs.txt":
            faq_ans = _extract_faq_answer(hit["text"])
            if faq_ans and faq_ans not in parts:
                parts.append(faq_ans)

    # 2. If no FAQ matched, pull from narrative/project/cv chunks
    if not parts:
        for hit in hits[:2]:
            text = hit["text"].strip()
            if len(text) > 40 and text not in parts:
                parts.append(text)

    if not parts:
        return _not_found(lang), hits

    # Keep response concise — max 2 paragraphs
    response = "\n\n".join(parts[:2])

    # Append contact cue when the question is about availability / contact
    contact_kws = ["contact", "email", "reach", "hire", "available", "remote",
                   "contacto", "disponible", "contatto", "disponibile", "contratar"]
    if any(kw in query.lower() for kw in contact_kws):
        response += _contact_footer(lang)

    return response, hits
