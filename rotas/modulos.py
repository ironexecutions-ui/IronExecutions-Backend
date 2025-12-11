from fastapi import APIRouter
from database import conectar

router = APIRouter()

@router.get("/modulos/empresa/{comercio_id}")
def listar_modulos_empresa(comercio_id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            mc.id,
            mc.modulo,
            COALESCE(mc.ativo, 1) AS ativo,
            m.descricao
        FROM modulos_comercio mc
        INNER JOIN modulos m ON m.modulo = mc.modulo
        WHERE mc.comercio_cadastrado_id = %s
        AND m.ativo = 1
        ORDER BY mc.id ASC
    """, (comercio_id,))

    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return lista
@router.get("/modulos/ativos")
def listar_modulos_ativos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT modulo, descricao 
        FROM modulos
        WHERE ativo = 1
    """)

    lista = cursor.fetchall()

    cursor.close()
    conn.close()
    return lista
@router.put("/modulos/solicitar")
def solicitar_modulo(body: dict):
    comercio_id = body.get("comercio_id")
    modulo = body.get("modulo")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO modulos_comercio (comercio_cadastrado_id, modulo, ativo)
        VALUES (%s, %s, 0)
    """, (comercio_id, modulo))

    conn.commit()
    cursor.close()
    conn.close()

    return { "mensagem": "Módulo solicitado com sucesso" }
