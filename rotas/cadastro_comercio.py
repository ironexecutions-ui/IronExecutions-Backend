from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import conectar
import random
import string
import bcrypt

router = APIRouter(prefix="/cadastro")

# -----------------------------------------
# Funções auxiliares
# -----------------------------------------

def executar_select(conn, query, params=()):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    resultado = cursor.fetchall()
    cursor.close()
    return resultado

def executar_comando(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    last_id = cursor.lastrowid
    cursor.close()
    return last_id


def gerar_codigo_unico(conn, tabela, coluna, tamanho=20):
    while True:
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))
        resultado = executar_select(conn, f"SELECT {coluna} FROM {tabela} WHERE {coluna} = %s", (codigo,))
        if not resultado:
            return codigo

# -----------------------------------------
# Modelos
# -----------------------------------------

class Loja(BaseModel):
    loja: str
    imagem: str | None = None

class Personalizar(BaseModel):
    fundo: str
    letra_tipo: str
    letra_cor: str

class ModuloItem(BaseModel):
    id: int
    nome: str
    preco: float
    texto: str

class Cliente(BaseModel):
    email: str
    nome_completo: str
    senha: str
    cargo: str
    funcao: str
    matricula: str | None = None

class CadastroFinal(BaseModel):
    loja: Loja
    personalizar: Personalizar
    modulos: list[ModuloItem]
    cliente: Cliente

# -----------------------------------------
# ROTA FINAL - SALVA TUDO JUNTOS
# -----------------------------------------

@router.post("/finalizar")
def finalizar_cadastro(body: CadastroFinal):
    conn = conectar()

    try:
        conn.start_transaction()

        # 1. SALVA A LOJA
        comercio_id = executar_comando(conn,
            """
            INSERT INTO comercios_cadastradas (loja, imagem, fundo, letra_tipo, letra_cor)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                body.loja.loja,
                body.loja.imagem,
                body.personalizar.fundo,
                body.personalizar.letra_tipo,
                body.personalizar.letra_cor
            )
        )

        # 2. SALVA MODULOS
        for m in body.modulos:
            executar_comando(conn,
                """
                INSERT INTO modulos_comercio (comercio_cadastrado_id, modulo)
                VALUES (%s, %s)
                """,
                (comercio_id, m.nome)
            )

        # 3. SALVA CLIENTE
        existe = executar_select(conn, "SELECT id FROM clientes WHERE email = %s", (body.cliente.email,))
        if existe:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        senha_hash = bcrypt.hashpw(body.cliente.senha.encode(), bcrypt.gensalt()).decode()

        codigo_unico = gerar_codigo_unico(conn, "clientes", "codigo", 20)
        qrcode_unico = gerar_codigo_unico(conn, "clientes", "qrcode", 12)

        executar_comando(conn,
            """
            INSERT INTO clientes
            (email, nome_completo, senha, cargo, funcao, matricula, codigo, qrcode, comercio_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                body.cliente.email,
                body.cliente.nome_completo,
                senha_hash,
                body.cliente.cargo,
                body.cliente.funcao,
                body.cliente.matricula,
                codigo_unico,
                qrcode_unico,
                comercio_id
            )
        )

        conn.commit()

        return {
            "mensagem": "Cadastro concluído com sucesso",
            "codigo": codigo_unico,
            "qrcode": qrcode_unico
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

@router.get("/comercio/{id}")
def obter_comercio(id: int):
    conn = conectar()
    try:
        dados = executar_select(
            conn,
            "SELECT * FROM comercios_cadastradas WHERE id = %s",
            (id,)
        )

        if not dados:
            raise HTTPException(status_code=404, detail="Comércio não encontrado")

        return dados[0]

    finally:
        conn.close()
