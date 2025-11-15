from pydantic import BaseModel

class NoticiaCreate(BaseModel):
    titulo: str
    conteudo: str
    campus: str
    url: str

class NoticiaUpdate(BaseModel):
    titulo: str | None = None
    conteudo: str | None = None
    campus: str | None = None

class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    campus: str
    url: str

    class Config:
        orm_mode = True
