import re
from app.repository.repository import salvar_noticia
from app.service.search_service import atualizar_indices_tfidf


def limpar_texto(texto):
    if not texto:
        return ""
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def tratar_noticia(noticia):
    return {
        "titulo": limpar_texto(noticia.get("titulo", "")),
        "html_puro": noticia.get("html_puro"),
        "conteudo": limpar_texto(noticia.get("conteudo", "")),
        "campus": noticia.get("campus", "Desconhecido"),
        "url": noticia.get("url", ""),
        "coletado_em": noticia.get("coletado_em")
    }


def processar_lista_de_noticias(lista):
    tratadas = []
    for item in lista:
        noticia = tratar_noticia(item)
        salvar_noticia(noticia)
        tratadas.append(noticia)

    atualizar_indices_tfidf()

    return tratadas
