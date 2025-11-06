"""FastAPI server exposing plant disease prediction endpoints."""
from __future__ import annotations

from functools import lru_cache
from io import BytesIO
from typing import Dict, List, Sequence

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Note: recommendation text is not returned by the API per request.


@lru_cache(maxsize=1)
def load_model() -> tf.keras.Model:
    """Load and cache the trained TensorFlow model."""
    return tf.keras.models.load_model("trained_model.h5")


CLASS_NAMES: List[str] = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]


def _build_plant_mappings(class_names: Sequence[str]) -> Dict[str, List[int]]:
    """Group class indices by plant name extracted from the label."""

    plant_to_indices: Dict[str, List[int]] = {}
    for idx, label in enumerate(class_names):
        plant = label.split("___")[0]
        plant_to_indices.setdefault(plant, []).append(idx)
    return plant_to_indices


PLANT_TO_CLASS_INDICES: Dict[str, List[int]] = _build_plant_mappings(CLASS_NAMES)


def preprocess_image(contents: bytes) -> np.ndarray:
    """Convert raw bytes into a model-ready tensor."""
    try:
        image = tf.keras.utils.load_img(BytesIO(contents), target_size=(128, 128))
    except Exception as exc:  # pragma: no cover - FastAPI handles response
        raise HTTPException(status_code=400, detail="Không đọc được ảnh tải lên.") from exc

    array = tf.keras.utils.img_to_array(image)
    array = np.expand_dims(array, axis=0)
    return array


def predict(image_array: np.ndarray, *, plant: str | None = None) -> dict:
    """Run inference and format the response payload.

    Changes made per request:
    - Only return result when reported confidence > 0.80 (80%).
    - Do not include recommendation_markdown in the response.
    - Split label into `plant` and `disease` fields.
    """
    THRESHOLD = 0.80

    model = load_model()
    preds = model.predict(image_array)
    prob_vec = preds[0]

    restricted_indices: Sequence[int] | None = None
    if plant:
        restricted_indices = PLANT_TO_CLASS_INDICES.get(plant)

    if restricted_indices:
        plant_probs = prob_vec[list(restricted_indices)]
        best_local_idx = int(np.argmax(plant_probs))
        best_global_idx = restricted_indices[best_local_idx]
        full_label = CLASS_NAMES[best_global_idx]
        confidence_raw = float(prob_vec[best_global_idx])

        group_prob_sum = float(np.sum(plant_probs))
        normalized_conf = (
            float(plant_probs[best_local_idx] / group_prob_sum)
            if group_prob_sum > 0
            else 0.0
        )

        # Use normalized confidence within the selected plant group as the sole
        # decision metric per user's request. Do not return per-class probabilities.
        reported_normalized = normalized_conf

        if reported_normalized < THRESHOLD:
            raise HTTPException(
                status_code=422,
                detail=f"Độ tự tin trong nhóm ({reported_normalized:.2%}) dưới ngưỡng {THRESHOLD:.0%}"
            )

        # Split predicted label and return only normalized probability (no raw probs)
        _, disease = full_label.split("___", 1)

        return {
            "plant": plant,
            "disease": disease,
            "normalized_probability": reported_normalized,
        }

    # Default behaviour: evaluate all classes and require raw confidence > THRESHOLD
    idx = int(np.argmax(prob_vec))
    confidence_raw = float(prob_vec[idx])

    if confidence_raw < THRESHOLD:
        raise HTTPException(
            status_code=422,
            detail=f"Độ tự tin ({confidence_raw:.2%}) dưới ngưỡng {THRESHOLD:.0%}"
        )

    top_indices = np.argsort(prob_vec)[::-1]
    probabilities = []
    for i in top_indices:
        cls_full = CLASS_NAMES[i]
        parts = cls_full.split("___", 1)
        plant_name = parts[0]
        disease_name = parts[1] if len(parts) > 1 else ""
        probabilities.append(
            {
                "plant": plant_name,
                "disease": disease_name,
                "probability": float(prob_vec[i]),
            }
        )

    full_label = CLASS_NAMES[idx]
    parts = full_label.split("___", 1)
    plant_name = parts[0]
    disease_name = parts[1] if len(parts) > 1 else ""

    return {
        "plant": plant_name,
        "disease": disease_name,
        "confidence": confidence_raw,
        "probabilities": probabilities,
    }


app = FastAPI(title="Plant Disease Detection API", version="1.0.0")
app = FastAPI(title="Plant Disease Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}


@app.post("/predict")
async def predict_endpoint(
    file: UploadFile = File(...),
    plant: str | None = None,
) -> dict:
    """Accept an uploaded image and return the prediction results."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Tập tin tải lên rỗng.")

    if plant and plant not in PLANT_TO_CLASS_INDICES:
        raise HTTPException(status_code=400, detail="Loại cây không hợp lệ.")

    image_array = preprocess_image(contents)
    result = predict(image_array, plant=plant)
    result["filename"] = file.filename
    return result


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
