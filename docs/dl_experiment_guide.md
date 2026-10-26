# Optional Deep Learning Experiment: Visual Similarity for Jewellery Images

**This is a stretch task, not required to publish the first portfolio version today.**

## What it demonstrates

The script uses a pretrained MobileNetV3 model to convert images into numeric feature vectors (embeddings) and computes cosine similarity between the vectors. This is an exploratory image-retrieval prototype, not a jewellery-specific product matcher.

## Data and permission

Add at least two JPG, JPEG, PNG or WebP images that you created, own, or have permission to process to `assets/jewellery_images/`. Do not put customer photos or private client material in a public repository.

## Setup

1. Open the official PyTorch installation selector: https://pytorch.org/get-started/locally/
2. Select Windows, Pip, Python, and CPU unless you have verified GPU compatibility.
3. Run the generated installation command in your activated project environment. Install Pillow and scikit-learn if not already installed.
4. From the project root, run `python experiments/dl_image_similarity.py`.

The first run may download model weights. If time, disk space, or internet access is limited, skip this experiment; do not let it delay the dashboard launch.

## Evaluation and limitations

Inspect the output pairs manually. General ImageNet features can group images by background, colour, or composition instead of jewellery design. For a credible portfolio, report where it works and fails, and do not claim accuracy without a jewellery-specific labelled test set. The script does not fine-tune or train a model on jewellery data.
