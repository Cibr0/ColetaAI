
import json
from pathlib import Path

annotations_path = Path("data/TACO/annotations.json")

with open(annotations_path, "r", encoding="utf-8") as file:
    dataset = json.load(file)

# Identifica as imagens que possuem pelo menos uma anotação
images_with_trash = {
    annotation["image_id"]
    for annotation in dataset["annotations"]
}

total_images = len(dataset["images"])
total_with_trash = len(images_with_trash)
total_without_annotations = total_images - total_with_trash

print(f"Total de imagens: {total_images}")
print(f"Imagens com anotações: {total_with_trash}")
print(f"Imagens sem anotações: {total_without_annotations}")
