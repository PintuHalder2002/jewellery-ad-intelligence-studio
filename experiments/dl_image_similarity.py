"""Optional pretrained computer-vision demo for similarity between images.

This does NOT train a deep neural network. It extracts image embeddings from a
pretrained MobileNetV3 model and compares them with cosine similarity. The
model is not jewellery-specific; results must be manually evaluated and are
not proof of commercial quality.

Usage after optional dependencies are installed and at least two permitted
images are copied into assets/jewellery_images/:
    python experiments/dl_image_similarity.py

The first run may download pretrained weights. CPU use is supported but can be
slower. Use images you own or have permission to process.
"""
from __future__ import annotations

from pathlib import Path
import sys

import torch
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets" / "jewellery_images"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def main() -> int:
    files = sorted(path for path in IMAGE_DIR.iterdir() if path.suffix.lower() in EXTENSIONS)
    if len(files) < 2:
        print(f"Add at least 2 licensed/owned images to: {IMAGE_DIR}")
        return 1

    weights = MobileNet_V3_Small_Weights.DEFAULT
    preprocess = weights.transforms()
    model = mobilenet_v3_small(weights=weights)
    model.classifier = torch.nn.Identity()
    model.eval()
    vectors = []
    processed_files = []

    for path in files:
        try:
            with Image.open(path) as image:
                tensor = preprocess(image.convert("RGB")).unsqueeze(0)
            with torch.inference_mode():
                embedding = model(tensor).squeeze(0).cpu().numpy()
            vectors.append(embedding)
            processed_files.append(path)
            print(f"Processed: {path.name}")
        except Exception as exc:
            print(f"Skipping {path.name}: {exc}")

    if len(vectors) < 2:
        print("Could not process at least two images.")
        return 1

    matrix = cosine_similarity(vectors)
    pairs = []
    for i in range(len(processed_files)):
        for j in range(i + 1, len(processed_files)):
            pairs.append((float(matrix[i, j]), processed_files[i].name, processed_files[j].name))
    pairs.sort(reverse=True)

    print("\nMOST SIMILAR IMAGE PAIRS (cosine similarity; exploratory only)")
    for score, left, right in pairs[:10]:
        print(f"{score:.3f}  |  {left}  <->  {right}")
    print("\nCaution: an ImageNet-pretrained model is not jewellery-specific. Inspect matches manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
