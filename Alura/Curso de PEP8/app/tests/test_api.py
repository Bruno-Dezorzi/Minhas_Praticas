import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "mensagem": "Bem-vindo à API de Recomendação de Produtos"
    }


def test_criar_produtos():
    response = client.post(
        "/produtos/",
        json={
            "nome": "Produto A",
            "categoria": "Categoria 1",
            "tags": ["tag1", "tag2"],
        },
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto A"
    assert response.json()["categoria"] == "Categoria 1"


def test_listar_produtos():
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0