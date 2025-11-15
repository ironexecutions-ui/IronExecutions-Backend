from fastapi import APIRouter, Request
from database import conectar

router = APIRouter()

# verificar email
@router.get("/verificar-email")
def verificar_email(email: str):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    if dados:
        return {"existe": True}
    return {"existe": False}


# verificar senha
@router.post("/verificar-senha")
async def verificar_senha(request: Request):
    body = await request.json()
    email = body.get("email")
    senha = body.get("senha")

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
    cursor.execute(query, (email, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return {"ok": True}
    
    return {"ok": False}


@router.get("/dados-funcionario")
def dados_funcionario(email: str):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    dados = cursor.fetchone()

    cursor.close()
    conn.close()

    return dados


# ============================================
# NOVAS ROTAS PARA FUNCIONÁRIOS
# ============================================

# listar todos
@router.get("/usuarios/todos")
def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


# inserir novo
@router.post("/usuarios/inserir")
async def inserir_usuario(request: Request):
    body = await request.json()

    nome = body.get("nome")
    sobrenome = body.get("sobrenome")
    email = body.get("email")
    senha = body.get("senha")
    funcao = body.get("funcao")
    responsabilidade = body.get("responsabilidade")
    porcentagem = body.get("porcentagem")
    foto = body.get("foto")

    conn = conectar()
    cursor = conn.cursor()

    query = """
        INSERT INTO usuarios (nome, sobrenome, email, senha, funcao, responsabilidade, porcentagem, foto)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nome, sobrenome, email, senha, funcao, responsabilidade, porcentagem, foto))
    conn.commit()

    cursor.close()
    conn.close()

    return {"ok": True, "mensagem": "Usuário criado com sucesso"}


# atualizar usuário
@router.put("/usuarios/atualizar")
async def atualizar_usuario(request: Request):
    body = await request.json()

    id = body.get("id")
    nome = body.get("nome")
    sobrenome = body.get("sobrenome")
    email = body.get("email")
    senha = body.get("senha")
    funcao = body.get("funcao")
    responsabilidade = body.get("responsabilidade")
    porcentagem = body.get("porcentagem")
    foto = body.get("foto")

    conn = conectar()
    cursor = conn.cursor()

    query = """
        UPDATE usuarios
        SET nome = %s, sobrenome = %s, email = %s, senha = %s,
            funcao = %s, responsabilidade = %s, porcentagem = %s, foto = %s
        WHERE id = %s
    """
    cursor.execute(query, (nome, sobrenome, email, senha, funcao, responsabilidade, porcentagem, foto, id))
    conn.commit()

    cursor.close()
    conn.close()

    return {"ok": True, "mensagem": "Usuário atualizado com sucesso"}


# apagar usuário
@router.delete("/usuarios/apagar")
def apagar_usuario(id: int):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"ok": True, "mensagem": "Usuário apagado com sucesso"}
