from typing import Union

from fastapi import FastAPI
import requests

app = FastAPI()

url = "https://portal.ifpe.edu.br/igarassu/noticias/"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/buscar")
def buscar_pagina():
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        return {"status": resposta.status_code, "conteudo": resposta.text[:500]}
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}