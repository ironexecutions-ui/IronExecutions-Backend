from fastapi import APIRouter, Depends, HTTPException
from database import executar_select
from .auth import verificar_token

router = APIRouter()

@router.get("/produtos_servicos/buscar")
def buscar_produtos(query: str, usuario=Depends(verificar_token)):

    # 1. Buscar comercio_id correto pela tabela clientes
    sql_cliente = """
        SELECT comercio_id
        FROM clientes
        WHERE id = %s
    """
    dados_cliente = executar_select(sql_cliente, (usuario["id"],))

    if not dados_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    comercio_id = dados_cliente[0]["comercio_id"]

    # 2. Caso não tenha comercio vinculado
    if comercio_id is None:
        return []

    # 3. Se query estiver vazia
    if not query or query.strip() == "":
        return []

    # 4. Buscar produtos do comércio
    sql = """
        SELECT id, nome, unidade, codigo_barras, qrcode, preco, preco_recebido,
               categoria, imagem_url, tempo_servico
        FROM produtos_servicos
        WHERE comercio_id = %s
        AND disponivel = 1
        AND (
            nome LIKE %s
            OR codigo_barras = %s
            OR qrcode = %s
        )
        ORDER BY nome ASC
        LIMIT 20
    """

    dados = executar_select(sql, (
        comercio_id,
        f"%{query}%",
        query,
        query
    ))

    return dados
