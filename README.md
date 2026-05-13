# Context-Aware AI Chatbot

A production-quality chatbot that uses NLP to understand intent, extract entities, and maintain conversation context.

## Features
- **Intent Classification**: Uses Scikit-Learn to categorize user messages (Greeting, Question, Task, etc.).
- **Entity Extraction**: Uses SpaCy to identify key information (Names, Locations, etc.).
- **Semantic Search**: Uses Sentence Transformers to match queries against a knowledge base.
- **Contextual Memory**: Stores conversation history in SQLite to maintain context across turns.
- **Interfaces**: REST API (FastAPI) and Interactive UI (Streamlit).

## Project Structure
```
developing chatbot/
│
├── nlp/                  # Core NLP modules
│   ├── embeddings.py     # Sentence embeddings
│   ├── intent_classifier.py # ML classifier
│   └── entity_extractor.py  # SpaCy wrapper
├── memory/               # Data persistence
│   └── chat_memory.py    # SQLite handler
├── engine/               # Logic coordinator
│   └── response_engine.py
├── api/                  # FastAPI backend
│   └── app.py
├── ui/                   # Streamlit frontend
│   └── streamlit_app.py
└── requirements.txt
```

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Download SpaCy Model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Running the Application

### Option 1: Streamlit UI (Easiest)
Run the interactive chat interface:
```bash
streamlit run ui/streamlit_app.py
```

### Option 2: API Server
Run the backend API:
```bash
uvicorn api.app:app --reload
```
You can then send POST requests to `http://localhost:8000/chat`.
