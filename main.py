from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from routers import pratos, bebidas, reservas, predict, pedidos
from config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)


# Handlers de erro customizados (Exercício 2.5 do Caderno 2)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"erro": "Dados inválidos", "detalhes": exc.errors()}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"erro": exc.detail})


# Inclusão dos routers (Exercício 3 do Caderno 2 e Caderno 3)
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
