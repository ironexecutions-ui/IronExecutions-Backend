from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas.funcionarios import router as funcionarios_router
from rotas.servicos import router as servicos_router
from rotas.ganhos import router as ganhos_router
from rotas.contratos import router as contratos_router
from rotas.pdf import router as pdf_router

app = FastAPI()

origins = [
    "https://ironexecutions.com.br",
   "https://ironexecutions-frontend.onrender.com",
    "http://localhost:5173",
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(funcionarios_router, prefix="/api")
app.include_router(servicos_router)
app.include_router(ganhos_router)
app.include_router(contratos_router)
app.include_router(pdf_router)

@app.get("/")
def raiz():
    return {"status": "API Iron Executions funcionando"}
