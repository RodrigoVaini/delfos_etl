from datetime import datetime
from typing import List

from fastapi import FastAPI, Query, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Data

app = FastAPI(
    title="Delfos Energy Source Data API",
    description="""
API responsável por expor os dados do banco fonte do teste técnico.

Funcionalidades:
- Consulta por intervalo de tempo
- Seleção de uma ou mais variáveis
- Retorno em formato JSON para consumo pelo processo ETL
""",
    version="1.0.0",
    contact={
        "name": "Rodrigo Vaini de Freitas",
    },
)

ALLOWED_VARIABLES = {"wind_speed", "power", "ambient_temperature"}


@app.get(
    "/data",
    tags=["Data"],
    summary="Consultar dados históricos por intervalo",
    description="""
Retorna os registros da tabela `data` filtrados por intervalo de tempo.

É possível informar uma ou mais variáveis no parâmetro `variables`.
Exemplos:
- `wind_speed`
- `power`
- `ambient_temperature`
""",
)
def get_data(
    start: datetime = Query(
        ...,
        description="Data/hora inicial da consulta no formato ISO 8601.",
        example="2025-01-01T00:00:00",
    ),
    end: datetime = Query(
        ...,
        description="Data/hora final da consulta no formato ISO 8601.",
        example="2025-01-01T23:59:59",
    ),
    variables: List[str] = Query(
        default=["wind_speed", "power"],
        description="Lista de variáveis que devem ser retornadas.",
        example=["wind_speed", "power"],
    ),
):
    invalid_vars = [v for v in variables if v not in ALLOWED_VARIABLES]
    if invalid_vars:
        raise HTTPException(
            status_code=400,
            detail=f"Variáveis inválidas: {invalid_vars}. Permitidas: {sorted(ALLOWED_VARIABLES)}"
        )

    db: Session = SessionLocal()
    try:
        query = db.query(Data).filter(Data.timestamp.between(start, end))
        rows = query.all()

        result = []
        for row in rows:
            item = {"timestamp": row.timestamp}
            for variable in variables:
                item[variable] = getattr(row, variable)
            result.append(item)

        return result
    finally:
        db.close()