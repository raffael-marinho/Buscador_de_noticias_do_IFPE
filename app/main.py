from fastapi import FastAPI, HTTPException
from app.database.database import init_db
from app.repository.repository import (
    salvar_noticia, buscar_todas, buscar_por_id,
    atualizar_noticia, deletar_noticia
)
from app.schemas.schema import NoticiaCreate, NoticiaUpdate, NoticiaResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    init_db()
    yield
    print("Encerrando aplicação...")

app = FastAPI(title="Buscador de notícias do IFPE", lifespan=lifespan)

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
