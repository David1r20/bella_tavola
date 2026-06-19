import pytest


@pytest.mark.smoke
def test_listar_pratos(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.smoke
def test_buscar_prato_existente(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Margherita"


@pytest.mark.smoke
def test_buscar_prato_inexistente(client):
    response = client.get("/pratos/999")
    assert response.status_code == 404


@pytest.mark.smoke
def test_criar_prato_valido(client):
    novo = {"nome": "Gnocchi", "categoria": "massa", "preco": 48.0}
    response = client.post("/pratos", json=novo)
    assert response.status_code == 201
    assert response.json()["nome"] == "Gnocchi"


@pytest.mark.validacao
def test_criar_prato_invalido(client):
    invalido = {"nome": "X", "categoria": "pizza", "preco": -10}
    response = client.post("/pratos", json=invalido)
    assert response.status_code == 422
