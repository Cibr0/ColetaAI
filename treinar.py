
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from torchvision.models import MobileNet_V3_Small_Weights
from pathlib import Path

# Configurações
BASE = Path("data/processado")
EPOCAS = 10
BATCH_SIZE = 16
DISPOSITIVO = torch.device("cpu")

# Preparação das imagens
transformacoes = {
    "treino": transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ]),
    "validacao": transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
}

# Carregar datasets
datasets_imagens = {
    fase: datasets.ImageFolder(
        BASE / fase,
        transform=transformacoes[fase]
    )
    for fase in ["treino", "validacao"]
}

carregadores = {
    fase: DataLoader(
        datasets_imagens[fase],
        batch_size=BATCH_SIZE,
        shuffle=(fase == "treino"),
        num_workers=0
    )
    for fase in ["treino", "validacao"]
}

print("Classes:", datasets_imagens["treino"].classes)

# Modelo MobileNetV3
modelo = models.mobilenet_v3_small(
    weights=MobileNet_V3_Small_Weights.DEFAULT
)

modelo.classifier[3] = nn.Linear(
    modelo.classifier[3].in_features,
    2
)

modelo = modelo.to(DISPOSITIVO)

criterio = nn.CrossEntropyLoss()
otimizador = torch.optim.Adam(
    modelo.parameters(),
    lr=0.0001
)

# Treinamento
melhor_acuracia = 0.0
Path("models").mkdir(exist_ok=True)

for epoca in range(EPOCAS):
    print(f"\nÉpoca {epoca + 1}/{EPOCAS}")

    for fase in ["treino", "validacao"]:
        modelo.train() if fase == "treino" else modelo.eval()

        perda_total = 0.0
        acertos = 0
        total = 0

        with torch.set_grad_enabled(fase == "treino"):
            for imagens, rotulos in carregadores[fase]:
                imagens = imagens.to(DISPOSITIVO)
                rotulos = rotulos.to(DISPOSITIVO)

                if fase == "treino":
                    otimizador.zero_grad()

                saidas = modelo(imagens)
                perda = criterio(saidas, rotulos)

                if fase == "treino":
                    perda.backward()
                    otimizador.step()

                perda_total += perda.item() * imagens.size(0)
                previsoes = saidas.argmax(dim=1)
                acertos += (previsoes == rotulos).sum().item()
                total += rotulos.size(0)

        perda_media = perda_total / total
        acuracia = acertos / total

        print(
            f"{fase.capitalize()} - "
            f"Perda: {perda_media:.4f} | "
            f"Acurácia: {acuracia:.2%}"
        )

        if fase == "validacao" and acuracia > melhor_acuracia:
            melhor_acuracia = acuracia
            torch.save({
                "modelo": modelo.state_dict(),
                "classes": datasets_imagens["treino"].classes
            }, "models/mobilenetv3_coletacerta.pth")

print("\nTreinamento concluído!")
print(f"Melhor acurácia de validação: {melhor_acuracia:.2%}")
print("Modelo salvo em models/mobilenetv3_coletacerta.pth")
