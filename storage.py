from datetime import datetime
from pathlib import Path
import sqlite3

from config import settings

PRATOS_INICIAIS = [
    {
        "id": 1,
        "nome": "Margherita",
        "categoria": "pizza",
        "preco": 45.0,
        "disponivel": True,
        "preco_promocional": None,
        "criado_em": datetime.now().isoformat(),
    },
    {
        "id": 2,
        "nome": "Carbonara",
        "categoria": "massa",
        "preco": 52.0,
        "disponivel": True,
        "preco_promocional": None,
        "criado_em": datetime.now().isoformat(),
    },
]


def database_path() -> Path:
    path = Path(settings.database_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_connection():
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS pratos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                disponivel INTEGER NOT NULL DEFAULT 1,
                preco_promocional REAL,
                criado_em TEXT NOT NULL
            )
            """)
        total = connection.execute("SELECT COUNT(*) FROM pratos").fetchone()[0]
        if total == 0:
            connection.executemany(
                """
                INSERT INTO pratos (
                    id, nome, categoria, preco, disponivel,
                    preco_promocional, criado_em
                )
                VALUES (
                    :id, :nome, :categoria, :preco, :disponivel,
                    :preco_promocional, :criado_em
                )
                """,
                [
                    {**prato, "disponivel": int(prato["disponivel"])}
                    for prato in PRATOS_INICIAIS
                ],
            )


def row_to_dict(row):
    data = dict(row)
    data["disponivel"] = bool(data["disponivel"])
    return data


def listar_pratos_db(categoria=None, apenas_disponiveis=False):
    init_db()
    query = "SELECT * FROM pratos"
    clauses = []
    params = []
    if categoria:
        clauses.append("categoria = ?")
        params.append(categoria)
    if apenas_disponiveis:
        clauses.append("disponivel = 1")
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id"

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
    return [row_to_dict(row) for row in rows]


def buscar_prato_db(prato_id):
    init_db()
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM pratos WHERE id = ?",
            (prato_id,),
        ).fetchone()
    return row_to_dict(row) if row else None


def criar_prato_db(prato):
    init_db()
    payload = prato.model_dump()
    criado_em = datetime.now().isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO pratos (
                nome, categoria, preco, disponivel,
                preco_promocional, criado_em
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload["nome"],
                payload["categoria"],
                payload["preco"],
                int(payload.get("disponivel", True)),
                payload.get("preco_promocional"),
                criado_em,
            ),
        )
        novo_id = cursor.lastrowid
    return buscar_prato_db(novo_id)
