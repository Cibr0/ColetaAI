
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torchvision.models import MobileNet_V3_Small_Weights
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path

DISPOSITIVO = torch.device("cpu")

transformacao = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

dataset = datasets.ImageFolder(
    Path("data/processado/teste"),
    transform=transformacao
)

carregador = DataLoader(
    dataset,
    batch_size=16,
    shuffle=False,
    num_workers=0
)

modelo = models.mobilenet_v3_small(weights=None)
modelo.classifier[3] = nn.Linear(
    modelo.classifier[3].in_features, 2
)

checkpoint = torch.load(
    "models/mobilenetv3_coletacerta.pth",
    map_location=DISPOSITIVO
)

modelo.load_state_dict(checkpoint["modelo"])
modelo.to(DISPOSITIVO)
modelo.eval()

previsoes = []
rotulos_reais = []

with torch.no_grad():
    for imagens, rotulos in carregador:
        saidas = modelo(imagens.to(DISPOSITIVO))
        previsoes.extend(saidas.argmax(dim=1).cpu().tolist())
        rotulos_reais.extend(rotulos.tolist())

nomes = dataset.classes

print("\nRELATÓRIO DE CLASSIFICAÇÃO")
print(classification_report(
    rotulos_reais,
    previsoes,
    target_names=nomes,
    digits=4
))

print("MATRIZ DE CONFUSÃO")
print(confusion_matrix(rotulos_reais, previsoes))

acertos = sum(
    real == previsto
    for real, previsto in zip(rotulos_reais, previsoes)
)

print(f"\nAcurácia geral: {acertos / len(rotulos_reais):.2%}")
print("\nIMAGENS CLASSIFICADAS INCORRETAMENTE")

for i, (real, previsto) in enumerate(zip(rotulos_reais, previsoes)):
    if real != previsto:
        caminho = dataset.samples[i][0]

        print(f"\nImagem: {caminho}")
        print(f"Classe real: {nomes[real]}")
        print(f"Previsão do modelo: {nomes[previsto]}")

from PIL import Image, ImageDraw
from pathlib import Path

erros = [
    (dataset.samples[i][0], nomes[real], nomes[previsto])
    for i, (real, previsto) in enumerate(zip(rotulos_reais, previsoes))
    if real != previsto
]

folha = Image.new("RGB", (1000, 750), "white")
desenho = ImageDraw.Draw(folha)

for i, (caminho, real, previsto) in enumerate(erros):
    imagem = Image.open(caminho).convert("RGB")
    imagem.thumbnail((300, 300))

    x = 20 + (i % 3) * 330
    y = 20 + (i // 3) * 370

    folha.paste(imagem, (x, y))
    desenho.text(
        (x, y + 310),
        f"Real: {real} | Modelo: {previsto}",
        fill="black"
    )
    desenho.text(
        (x, y + 330),
        Path(caminho).name,
        fill="black"
    )

folha.save("erros_teste.jpg")
print("\nFolha salva em erros_teste.jpg")