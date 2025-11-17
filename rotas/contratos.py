from fastapi import APIRouter, HTTPException
from database import conectar
import random
import string
from datetime import datetime

router = APIRouter()


# ====================================
# Função para gerar código único
# ====================================
def gerar_codigo():
    return "".join(random.choice(string.digits) for _ in range(12))



def gerar_codigo_unico(cursor):
    while True:
        codigo = gerar_codigo()
        cursor.execute("SELECT id FROM contratos WHERE codigo = %s", (codigo,))
        existe = cursor.fetchone()
        if not existe:
            return codigo
# ====================================
# Criar um novo contrato
# ====================================
@router.post("/contratos/novo")
async def novo_contrato(dados: dict):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    codigo = gerar_codigo_unico(cursor)
    criado_em = datetime.now()

    try:
        cursor.execute("""
            INSERT INTO contratos (
                codigo, criado_em, atualizado_em,
                representante_nome, documento_empresa, endereco_empresa, telefone_empresa, email_empresa,
                negocio_cliente,
                nome_cliente, documento_cliente, endereco_cliente, telefone_cliente, email_cliente,
                tipo_site, tecnologias, quantidade_paginas,
                integracoes, numero_revisoes,
                prazo_entrega,
                valor_total, forma_pagamento, valor_entrada, valor_final_entrega,
                valor_revisao_extra,
                hospedagem_inclusa, valor_hospedagem,
                dias_suporte,
                cidade_foro,
                data_assinatura_contratada, data_assinatura_cliente,
                LOGO_ASSINATURA_CONTRATADA, LOGO_ASSINATURA_CLIENTE,
                atualizacoes_inclusas
            )
            VALUES (
                %s, %s, NULL,
                %s, %s, %s, %s, %s,
                %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s,
                %s, %s, %s, %s,
                %s,
                %s, %s,
                %s,
                %s,
                %s, %s,
                %s, %s,
                %s
            )
        """, (
            codigo, criado_em,
            dados.get("representante_nome"), dados.get("documento_empresa"), dados.get("endereco_empresa"),
            dados.get("telefone_empresa"), dados.get("email_empresa"),
            dados.get("negocio_cliente"),
            dados.get("nome_cliente"), dados.get("documento_cliente"), dados.get("endereco_cliente"),
            dados.get("telefone_cliente"), dados.get("email_cliente"),
            dados.get("tipo_site"), dados.get("tecnologias"), dados.get("quantidade_paginas"),
            dados.get("integracoes"), dados.get("numero_revisoes"),
            dados.get("prazo_entrega"),
            dados.get("valor_total"), dados.get("forma_pagamento"),
            dados.get("valor_entrada"), dados.get("valor_final_entrega"),
            dados.get("valor_revisao_extra"),
            dados.get("hospedagem_inclusa"), dados.get("valor_hospedagem"),
            dados.get("dias_suporte"),
            dados.get("cidade_foro"),
            dados.get("data_assinatura_contratada"), dados.get("data_assinatura_cliente"),
            None,  # LOGO_ASSINATURA_CONTRATADA
            None,  # LOGO_ASSINATURA_CLIENTE
            dados.get("atualizacoes_inclusas")
        ))

        conn.commit()
        return {"ok": True, "codigo": codigo}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# ====================================
# Listar todos os contratos (somente nome e telefone)
# ====================================
@router.get("/contratos")
def listar_contratos():

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
      SELECT 
    id AS id,
    nome_cliente,
    telefone_cliente,
    codigo
