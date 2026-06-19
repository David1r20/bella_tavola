from fastapi import APIRouter, HTTPException
from models.pedido import PedidoInput, PedidoOutput
from routers.pratos import pratos
from typing import List
from datetime import datetime

router = APIRouter()
pedidos_db = []


@router.get("/", response_model=List[PedidoOutput])
async def listar_pedidos():
    return pedidos_db


@router.post("/", response_model=PedidoOutput, status_code=201)
async def criar_pedido(pedido: PedidoInput):
    # Buscar o prato para validar e pegar o preço
    prato_alvo = None
    for p in pratos:
        if p["id"] == pedido.prato_id:
            prato_alvo = p
            break

    if not prato_alvo:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if not prato_alvo.get("disponivel", True):
        raise HTTPException(status_code=400, detail="Prato indisponível no momento")

    valor_total = prato_alvo["preco"] * pedido.quantidade

    novo = {
        "id": len(pedidos_db) + 1,
        "prato_id": pedido.prato_id,
        "quantidade": pedido.quantidade,
        "nome_prato": prato_alvo["nome"],
        "valor_total": valor_total,
        "status": "pendente",
        "criado_em": datetime.now().isoformat(),
    }
    pedidos_db.append(novo)
    return novo
