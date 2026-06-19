import numpy as np
import pytest

from ml.model_utils import load_model

PAYLOAD_VALIDO = {
    "valor_transacao": 120.0,
    "hora_transacao": 20,
    "distancia_ultima_compra": 2.5,
    "tentativas_senha": 1,
    "pais_diferente": 0,
}


@pytest.fixture(scope="module")
def modelo():
    return load_model()


@pytest.fixture
def amostra_valida():
    return np.array([[120.0, 20, 2.5, 1, 0]])


@pytest.mark.integracao
def test_modelo_carregado_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_metodo_predict(modelo):
    assert hasattr(modelo, "predict")
    assert callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_metodo_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")
    assert callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_retorna_array_com_formato_correto(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)
    assert resultado.shape == (1,)
    assert resultado[0] in [0, 1]


@pytest.mark.integracao
def test_predict_proba_retorna_probabilidades_validas(modelo, amostra_valida):
    probabilidades = modelo.predict_proba(amostra_valida)
    assert probabilidades.shape == (1, 2)
    assert abs(probabilidades[0].sum() - 1.0) < 1e-6
    assert all(0 <= probabilidade <= 1 for probabilidade in probabilidades[0])


@pytest.mark.integracao
def test_endpoint_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200


@pytest.mark.integracao
def test_endpoint_predict_retorna_campos_esperados(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200
    dados = response.json()
    assert "prediction" in dados
    assert "probability" in dados
    assert "label" in dados
    assert "model_version" in dados


@pytest.mark.integracao
def test_endpoint_predict_prediction_e_binario(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.json()["prediction"] in [0, 1]


@pytest.mark.integracao
def test_endpoint_predict_probability_entre_zero_e_um(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    probability = response.json()["probability"]
    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0


@pytest.mark.integracao
def test_endpoint_predict_label_e_string_nao_vazia(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    label = response.json()["label"]
    assert isinstance(label, str)
    assert len(label) > 0


@pytest.mark.integracao
def test_endpoint_predict_sem_campo_obrigatorio_retorna_422(client):
    payload_incompleto = {"valor_transacao": 120.0}
    response = client.post("/ml/predict", json=payload_incompleto)
    assert response.status_code == 422


@pytest.mark.integracao
@pytest.mark.parametrize(
    "campo,valor_invalido",
    [
        ("hora_transacao", 25),
        ("hora_transacao", -1),
        ("tentativas_senha", 0),
        ("valor_transacao", -50.0),
        ("pais_diferente", 2),
    ],
)
def test_endpoint_predict_campo_invalido_retorna_422(client, campo, valor_invalido):
    payload = {**PAYLOAD_VALIDO, campo: valor_invalido}
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422


@pytest.mark.integracao
def test_health_modelo_retorna_ok(client):
    response = client.get("/ml/health")
    assert response.status_code == 200
    dados = response.json()
    assert dados["api"] == "ok"
    assert dados["model"] == "ok"
    assert "model_repo" in dados


@pytest.mark.integracao
def test_health_modelo_retorna_degraded_quando_modelo_falha(client, monkeypatch):
    from routers import predict

    def falhar_ao_carregar_modelo():
        raise RuntimeError("falha simulada no modelo")

    monkeypatch.setattr(predict, "get_model", falhar_ao_carregar_modelo)

    response = client.get("/ml/health")
    assert response.status_code == 503
    dados = response.json()
    assert dados["api"] == "ok"
    assert dados["model"] == "degraded"
    assert "falha simulada" in dados["detail"]
