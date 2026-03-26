# Rossana De Rose — AI Portfolio Assistant

I created an interactive portfolio assistant that allows recruiters, hiring managers and collaborators to explore my  professional background, skills, projects and career story — powered entirely by a custom-built RAG (Retrieval-Augmented Generation) system with **no external AI API**.

---

## What it does

- Answers questions about Rossana's experience, skills, projects and personal interests
- Responds in **English, Spanish and Italian**
- Shows a project grid with direct GitHub links
- Includes recruiter-ready quick questions
- Built from scratch — no OpenAI, no Anthropic, no paid API

---

## How it works

```
User question
     ↓
TF-IDF vectorizer (scikit-learn)
     ↓
Cosine similarity search over 130+ indexed chunks
     ↓
FAQ-priority answer builder
     ↓
Response in the detected language
```

The knowledge base is built from Rossana's real CV (EN + ES), cover letters, project descriptions, career story and FAQs — all indexed locally.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Retrieval | TF-IDF + Cosine Similarity (scikit-learn) |
| Chunking | Paragraph-based semantic splitting |
| Knowledge base | Plain text files (CV, projects, FAQs, cover letters) |
| Language | Python |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
rossana-portfolio-assistant/
├── 1_ingest.py          # Indexes data files into vector store
├── 2_app.py             # Streamlit app
├── rag_engine.py        # Retrieval + answer builder
├── data/
│   ├── cv_en.txt
│   ├── cv_es.txt
│   ├── cover_letter_en.txt
│   ├── cover_letter_es.txt
│   ├── projects.txt
│   ├── experience_story.txt
│   └── faqs.txt
└── vector_store/        # Pre-built TF-IDF index
```

---

## Run locally

```bash
pip install -r requirements.txt
python 1_ingest.py      # only needed if you change the data files
streamlit run 2_app.py
```

---

## About Rossana

Data Analyst & AI Specialist based in Málaga, Spain. Passionate about turning complex data into clear, actionable insights.

- Email: rossanadero@hotmail.it
- LinkedIn: [linkedin.com/in/rossana-derose](https://linkedin.com/in/rossana-derose)
- GitHub: [github.com/RossanaDr11](https://github.com/RossanaDr11)
