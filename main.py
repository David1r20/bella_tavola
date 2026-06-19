from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routers import bebidas, pedidos, pratos, predict, reservas
from starlette.exceptions import HTTPException

from config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)


# Handlers de erro customizados (Exercicio 2.6 do caderno FastAPI)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "erro": "Dados invalidos",
                "detalhes": exc.errors(),
            }
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"erro": exc.detail})


# Inclusao dos routers (Exercicio 3 do caderno FastAPI)
app.include_router(pratos.router, prefix="/pratos", tags=["Pratos"])
app.include_router(bebidas.router, prefix="/bebidas", tags=["Bebidas"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(predict.router, prefix="/ml", tags=["Machine Learning"])


@app.get("/")
async def root():
    return {"message": f"Bem-vindo ao {settings.app_name}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
