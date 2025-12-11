from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas.funcionarios import router as funcionarios_router
from rotas.servicos import router as servicos_router
from rotas.ganhos import router as ganhos_router
from rotas.contratos import router as contratos_router
from rotas.comercios_cadastrados import router as comercios_cadastrados_router
from rotas.cadastro_comercio import router as cadastro_comercio_router
from rotas.supabase import router as supabase_router
from rotas.comercios import router as comercio_router
from rotas.clientes import router as clientes_router
from rotas.login_clientes import router as login_clientes_router
from rotas.pdf import router as pdf_router
from dotenv import load_dotenv
load_dotenv()
from rotas.modulos import router as modulos_router
from rotas.modalmodulos import router as modalmodulos_router
from rotas.modulos_publico import router as modulos_publicos_router
from rotas.produtos_servicos import router as produtos_servicos_router

from rotas.retornmodulos import router as retornmodulos_router


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
app.include_router(clientes_router)
app.include_router(comercio_router)
app.include_router(comercios_cadastrados_router)
app.include_router(ganhos_router)
app.include_router(modulos_publicos_router)
app.include_router(supabase_router)
app.include_router(cadastro_comercio_router)
app.include_router(produtos_servicos_router, prefix="/api")

app.include_router(contratos_router)
app.include_router(login_clientes_router)
app.include_router(pdf_router)
app.include_router(modulos_router)
app.include_router(modalmodulos_router)
app.include_router(retornmodulos_router)

@app.get("/")
def raiz():
    return {"status": "API Iron Executions funcionando"}

from database import conectar
# =====================================================
# ROTA NOVA PARA LISTAR CONTRATOS – SEM CONFLITO
# =====================================================
@app.get("/listar-contratos")
def listar_contratos_novo():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome_cliente, telefone_cliente, codigo, apagado
        FROM contratos
        ORDER BY id DESC
    """)

    contratos = cursor.fetchall()
    cursor.close()
    conn.close()

    return contratos
