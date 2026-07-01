---
name: segment-anything-model
description: "SAM: zero-shot image segmentation via points, boxes, masks."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies:
  - segment-anything
  - "transformers>=4.30.0"
  - "torch>=1.7.0"
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags:
      - Multimodal
      - Image Segmentation
      - Computer Vision
      - SAM
      - Zero-Shot
---

# Segment Anything Model (SAM)

Comprehensive guide to using Meta AI's Segment Anything Model for zero‑shot image segmentation.

## When to use SAM

**Use SAM when:**

- You need to segment any object in images without task‑specific training.  
- Building interactive annotation tools with point/box prompts.  
- Generating training data for other vision models.  
- You need zero‑shot transfer to new image domains.  
- Building object detection/segmentation pipelines.  
- Processing medical, satellite, or other domain‑specific images.

### Key features

- **Zero‑shot segmentation** – works on any image domain without fine‑tuning.  
- **Flexible prompts** – points, bounding boxes, or previous masks.  
- **Automatic segmentation** – generate all object masks automatically.  
- **High quality** – trained on 1.1 billion masks from 11 million images.  
- **Multiple model sizes** – ViT‑B (fastest), ViT‑L, ViT‑H (most accurate).  
- **ONNX export** – deploy in browsers and edge devices.

### Alternatives

| Alternative | Typical use‑case |
|-------------|-----------------|
| YOLO / Detectron2 | Real‑time object detection with predefined classes |
| Mask2Former | Semantic / panoptic segmentation with categories |
| GroundingDINO + SAM | Text‑prompted segmentation |
| SAM 2 | Video segmentation tasks |

## Quick start

### Installation

```bash
# Install the official repo
pip install git+https://github.com/facebookresearch/segment-anything.git

# Optional visualisation / COCO utilities
pip install opencv-python pycocotools matplotlib

# Transformers (for the HF wrapper)
pip install transformers
```

### Download checkpoints

```bash
# ViT‑H (largest, most accurate) – 2.4 GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

# ViT‑L (medium) – 1.2 GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

# ViT‑B (smallest, fastest) – 375 MB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

### Basic usage with `SamPredictor`

```python
import cv2
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

# Load a model checkpoint
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
sam.to("cuda")                     # move to GPU (or "cpu")

# Create a predictor
predictor = SamPredictor(sam)

# Load and preprocess an image (once per image)
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# Predict with a single foreground point
input_point = np.array([[500, 375]])          # (x, y)
input_label = np.array([1])                  # 1 = foreground, 0 = background

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True                     # returns 3 mask candidates
)

# Keep the highest‑scoring mask
best_mask = masks[np.argmax(scores)]
```

### HuggingFace 🤗 Transformers wrapper

```python
import torch
from PIL import Image
from transformers import SamModel, SamProcessor

# Load the HF model & processor
model = SamModel.from_pretrained("facebook/sam-vit-huge")
processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")
model.to("cuda")

# Prepare inputs (batch of one image)
image = Image.open("image.jpg")
input_points = [[[450, 600]]]                # list‑of‑list for batch compatibility

inputs = processor(
    image,
    input_points=input_points,
    return_tensors="pt"
)
inputs = {k: v.to("cuda") for k, v in inputs.items()}

# Forward pass
with torch.no_grad():
    outputs = model(**inputs)

# Post‑process masks back to the original image size
masks = processor.image_processor.post_process_masks(
    outputs.pred_masks.cpu(),
    inputs["original_sizes"].cpu(),
    inputs["reshaped_input_sizes"].cpu()
)
```

## Core concepts

### Model architecture

<!-- ascii-guard-ignore -->
```
SAM Architecture:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │
│     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Image Embeddings      Prompt Embeddings         Masks + IoU
   (computed once)       (per prompt)             predictions
```
<!-- ascii-guard-ignore-end -->

### Model variants

| Model | Registry key | Checkpoint size | Speed   | Accuracy |
|-------|--------------|----------------|---------|----------|
| ViT‑H | `vit_h`      | 2.4 GB         | Slowest | Best     |
| ViT‑L | `vit_l`      | 1.2 GB         | Medium  | Good     |
| ViT‑B | `vit_b`      | 375 MB         | Fastest | Good     |

### Prompt types

| Prompt          | Description                | Typical use |
|-----------------|----------------------------|-------------|
| Point (fg)      | Click on object            | Single‑object selection |
| Point (bg)      | Click outside object       | Exclude regions |
| Bounding box    | Rectangle around object    | Larger objects |
| Previous mask   | Low‑res mask input         | Iterative refinement |

## Interactive segmentation

### Point prompts

```python
# Single foreground point
input_point = np.array([[500, 375]])
input_label = np.array([1])

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True
)

# Multiple points (foreground + background)
input_points = np.array([[500, 375], [600, 400], [450, 300]])
input_labels = np.array([1, 1, 0])   # 2 foreground, 1 background

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False          # single mask when prompts are clear
)
```

### Box prompts

```python
# Bounding box format: [x1, y1, x2, y2]
input_box = np.array([425, 600, 700, 875])

