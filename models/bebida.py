from pydantic import BaseModel, Field


class BebidaInput(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    tipo: str = Field(pattern="^(suco|refrigerante|vinho|cerveja|agua)$")
    preco: float = Field(gt=0)
    tamanho: str = Field(description="Ex: 350ml, 750ml, 1L")
    alcoolica: bool = False


class BebidaOutput(BaseModel):
    id: int
    nome: str
    tipo: str
    preco: float
    tamanho: str
    alcoolica: bool
    criado_em: str
