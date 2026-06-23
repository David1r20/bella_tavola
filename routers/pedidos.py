from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from models.pedido import PedidoInput, PedidoOutput
from storage import buscar_prato_db

router = APIRouter()
pedidos_db = []


@router.get("/", response_model=List[PedidoOutput])
async def listar_pedidos():
    return pedidos_db


@router.post("/", response_model=PedidoOutput, status_code=201)
async def criar_pedido(pedido: PedidoInput):
    prato_alvo = buscar_prato_db(pedido.prato_id)

    if not prato_alvo:
        raise HTTPException(status_code=404, detail="Prato nao encontrado")

    if not prato_alvo.get("disponivel", True):
        raise HTTPException(status_code=400, detail="Prato indisponivel no momento")

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
