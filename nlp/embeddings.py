from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load model globally to avoid reloading (singleton-ish)
# 'all-MiniLM-L6-v2' is fast and good for this use case
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Returns the embedding vector for the input text."""
    print(f"DEBUG: get_embedding called with type={type(text)}, content='{text}'")
    return model.encode(text, convert_to_tensor=True)

def compute_similarity(text1, text2):
    """Computes cosine similarity between two texts."""
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return util.pytorch_cos_sim(emb1, emb2).item()

def find_best_match(query, corpus):
    """
    Finds the best matching sentence in a corpus.
    query: str
    corpus: list of str
    Returns: (best_match_str, score)
    """
    query_emb = get_embedding(query)
    corpus_emb = model.encode(corpus, convert_to_tensor=True)
    
    hits = util.semantic_search(query_emb, corpus_emb, top_k=1)
    hit = hits[0][0]
    
    return corpus[hit['corpus_id']], hit['score']
