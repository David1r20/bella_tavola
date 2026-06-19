import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Cria um TestClient novo para cada teste."""
    return TestClient(app)


@pytest.fixture
def prato_valido():
    return {"nome": "Nhoque da Fixture", "categoria": "massa", "preco": 45.0}


@pytest.fixture
def bebida_valida():
    return {"nome": "Vinho da Casa", "tipo": "vinho", "preco": 80.0, "tamanho": "750ml"}
