from fastapi import APIRouter, HTTPException
from models.prato import PratoInput, PratoOutput
from typing import List, Optional
from datetime import datetime

router = APIRouter()

pratos = [
    {
        "id": 1,
        "nome": "Margherita",
        "categoria": "pizza",
        "preco": 45.0,
        "disponivel": True,
        "criado_em": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "nome": "Carbonara",
        "categoria": "massa",
        "preco": 52.0,
        "disponivel": True,
        "criado_em": datetime.now().isoformat(),
    },
]


@router.get("/", response_model=List[PratoOutput])
async def listar_pratos(
    categoria: Optional[str] = None, apenas_disponiveis: bool = False
):
    resultado = pratos
    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]
    return resultado


@router.get("/{prato_id}", response_model=PratoOutput)
async def buscar_prato(prato_id: int):
    for prato in pratos:
        if prato["id"] == prato_id:
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1 if pratos else 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump(),
    }
    pratos.append(novo_prato)
    return novo_prato
