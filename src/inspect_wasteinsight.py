import json
from pathlib import Path

for split in ["train", "valid", "test"]:
    arquivo = Path(f"data/WasteInsight/{split}/_annotations.coco.json")

    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    categorias = dados.get("categories", [])
    anotacoes = dados.get("annotations", [])
    imagens = dados.get("images", [])

    print(f"\n--- {split.upper()} ---")
    print(f"Imagens: {len(imagens)}")
    print(f"Anotações: {len(anotacoes)}")
    print("Categorias:")

    for categoria in categorias:
        print(f"  - {categoria['name']}")