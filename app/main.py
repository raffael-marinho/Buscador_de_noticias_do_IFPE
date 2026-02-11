from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import init_db
from app.repository.repository import (
    salvar_noticia, buscar_todas, buscar_por_id,
    atualizar_noticia, deletar_noticia
)
from app.schemas.schema import NoticiaCreate, NoticiaUpdate, NoticiaResponse
from contextlib import asynccontextmanager

from app.scraper.scraper import run_full_scrape
from app.service.service import processar_lista_de_noticias
from app.service.search_service import realizar_busca_ordenada, construir_indice

origins = [
    "http://localhost:4200",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    yield
    print("Encerrando aplicação...")

app = FastAPI(title="Buscador de notícias do IFPE", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/atualizar-base")
def atualizar_base_de_dados():
    """
    Roda o scraper, pega as notícias da internet e salva no banco.
    """
    print("Iniciando Scraper via API...")
    lista_bruta = run_full_scrape()
    
    lista_salva = processar_lista_de_noticias(lista_bruta)
    
    return {
        "mensagem": "Banco atualizado com sucesso",
        "total_novas": len(lista_salva)
    }

@app.get("/buscar")
def buscar_noticias(q: str):
    """
    Faz a busca usando TF-IDF e Similaridade de Cosseno.
    Uso: /buscar?q=tecnologia
    """
    resultados = realizar_busca_ordenada(q)
    
    return {
        "termo": q,
        "total": len(resultados),
        "resultados": resultados
    }

# GET ALL
@app.get("/noticias", response_model=list[NoticiaResponse])
def listar():
    return buscar_todas()


# GET por ID
@app.get("/noticias/{id}", response_model=NoticiaResponse)
def obter(id: int):
    noticia = buscar_por_id(id)
    if not noticia:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return noticia


# POST
@app.post("/noticias", response_model=NoticiaResponse)
def criar(noticia: NoticiaCreate):
    novo_id = salvar_noticia(noticia.dict())
    criada = buscar_por_id(novo_id)
    return criada


# PUT
@app.put("/noticias/{id}", response_model=NoticiaResponse)
def atualizar(id: int, noticia: NoticiaUpdate):
    dados = noticia.dict(exclude_unset=True)

    ok = atualizar_noticia(id, dados)

    if not ok:
        raise HTTPException(status_code=404, detail="Notícia não encontrada para atualizar")

    return buscar_por_id(id)


# DELETE
@app.delete("/noticias/{id}")
def remover(id: int):
    ok = deletar_noticia(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Notícia não encontrada para remoção")
    return {"status": "sucesso", "mensagem": "Notícia removida"}