from fastapi import APIRouter
from models.bebida import BebidaInput, BebidaOutput
from typing import List, Optional
from datetime import datetime

router = APIRouter()

bebidas = [
    {
        "id": 1,
        "nome": "Suco de Laranja",
        "tipo": "suco",
        "preco": 12.0,
        "tamanho": "400ml",
        "alcoolica": False,
        "criado_em": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "nome": "Água Mineral",
        "tipo": "agua",
        "preco": 6.0,
        "tamanho": "500ml",
        "alcoolica": False,
        "criado_em": datetime.now().isoformat(),
    },
    {
        "id": 3,
        "nome": "Refrigerante Cola",
        "tipo": "refrigerante",
        "preco": 8.0,
        "tamanho": "350ml",
        "alcoolica": False,
        "criado_em": datetime.now().isoformat(),
    },
]


@router.get("/", response_model=List[BebidaOutput])
async def listar_bebidas(alcoolica: Optional[bool] = None, tipo: Optional[str] = None):
    resultado = bebidas
    if alcoolica is not None:
        resultado = [b for b in resultado if b.get("alcoolica") == alcoolica]
    if tipo:
        resultado = [b for b in resultado if b["tipo"] == tipo]
    return resultado


@router.post("/", response_model=BebidaOutput, status_code=201)
async def criar_bebida(bebida: BebidaInput):
    novo_id = max(b["id"] for b in bebidas) + 1 if bebidas else 1
    nova = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **bebida.model_dump(),
    }
    bebidas.append(nova)
    return nova
