from fastapi import Request, HTTPException

import jwt

CHAVE = "ironexecutions_super_secreto_2025"


async def verificar_token(request: Request):

    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Token não enviado")

    try:
        tipo, token = auth_header.split()

        if tipo.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Tipo de token inválido")

        payload = jwt.decode(token, CHAVE, algorithms=["HS256"])

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
