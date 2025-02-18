from typing import Dict
from fastapi import FastAPI
from app.routers import routers_produtos, routers_usuarios


MENSAGEM_HOME: str = "Bem-vindo à API de Recomendação de Produtos"


# Criando o App
app = FastAPI()

# Adicionando os routers
app.include_router(router=routers_usuarios.router)
app.include_router(router=routers_produtos.router)

# Iniciando o servidor


@app.get("/")
def home() -> Dict[str, str]:
    """
    Rota de boas-vindas.
    Returns:
            Dict[str, str]: Um dicionário com a mensagem de boas-vindas.
    """
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}
