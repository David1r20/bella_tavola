from fastapi import APIRouter, HTTPException
from models.prato import PratoInput, PratoOutput
from storage import buscar_prato_db, criar_prato_db, listar_pratos_db
from typing import List, Optional

router = APIRouter()


@router.get("/", response_model=List[PratoOutput])
async def listar_pratos(
    categoria: Optional[str] = None, apenas_disponiveis: bool = False
):
    return listar_pratos_db(categoria, apenas_disponiveis)


@router.get("/{prato_id}", response_model=PratoOutput)
async def buscar_prato(prato_id: int):
    prato = buscar_prato_db(prato_id)
    if prato:
        return prato
    raise HTTPException(status_code=404, detail="Prato nao encontrado")


@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    return criar_prato_db(prato)
