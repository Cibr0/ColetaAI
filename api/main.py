import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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


if __name__ == "__main__":
    # Garante que a raiz do repositório esteja no sys.path
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
