import sys
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Garante que a raiz do repositório esteja no sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from api.imagem import (
    TAMANHO_MAXIMO_BYTES,
    ImagemInvalidaError,
    preparar_imagem,
    validar_imagem,
)
from api.modelo import classificar

app = FastAPI(
    title="ColetaAI API",
    description="API de inferência para classificação e validação de imagens de resíduos do projeto Coleta Certa.",
    version="0.1.0",
)

# Configuração de CORS para permitir requisições de outros serviços/front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Geral"])
def read_root():
    """
    Rota raiz da aplicação. Retorna informações básicas sobre o status da API.
    """
    return {
        "status": "online",
        "message": "API ColetaAI está operacional.",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Monitoramento"])
def health_check():
    """
    Endpoint para verificação de integridade da aplicação (health check).
    """
    return {
        "status": "healthy"
    }


@app.post("/validar-foto", tags=["Validação"])
def validar_foto(imagem: UploadFile = File(..., description="Imagem JPEG, PNG ou WebP (até 10 MB)")):
    """
    Recebe uma imagem, valida formato e integridade, classifica com o modelo
    e retorna a classificação com as probabilidades.
    """
    # Lê um byte além do limite para detectar arquivos grandes sem carregá-los inteiros
    conteudo = imagem.file.read(TAMANHO_MAXIMO_BYTES + 1)

    try:
        imagem_validada = validar_imagem(conteudo)
        tensor = preparar_imagem(imagem_validada)
    except ImagemInvalidaError as erro:
        raise HTTPException(status_code=erro.status_code, detail=erro.mensagem)

    resultado = classificar(tensor)

    return {
        "status": "recebida",
        "arquivo": imagem.filename,
        "formato": imagem_validada.format,
        "largura": imagem_validada.width,
        "altura": imagem_validada.height,
        "tamanho_bytes": len(conteudo),
        "tensor": list(tensor.shape),
        **resultado,
    }


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )