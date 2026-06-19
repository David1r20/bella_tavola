from fastapi import APIRouter, HTTPException
from models.reserva import ReservaInput, ReservaOutput
from typing import List, Optional
from datetime import datetime

router = APIRouter()
reservas = []


@router.get("/", response_model=List[ReservaOutput])
async def listar_reservas(status_ativa: Optional[bool] = True):
    return [r for r in reservas if r["ativa"] == status_ativa]


@router.post("/", response_model=ReservaOutput, status_code=201)
async def criar_reserva(reserva: ReservaInput):
    data_reserva = reserva.data_hora.date()
    conflito = any(
        r["mesa"] == reserva.mesa
        and r["ativa"]
        and datetime.fromisoformat(r["data_hora"]).date() == data_reserva
        for r in reservas
    )
    if conflito:
        raise HTTPException(
            status_code=400, detail=f"Mesa {reserva.mesa} já reservada para esta data."
        )

    nova = {
        "id": len(reservas) + 1,
        "ativa": True,
        "criada_em": datetime.now().isoformat(),
        **reserva.model_dump(),
        "data_hora": reserva.data_hora.isoformat(),
    }
    reservas.append(nova)
    return nova


@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.get("/mesa/{mesa_id}", response_model=List[ReservaOutput])
async def buscar_reservas_por_mesa(mesa_id: int):
    return [r for r in reservas if r["mesa"] == mesa_id]
