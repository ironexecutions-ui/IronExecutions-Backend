from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import uuid

router = APIRouter()

# Conectar ao Supabase
SUPABASE_URL = "https://mtljmvivztkgoolnnwxc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im10bGptdml2enRrZ29vbG5ud3hjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzQwMzM0MywiZXhwIjoyMDc4OTc5MzQzfQ.XFJVnYVbK-pxJ7oftduk680YsXltdUB06Yr_buIoJPA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/upload/imagem")
async def upload_imagem(
    arquivo: UploadFile = File(...),
    pasta: str = Form(...)
):
    conteudo = await arquivo.read()

    # Gerar nome único
    ext = arquivo.filename.split(".")[-1]
    nome_unico = f"{uuid.uuid4()}.{ext}"

    caminho = f"{pasta}/{nome_unico}"

    # Upload Supabase
    resp = supabase.storage.from_("assinaturas").upload(caminho, conteudo)

    # Obter URL pública
    url_final = supabase.storage.from_("assinaturas").get_public_url(caminho)

    return {
        "ok": True,
        "url": url_final
    }
