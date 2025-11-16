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

class Noticia:
    def __init__(self, titulo, html_puro, conteudo, campus, url, coletado_em):
        self.titulo = titulo
        self.html_puro = html_puro
        self.conteudo = conteudo
        self.campus = campus
        self.url = url
        self.coletado_em = coletado_em