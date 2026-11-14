"""
Validação e preparação das imagens recebidas pela API.
"""
from io import BytesIO

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

FORMATOS_PERMITIDOS = {"JPEG", "PNG", "WEBP"}
TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024  # 10 MB

# Mesmas transformações usadas na validação do treinamento (treinar.py)
transformacao = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class ImagemInvalidaError(Exception):
    """Erro de validação da imagem, com o status HTTP correspondente."""

    def __init__(self, status_code: int, mensagem: str):
        super().__init__(mensagem)
        self.status_code = status_code
        self.mensagem = mensagem


def validar_imagem(conteudo: bytes) -> Image.Image:
    """
    Verifica tamanho, formato e integridade do arquivo e retorna a imagem carregada.
    """
    if not conteudo:
        raise ImagemInvalidaError(400, "Arquivo vazio.")

    if len(conteudo) > TAMANHO_MAXIMO_BYTES:
        raise ImagemInvalidaError(413, "Arquivo excede o tamanho máximo de 10 MB.")

    try:
        imagem = Image.open(BytesIO(conteudo))
    except UnidentifiedImageError:
        raise ImagemInvalidaError(415, "Formato não suportado. Envie uma imagem JPEG, PNG ou WebP.")

    if imagem.format not in FORMATOS_PERMITIDOS:
        raise ImagemInvalidaError(415, "Formato não suportado. Envie uma imagem JPEG, PNG ou WebP.")

    try:
        # verify() checa a estrutura do arquivo, mas invalida o objeto;
        # por isso a imagem é reaberta e carregada por completo em seguida.
        imagem.verify()
        imagem = Image.open(BytesIO(conteudo))
        imagem.load()
    except (OSError, SyntaxError, Image.DecompressionBombError):
        raise ImagemInvalidaError(400, "Imagem corrompida ou incompleta.")

    return imagem


def preparar_imagem(imagem: Image.Image) -> torch.Tensor:
    """
    Converte a imagem para RGB e aplica as transformações do modelo,
    retornando um tensor no formato (1, 3, 224, 224).
    """
    return transformacao(imagem.convert("RGB")).unsqueeze(0)
