from fastapi import APIRouter
from database import conectar
from datetime import datetime, timedelta, date

router = APIRouter()

# ======================================================
# Função segura para converter qualquer formato de data
# ======================================================

def data_para_datetime(valor):
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, date):
        return datetime.combine(valor, datetime.min.time())
    if isinstance(valor, str):
        return datetime.strptime(valor, "%Y-%m-%d")
    raise ValueError(f"Data em formato inválido: {valor}")


# ======================================================
# GANHOS DO USUARIO LOGADO
# ======================================================

@router.get("/ganhos/mensais")
def ganhos_mensais(email: str):
    db = conectar()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, sobrenome, porcentagem 
        FROM usuarios 
        WHERE email = %s
    """, (email,))
    usuario = cursor.fetchone()

    if not usuario:
        return []

    porcentagem = usuario["porcentagem"]

    cursor.execute("""
        SELECT cliente, loja, data, valor, dias, link, processo
        FROM servicos
        WHERE processo = 'finalizado'
    """)

    servicos = cursor.fetchall()

    cursor.close()
    db.close()

    meses = {}

    for s in servicos:
        data_original = data_para_datetime(s["data"])
        data_recebimento = data_original + timedelta(days=s["dias"])

        mes = data_recebimento.strftime("%Y-%m")

        if mes not in meses:
            meses[mes] = {
                "mes": mes,
                "total_mes": 0,
                "servicos": []
            }

        meses[mes]["total_mes"] += float(s["valor"])
        meses[mes]["servicos"].append(s)

    resultado = []

    for mes, dados in meses.items():
        ganho_socio = dados["total_mes"] * porcentagem / 100

        resultado.append({
            "mes": mes,
            "usuario": usuario["nome"] + " " + usuario["sobrenome"],
            "porcentagem": porcentagem,
            "ganho_usuario": ganho_socio,
            "total_mes": dados["total_mes"],
            "servicos": dados["servicos"]
        })

    resultado.sort(key=lambda x: x["mes"], reverse=True)

    return resultado


# ======================================================
# GANHOS DE TODOS OS SÓCIOS
# ======================================================

@router.get("/ganhos/socios")
def ganhos_socios():
    db = conectar()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, nome, sobrenome, porcentagem
        FROM usuarios
        ORDER BY porcentagem DESC
    """)

    socios = cursor.fetchall()

    cursor.execute("""
        SELECT cliente, loja, data, valor, dias, link, processo
        FROM servicos
        WHERE processo = 'finalizado'
    """)

    servicos = cursor.fetchall()

    cursor.close()
    db.close()

    meses = {}

    for s in servicos:
        data_original = data_para_datetime(s["data"])
        data_recebimento = data_original + timedelta(days=s["dias"])

        mes = data_recebimento.strftime("%Y-%m")

        if mes not in meses:
            meses[mes] = []

        meses[mes].append(s)

    resultado = []

    for socio in socios:
        calc = []

        for mes, lista in meses.items():
            total = sum(float(s["valor"]) for s in lista)
            ganho_socio = total * socio["porcentagem"] / 100

            calc.append({
                "mes": mes,
                "total_mes": total,
                "ganho_socio": ganho_socio,
                "porcentagem": socio["porcentagem"],
                "nome": socio["nome"],
                "sobrenome": socio["sobrenome"]
            })

        resultado.append({
            "socio": socio["nome"] + " " + socio["sobrenome"],
            "porcentagem": socio["porcentagem"],
            "meses": calc
        })

    return resultado
