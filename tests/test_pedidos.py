import pytest


@pytest.mark.smoke
def test_criar_pedido_com_prato_existente(client):
    payload = {"prato_id": 1, "quantidade": 2, "observacao": "sem cebola"}
    response = client.post("/pedidos", json=payload)
    assert response.status_code in [200, 201]
    dados = response.json()
    assert "valor_total" in dados
    assert "nome_prato" in dados


@pytest.mark.smoke
def test_valor_total_calculado_corretamente(client):
    payload = {"prato_id": 1, "quantidade": 3}
    response = client.post("/pedidos", json=payload)
    assert response.status_code in [200, 201]
    assert response.json()["valor_total"] == 45.0 * 3


@pytest.mark.smoke
def test_criar_pedido_com_prato_inexistente_retorna_404(client):
    payload = {"prato_id": 9999, "quantidade": 1}
    response = client.post("/pedidos", json=payload)
    assert response.status_code == 404


@pytest.mark.validacao
def test_criar_pedido_com_quantidade_zero_retorna_422(client):
    payload = {"prato_id": 1, "quantidade": 0}
    response = client.post("/pedidos", json=payload)
    assert response.status_code == 422
