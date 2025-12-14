import math
import re
from collections import Counter

TFIDF_INDEX = {}
DOCS_CACHE = []

def preprocess_text(text: str):
    text = text.lower()
    text = re.sub(r'[^a-zà-ÿ\s]', ' ', text)
    return text.split()

def compute_tf(tokens):
    tf = Counter(tokens)
    total = len(tokens)
    return {term: freq / total for term, freq in tf.items()}

def compute_idf(docs_tokens):
    N = len(docs_tokens)
    idf = {}

    all_terms = set(term for tokens in docs_tokens for term in tokens)

    for term in all_terms:
        docs_with_term = sum(1 for tokens in docs_tokens if term in tokens)
        idf[term] = math.log(N / (1 + docs_with_term))

    return idf

def build_tfidf_index(news_list):
    global TFIDF_INDEX, DOCS_CACHE

    DOCS_CACHE = news_list
    docs_tokens = []

    for news in news_list:
        tokens = preprocess_text(news["conteudo"])
        docs_tokens.append(tokens)

    idf = compute_idf(docs_tokens)

    TFIDF_INDEX = {}

    for doc_id, tokens in enumerate(docs_tokens):
        tf = compute_tf(tokens)
        TFIDF_INDEX[doc_id] = {
            term: tf_val * idf.get(term, 0)
            for term, tf_val in tf.items()
        }

    print(f"TF-IDF gerado para {len(TFIDF_INDEX)} documentos")
