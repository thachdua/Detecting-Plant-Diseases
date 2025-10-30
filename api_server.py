"""FastAPI server exposing plant disease prediction endpoints."""
from __future__ import annotations

from functools import lru_cache
from io import BytesIO
from typing import List

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from recommendation_vi import get_recommendation


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


def preprocess_image(contents: bytes) -> np.ndarray:
    """Convert raw bytes into a model-ready tensor."""
    try:
        image = tf.keras.utils.load_img(BytesIO(contents), target_size=(128, 128))
    except Exception as exc:  # pragma: no cover - FastAPI handles response
        raise HTTPException(status_code=400, detail="Không đọc được ảnh tải lên.") from exc

    array = tf.keras.utils.img_to_array(image)
    array = np.expand_dims(array, axis=0)
    return array


def predict(image_array: np.ndarray) -> dict:
    """Run inference and format the response payload."""
    model = load_model()
    preds = model.predict(image_array)
    idx = int(np.argmax(preds, axis=1)[0])
    confidence = float(np.max(preds))
    prob_vec = preds[0]

    # Prepare probability list sorted desc
    top_indices = np.argsort(prob_vec)[::-1]
    probabilities = [
        {"label": CLASS_NAMES[i], "probability": float(prob_vec[i])}
        for i in top_indices
    ]

    label = CLASS_NAMES[idx]
    recommendation = get_recommendation(label)

    return {
        "label": label,
        "confidence": confidence,
        "probabilities": probabilities,
        "recommendation_markdown": recommendation,
    }


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
async def predict_endpoint(file: UploadFile = File(...)) -> dict:
    """Accept an uploaded image and return the prediction results."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Tập tin tải lên rỗng.")

    image_array = preprocess_image(contents)
    result = predict(image_array)
    result["filename"] = file.filename
    return result


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
