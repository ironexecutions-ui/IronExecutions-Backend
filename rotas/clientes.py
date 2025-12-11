from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import executar_select
from .auth import verificar_token

router = APIRouter(prefix="/clientes")


class ClienteMe(BaseModel):
    id: int
    nome_completo: str
    cargo: str
    funcao: str
    codigo: str
    qrcode: str
    comercio_id: int | None = None
    modulos: dict | None = None



@router.get("/me")
async def get_me(usuario = Depends(verificar_token)):
    dados = executar_select(
        """
        SELECT id, nome_completo, cargo, funcao, codigo, qrcode, comercio_id
        FROM clientes
        WHERE id = %s
        """,
        (usuario["id"],)
    )

    if not dados:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente = dados[0]

    modulos = None

    if cliente["comercio_id"]:
        lista = executar_select(
            """
            SELECT produtividade, administracao, delivery_vendas,
            mesas_salao_cozinha, integracao_ifood, agendamentos,
            gerencial, fiscal
            FROM comercios_cadastradas
            WHERE id = %s
            """,
            (cliente["comercio_id"],)
        )

        if lista:
            modulos = lista[0]

    return {
        "id": cliente["id"],
        "nome_completo": cliente["nome_completo"],
        "cargo": cliente["cargo"],
        "funcao": cliente["funcao"],
        "codigo": cliente["codigo"],
        "qrcode": cliente["qrcode"],
        "comercio_id": cliente["comercio_id"],
        "modulos": modulos
    }
@router.get("/modulo")
def listar_modulos():
    return executar_select("SELECT * FROM modulos WHERE ativo = 1")
