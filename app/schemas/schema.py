from pydantic import BaseModel

class NoticiaCreate(BaseModel):
    titulo: str
    conteudo: str
    campus: str
    url: str

    model_config = {
        "from_attributes": True
    }

class NoticiaUpdate(BaseModel):
    titulo: str | None = None
    conteudo: str | None = None
    campus: str | None = None

    model_config = {
        "from_attributes": True
    }

class NoticiaResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    campus: str
    url: str

    model_config = {
        "from_attributes": True
    }