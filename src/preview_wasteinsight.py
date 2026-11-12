
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

DATASET_DIR = Path("data/WasteInsight")
OUTPUT_DIR = Path("data/WasteInsight_previews")

IMAGES_PER_SHEET = 150
COLUMNS = 10
THUMB_WIDTH = 150
THUMB_HEIGHT = 100
CELL_HEIGHT = 125

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for split in ["train", "valid", "test"]:
    split_dir = DATASET_DIR / split
    annotations_file = split_dir / "_annotations.coco.json"

    with open(annotations_file, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    images = dataset["images"]

    for sheet_number, start in enumerate(
        range(0, len(images), IMAGES_PER_SHEET), start=1
    ):
        batch = images[start:start + IMAGES_PER_SHEET]
        rows = (len(batch) + COLUMNS - 1) // COLUMNS

        sheet = Image.new(
            "RGB",
            (COLUMNS * THUMB_WIDTH, rows * CELL_HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(sheet)

        for index, image_data in enumerate(batch):
            image_path = split_dir / image_data["file_name"]

            if not image_path.exists():
                print(f"Imagem não encontrada: {image_path}")
                continue

            try:
                with Image.open(image_path) as original:
                    image = ImageOps.exif_transpose(original).convert("RGB")
                    image.thumbnail((THUMB_WIDTH - 10, THUMB_HEIGHT - 5))

                column = index % COLUMNS
                row = index // COLUMNS

                x = column * THUMB_WIDTH
                y = row * CELL_HEIGHT

                sheet.paste(image, (x + 5, y + 5))

                filename = Path(image_data["file_name"]).name
                draw.text(
                    (x + 5, y + THUMB_HEIGHT + 5),
                    f"{split} ID:{image_data['id']} {filename[:12]}",
                    fill="black"
                )

            except Exception as error:
                print(f"Erro ao abrir {image_path}: {error}")

        output_file = OUTPUT_DIR / f"{split}_{sheet_number:02d}.jpg"
        sheet.save(output_file, quality=90)

        print(f"Gerada: {output_file}")

print("\nVisualização concluída!")
