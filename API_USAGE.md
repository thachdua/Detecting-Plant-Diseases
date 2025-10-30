# Plant Disease Detection API Usage

This document summarizes how to run the FastAPI service that exposes the
plant disease detection model and how client applications can interact with it.

## 1. Environment setup

1. Create or activate a Python 3.9+ virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

> **Note**  
> The TensorFlow model file `trained_model.h5` must be present in the project
> root (it is already tracked in this repository). The service loads this file
> on demand when handling predictions.

## 2. Starting the server

Run the FastAPI application with Uvicorn:

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

The `--host 0.0.0.0` flag lets other machines on the same network reach the
service. You can omit it if you are running everything locally.

## 3. API endpoints

### `GET /health`

Simple health-check endpoint. Returns:

```json
{"status": "ok"}
```

### `POST /predict`

Accepts a single image file (JPG/PNG). The request must use the
`multipart/form-data` content type with a `file` field. Example using `curl`:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/leaf.jpg"
```

Example response:

```json
{
  "label": "Apple___Black_rot",
  "confidence": 0.92,
  "probabilities": [
    {"label": "Apple___Black_rot", "probability": 0.92},
    {"label": "Apple___Apple_scab", "probability": 0.04},
    {"label": "Apple___Cedar_apple_rust", "probability": 0.02},
    {"label": "Apple___healthy", "probability": 0.01},
    {"label": "Blueberry___healthy", "probability": 0.01},
    "..."
  ],
  "recommendation_markdown": "...",
  "filename": "leaf.jpg"
}
```

The `probabilities` array lists all known classes, sorted by likelihood in
descending order. `recommendation_markdown` contains the mitigation advice
pulled from `recommendation_vi.py` for the predicted disease. Client
applications can render it directly (it uses Markdown formatting).

## 4. Deployment considerations

- The model is loaded lazily and cached, so the first request will be slightly
  slower due to the loading time. Subsequent requests reuse the same model.
- The server enables permissive CORS by default, allowing mobile or web
  front-ends hosted on different origins to interact with it without extra
  configuration. If you need to restrict origins, edit the `allow_origins`
  list in `api_server.py`.
- Uvicorn's `--reload` flag is disabled in production mode. Use
  `uvicorn api_server:app --reload` during development to automatically reload
  after code changes.

## 5. Error handling

- Uploading an empty file or a file that cannot be decoded as an image results
  in a `400 Bad Request` response with a descriptive message in Vietnamese.
- Any unexpected error during inference will propagate as a `500 Internal Server
  Error`. Check the server logs if that happens.

By sharing this document and the `api_server.py` file with the app development
team, they have everything required to consume the AI service.
