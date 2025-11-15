from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas.funcionarios import router as funcionarios_router
from rotas.servicos import router as servicos_router
from rotas.ganhos import router as ganhos_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas
app.include_router(funcionarios_router, prefix="/api")
app.include_router(servicos_router)
app.include_router(ganhos_router)

@app.get("/")
def raiz():
    return {"status": "API Iron Executions funcionando"}
