
import csv
import random
import shutil
from pathlib import Path
from collections import Counter

random.seed(42)

BASE = Path("data")
DESTINO = BASE / "processado"

with open("classificacoes_final.csv", encoding="utf-8-sig") as arquivo:
    registros = list(csv.DictReader(arquivo))

# Usar apenas imagens válidas e inválidas
registros = [
    r for r in registros
    if r["classification"] in ("valida", "invalida")
]

# Separar TACO por classe: 70% treino, 15% validação, 15% teste
taco = [r for r in registros if r["dataset"] == "TACO"]
grupos = {"treino": [], "validacao": [], "teste": []}

for classe in ("valida", "invalida"):
    itens = [r for r in taco if r["classification"] == classe]
    random.shuffle(itens)

    n = len(itens)
    treino = round(n * 0.70)
    validacao = round(n * 0.15)

    grupos["treino"].extend(itens[:treino])
    grupos["validacao"].extend(itens[treino:treino + validacao])
    grupos["teste"].extend(itens[treino + validacao:])

# Acrescentar WasteInsight apenas ao treino
waste = [
    r for r in registros
    if r["dataset"] == "WasteInsight"
    and r["review_sheet"].startswith("train")
    and r["classification"] == "valida"
]
grupos["treino"].extend(waste)

# Criar pastas e copiar imagens
for divisao, itens in grupos.items():
    for item in itens:
        classe = item["classification"]
        if item["dataset"] == "TACO":
            origem = BASE / "TACO" / item["filename"]
        else:
            pasta = item["review_sheet"].split("_")[0]
            origem = BASE / "WasteInsight" / pasta / item["filename"]

        nome_unico = f"{item['dataset']}_{item['review_sheet']}_{item['image_id']}{origem.suffix}"
        destino = DESTINO / divisao / classe / nome_unico
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)

    print(f"\n{divisao.upper()}: {len(itens)} imagens")
    print(dict(Counter(x["classification"] for x in itens)))

print("\nDataset preparado em:", DESTINO)