masks, scores, logits = predictor.predict(
    box=input_box,
    multimask_output=False
)
```

### Combined prompts

```python
# Box + point for precise control
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    box=np.array([400, 300, 700, 600]),
    multimask_output=False
)
```

### Iterative refinement

```python
# Initial prediction
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    multimask_output=True
)

# Refine with an additional background point, using the best mask as input
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375], [550, 400]]),
    point_labels=np.array([1, 0]),
    mask_input=logits[np.argmax(scores)][None, :, :],  # best mask as prior
    multimask_output=False
)
```

## Automatic mask generation

### Basic automatic segmentation

```python
from segment_anything import SamAutomaticMaskGenerator

# Initialise the generator (uses the same `sam` model as above)
mask_generator = SamAutomaticMaskGenerator(sam)

# Generate masks for the whole image
all_masks = mask_generator.generate(image)

# Each entry contains:
# - segmentation: binary mask (H×W)
# - bbox: [x, y, w, h]
# - area: pixel count
# - predicted_iou: quality estimate (0‑1)
# - stability_score: robustness estimate (0‑1)
# - point_coords: point that triggered the mask
```

### Customized generation

```python
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,               # denser grid → more masks
    pred_iou_thresh=0.88,
    stability_score_thresh=0.95,
    crop_n_layers=1,
    crop_n_points_downscale_factor=2,
    min_mask_region_area=100         # discard tiny masks
)

custom_masks = mask_generator.generate(image)
```

### Filtering masks

```python
# Sort by area (largest first)
sorted_masks = sorted(all_masks, key=lambda m: m["area"], reverse=True)

# Keep only high‑quality masks
high_iou = [m for m in sorted_masks if m["predicted_iou"] > 0.90]
stable   = [m for m in high_iou if m["stability_score"] > 0.95]
```

## Batched inference

### Multiple images

```python
import cv2
import numpy as np

# Load a list of images
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]

all_results = []
for img in images:
    predictor.set_image(img)
    masks, _, _ = predictor.predict(
        point_coords=np.array([[500, 375]]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_results.append(masks)
```

### Multiple prompts for a single image

```python
# Encode the image once
predictor.set_image(image)

point_sets = [
    np.array([[100, 100]]),
    np.array([[200, 200]]),
    np.array([[300, 300]])
]

refined_masks = []
for pts in point_sets:
    masks, scores, _ = predictor.predict(
        point_coords=pts,
        point_labels=np.array([1]),
        multimask_output=True
    )
    refined_masks.append(masks[np.argmax(scores)])
```

## ONNX deployment

### Export the model

```bash
python scripts/export_onnx_model.py \
    --checkpoint sam_vit_h_4b8939.pth \
    --model-type vit_h \
    --output sam_onnx.onnx \
    --return-single-mask
```

### Run inference with ONNX Runtime

```python
import onnxruntime
import numpy as np

# Load the exported ONNX model
ort_session = onnxruntime.InferenceSession("sam_onnx.onnx")

# Example inputs (image_embeddings must be computed beforehand)
outputs = ort_session.run(
    None,
    {
        "image_embeddings": image_embeddings,          # (1, C, H', W')
        "point_coords": point_coords,                  # (N, 2)
        "point_labels": point_labels,                  # (N,)
        "mask_input": np.zeros((1, 1, 256, 256), dtype=np.float32),
        "has_mask_input": np.array([0], dtype=np.float32),
        "orig_im_size": np.array([h, w], dtype=np.float32)
    }
)
# `outputs` contains the predicted masks (and optionally IoU scores)
```

## Common workflows

### Workflow 1 – Interactive annotation tool

```python
import cv2
import numpy as np

predictor = SamPredictor(sam)
predictor.set_image(image)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        masks, scores, _ = predictor.predict(
            point_coords=np.array([[x, y]]),
            point_labels=np.array([1]),
            multimask_output=True
        )
        # Visualise the best mask (implementation left to the user)
        display_mask(masks[np.argmax(scores)])

cv2.namedWindow("Annotate")
cv2.setMouseCallback("Annotate", on_click)
cv2.imshow("Annotate", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Workflow 2 – Object extraction with transparent background

```python
def extract_object(image, point):
    """Return an RGBA image where the object at `point` is isolated."""
    predictor.set_image(image)

    masks, scores, _ = predictor.predict(
        point_coords=np.array([point]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    best_mask = masks[np.argmax(scores)]

    # Build an RGBA output
    rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    rgba[..., :3] = image
    rgba[..., 3] = (best_mask * 255).astype(np.uint8)
    return rgba
```

### Workflow 3 – Medical image segmentation (grayscale → RGB)

```python
import cv2

# Load a grayscale scan and convert to 3‑channel RGB
medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)
rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)

predictor.set_image(rgb_image)

# Example ROI bounding box (replace with actual coordinates)
x