FROM contratos
ORDER BY id DESC

    """)

    contratos = cursor.fetchall()

    cursor.close()
    conn.close()

    return contratos


# ====================================
# Visualizar contrato completo
# ====================================
@router.get("/contratos/{id_contrato}")
def ver_contrato(id_contrato: int):

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM contratos WHERE id = %s", (id_contrato,))
    contrato = cursor.fetchone()

    cursor.close()
    conn.close()

    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    return contrato


# ====================================
# Salvar assinatura (cliente ou contratada)
# ====================================
@router.post("/contratos/salvar-assinatura")
def salvar_assinatura(id_contrato: int, tipo: str, url: str):

    if tipo not in ["cliente", "contratada"]:
        raise HTTPException(status_code=400, detail="Tipo inválido. Use cliente ou contratada.")

    conn = conectar()
    cursor = conn.cursor()

    coluna_assinatura = (
        "LOGO_ASSINATURA_CLIENTE"
        if tipo == "cliente"
        else "LOGO_ASSINATURA_CONTRATADA"
    )

    coluna_data = (
        "data_assinatura_cliente"
        if tipo == "cliente"
        else "data_assinatura_contratada"
    )

    try:
        cursor.execute(
            f"""
            UPDATE contratos 
            SET {coluna_assinatura} = %s,
                {coluna_data} = NOW()
WHERE id = %s
            """,
            (url, id_contrato)
        )

        conn.commit()
        return {"ok": True, "mensagem": "Assinatura salva com sucesso"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()
@router.get("/contratos/codigo/{codigo}")
def ver_contrato_codigo(codigo: str):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM contratos WHERE codigo = %s", (codigo,))
    contrato = cursor.fetchone()

    cursor.close()
    conn.close()

    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")

    return contrato
# ====================================
# Atualizar contrato existente
# ====================================
@router.put("/contratos/{id_contrato}")
def atualizar_contrato(id_contrato: int, dados: dict):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE contratos SET
                atualizado_em = NOW(),
                representante_nome = %s,
                documento_empresa = %s,
                endereco_empresa = %s,
                telefone_empresa = %s,
                email_empresa = %s,

                negocio_cliente = %s,
                nome_cliente = %s,
                documento_cliente = %s,
                endereco_cliente = %s,
                telefone_cliente = %s,
                email_cliente = %s,

                tipo_site = %s,
                tecnologias = %s,
                quantidade_paginas = %s,

                integracoes = %s,
                numero_revisoes = %s,

                prazo_entrega = %s,

                valor_total = %s,
                forma_pagamento = %s,
                valor_entrada = %s,
                valor_final_entrega = %s,
                valor_revisao_extra = %s,

                hospedagem_inclusa = %s,
                valor_hospedagem = %s,

                dias_suporte = %s,
                cidade_foro = %s,

                data_assinatura_contratada = %s,
                data_assinatura_cliente = %s,

                atualizacoes_inclusas = %s
            WHERE id = %s
        """, (
            dados.get("representante_nome"),
            dados.get("documento_empresa"),
            dados.get("endereco_empresa"),
            dados.get("telefone_empresa"),
            dados.get("email_empresa"),

            dados.get("negocio_cliente"),
            dados.get("nome_cliente"),
            dados.get("documento_cliente"),
            dados.get("endereco_cliente"),
            dados.get("telefone_cliente"),
            dados.get("email_cliente"),

            dados.get("tipo_site"),
            dados.get("tecnologias"),
            dados.get("quantidade_paginas"),

            dados.get("integracoes"),
            dados.get("numero_revisoes"),

            dados.get("prazo_entrega"),

            dados.get("valor_total"),
            dados.get("forma_pagamento"),
            dados.get("valor_entrada"),
            dados.get("valor_final_entrega"),
            dados.get("valor_revisao_extra"),

            dados.get("hospedagem_inclusa"),
            dados.get("valor_hospedagem"),

            dados.get("dias_suporte"),
            dados.get("cidade_foro"),

            dados.get("data_assinatura_contratada"),
            dados.get("data_assinatura_cliente"),

            dados.get("atualizacoes_inclusas"),

            id_contrato
        ))

        conn.commit()
        return {"ok": True, "mensagem": "Contrato atualizado com sucesso"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()
# ====================================
# Apagar contrato
# ====================================
@router.delete("/contratos/{id_contrato}")
def apagar_contrato(id_contrato: int):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM contratos WHERE id = %s", (id_contrato,))
        conn.commit()

        return {"ok": True, "mensagem": "Contrato apagado com sucesso"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()
