import math
import re
from collections import defaultdict
from app.repository.repository import buscar_todas

VOCABULARIO = set()
IDF = {}
TF_IDF_DOCUMENTOS = []
DOCUMENTOS = []

def limpar(texto):
    if not texto:
        return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-zA-Z0-9áàâãéêíóôõúç\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def tokenizar(texto):
    return limpar(texto).split()

def calcular_tf(tokens):
    tf = defaultdict(int)
    for t in tokens:
        tf[t] += 1
    total = len(tokens)
    return {t: c / total for t, c in tf.items()}

def calcular_idf(documentos_tokenizados):
    global VOCABULARIO
    VOCABULARIO = set()

    df = defaultdict(int)
    total_docs = len(documentos_tokenizados)

    for tokens in documentos_tokenizados:
        unico_doc = set(tokens)
        for termo in unico_doc:
            df[termo] += 1
            VOCABULARIO.add(termo)

    return {t: math.log(total_docs / df[t], 10) for t in VOCABULARIO}

def construir_indice():
    """
    Lê TODAS as notícias do banco e recalcula:
    - VOCABULARIO
    - IDF
    - TF-IDF de cada documento
    """
    global DOCUMENTOS, TF_IDF_DOCUMENTOS, IDF

    DOCUMENTOS = buscar_todas()

    if not DOCUMENTOS:
        print("\n[AVISO] Nenhum documento encontrado no banco. Índice não construído.\n")
        return

    textos = [doc["conteudo"] for doc in DOCUMENTOS]
    docs_tokenizados = [tokenizar(t) for t in textos]

    IDF = calcular_idf(docs_tokenizados)

    TF_IDF_DOCUMENTOS = []
    for tokens in docs_tokenizados:
        tf = calcular_tf(tokens)
        tfidf = {t: tf[t] * IDF.get(t, 0) for t in tf}
        TF_IDF_DOCUMENTOS.append(tfidf)

    print("\n=========== TF-IDF INDEX CONSTRUÍDO ===========")
    print(f"Vocabulário criado: {len(VOCABULARIO)} termos")
    print(f"Documentos indexados: {len(DOCUMENTOS)}")
    print("================================================\n")

def atualizar_indices_tfidf():
    """ Usado após inserir notícias novas no banco """
    construir_indice()

def cosseno(vec1, vec2):
    inter = set(vec1.keys()) & set(vec2.keys())

    numerador = sum(vec1[t] * vec2[t] for t in inter)
    denom1 = math.sqrt(sum(v*v for v in vec1.values()))
    denom2 = math.sqrt(sum(v*v for v in vec2.values()))

    if denom1 == 0 or denom2 == 0:
        return 0

    return numerador / (denom1 * denom2)


def realizar_busca_ordenada(consulta):
    tokens = tokenizar(consulta)
    tf_q = calcular_tf(tokens)
    tfidf_q = {t: tf_q[t] * IDF.get(t, 0) for t in tf_q}

    scores = []
    for i, doc_vec in enumerate(TF_IDF_DOCUMENTOS):
        score = cosseno(tfidf_q, doc_vec)
        scores.append((score, DOCUMENTOS[i]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [
        {
            "score": round(score, 4),
            "id": doc["id"],
            "titulo": doc["titulo"],
            "conteudo": doc["conteudo"][:200] + "...",
            "campus": doc["campus"],
            "url": doc["url"]
        }
        for score, doc in scores if score > 0
    ]

construir_indice()

