
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from pathlib import Path

DISPOSITIVO = torch.device("cpu")

# Carregar modelo
checkpoint = torch.load(
    "models/mobilenetv3_coletacerta.pth",
    map_location=DISPOSITIVO
)

modelo = models.mobilenet_v3_small(weights=None)
modelo.classifier[3] = nn.Linear(
    modelo.classifier[3].in_features, 2
)

modelo.load_state_dict(checkpoint["modelo"])
modelo.eval()

classes = checkpoint["classes"]

transformacao = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Escolher imagem
caminho = input("Digite o caminho da imagem: ").strip().strip('"')

if not Path(caminho).is_file():
    print("Imagem não encontrada!")
    raise SystemExit

imagem = Image.open(caminho).convert("RGB")
imagem = transformacao(imagem).unsqueeze(0)

# Fazer previsão
with torch.no_grad():
    saida = modelo(imagem)
    probabilidades = torch.softmax(saida, dim=1)[0]

indice = probabilidades.argmax().item()

print("\nRESULTADO")
print(f"Classificação: {classes[indice]}")

for i, classe in enumerate(classes):
    print(f"{classe}: {probabilidades[i].item():.2%}")
