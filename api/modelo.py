"""Carregamento do modelo treinado e inferência."""

from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

CAMINHO_MODELO = Path(_file_).resolve().parent.parent / "models" / "mobilenetv3_coletacerta.pth"
DISPOSITIVO = torch.device("cpu")


def _carregar_modelo():
    checkpoint = torch.load(CAMINHO_MODELO, map_location=DISPOSITIVO)

    modelo = models.mobilenet_v3_small(weights=None)
    modelo.classifier[3] = nn.Linear(modelo.classifier[3].in_features, 2)
    modelo.load_state_dict(checkpoint["modelo"])
    modelo.to(DISPOSITIVO)
    modelo.eval()

    return modelo, checkpoint["classes"]


# Executado uma única vez, na inicialização da API
modelo, CLASSES = _carregar_modelo()


def classificar(tensor: torch.Tensor) -> dict:
    """
    Recebe o tensor (1, 3, 224, 224) e retorna a classe prevista
    com as probabilidades de cada classe.
    """
    with torch.no_grad():
        saida = modelo(tensor.to(DISPOSITIVO))
        probabilidades = torch.softmax(saida, dim=1)[0]

    indice = probabilidades.argmax().item()

    return {
        "classificacao": CLASSES[indice],
        "probabilidades": {
            classe: round(probabilidades[i].item(), 4)
            for i, classe in enumerate(CLASSES)
        },
    }