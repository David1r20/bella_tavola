import pytest


@pytest.mark.smoke
def test_listar_bebidas(client):
    response = client.get("/bebidas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.smoke
def test_filtrar_bebidas_alcoolicas(client):
    client.post(
        "/bebidas",
        json={
            "nome": "Cerveja",
            "tipo": "cerveja",
            "preco": 15,
            "tamanho": "600ml",
            "alcoolica": True,
        },
    )

    response = client.get("/bebidas?alcoolica=true")
    assert response.status_code == 200
    for bebida in response.json():
        assert bebida["alcoolica"] is True


@pytest.mark.smoke
def test_criar_bebida_valida(client, bebida_valida):
    response = client.post("/bebidas", json=bebida_valida)
    assert response.status_code == 201
    assert response.json()["nome"] == bebida_valida["nome"]
