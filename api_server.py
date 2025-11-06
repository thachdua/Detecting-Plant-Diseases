"""FastAPI server exposing plant disease prediction endpoints."""
from __future__ import annotations

import base64
import json
import logging
from functools import lru_cache
from io import BytesIO
from typing import Dict, List, Sequence

import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from urllib.parse import unquote
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


# --- (ĐÃ THÊM) Thiết lập OpenTelemetry ---
logger = logging.getLogger(__name__)

# 1. Tạo một "provider" (bộ cung cấp)


def _build_resource() -> Resource:
    """Tạo resource cho tracer provider, đảm bảo có service.name hợp lệ."""

    service_name = os.environ.get("OTEL_SERVICE_NAME", "detecting-plant-diseases-api").strip()
    if not service_name:
        service_name = "detecting-plant-diseases-api"
    return Resource.create({"service.name": service_name})


provider = TracerProvider(resource=_build_resource())

# 2. Tạo một "exporter" (bộ xuất)
#    Nó sẽ TỰ ĐỘNG đọc các biến môi trường OTEL_... mà bạn đã cài trên Render


def _has_scope_header(headers: list[str]) -> bool:
    """Kiểm tra xem danh sách header đã có trường X-Scope-OrgID/Grafana chưa."""

    for header in headers:
        header_lower = header.lower()
        if header_lower.startswith("x-scope-orgid=") or header_lower.startswith(
            "x-grafana-org-id="
        ) or header_lower.startswith("x-org-id="):
            return True
    return False


def _has_authorization(headers: list[str]) -> bool:
    """Kiểm tra danh sách header có Authorization hay không."""

    return any(item.lower().startswith("authorization=") for item in headers)


def _serialise_headers(headers: list[str]) -> str:
    """Ghép các header thành chuỗi, bỏ qua mục trống."""

    return ",".join(item for item in headers if item)


def _header_keys(headers: list[str]) -> str:
    """Trả về danh sách khóa header (ẩn giá trị) để ghi log an toàn."""

    if not headers:
        return "(none)"

    keys: list[str] = []
    for item in headers:
        key, sep, _ = item.partition("=")
        keys.append(key if sep else item)
    return ", ".join(keys)


def _unique_headers(headers: list[str]) -> list[str]:
    """Loại bỏ các header trùng nhau nhưng vẫn giữ nguyên thứ tự."""

    seen = set()
    deduped: list[str] = []
    for header in headers:
        key = header.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(header)
    return deduped


def _normalise_header_encoding(header: str) -> str:
    """Decode any phần trăm-encoding trong giá trị header."""

    if "=" not in header:
        return header

    key, value = header.split("=", 1)
    if "%" not in value:
        return header

    return f"{key}={unquote(value)}"


def _ensure_env_header(var_name: str, headers: list[str]) -> None:
    """Ghi lại danh sách header vào biến môi trường cụ thể."""

    os.environ[var_name] = _serialise_headers(_unique_headers(headers))


def _ensure_authorization_header(source: list[str], target: list[str]) -> None:
    """Đảm bảo target chứa Authorization, sao chép từ source nếu cần."""

    if _has_authorization(target):
        return  # Đã có, không cần làm gì

    # Nếu chưa có, tìm và sao chép từ source
        return

    for item in source:
        if item.lower().startswith("authorization="):
            target.append(item)
            break


def _decode_basic_credentials(encoded: str) -> tuple[str, str] | None:
    """Giải mã chuỗi Basic credentials (username:password)."""

    try:
        decoded = base64.b64decode(encoded).decode()
    except (ValueError, UnicodeDecodeError):
        return None

    username, sep, password = decoded.partition(":")
    if not sep:
        return None

    return username, password


def _extract_grafana_meta(username: str) -> tuple[str | None, dict | None]:
    """Tách slug Grafana và metadata từ username dạng glc_<payload>."""

    if not username.startswith("glc_"):
        return None, None

    grafana_meta = username[4:]
    padded_meta = grafana_meta + "=" * (-len(grafana_meta) % 4)
    try:
        meta_payload = base64.b64decode(padded_meta).decode()
        meta = json.loads(meta_payload)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None, None

    slug = str(meta.get("o", "")).strip() or None
    return slug, meta


def _infer_stack_id() -> str | None:
    """Thử suy ra stack slug của Grafana Cloud từ biến môi trường."""

    explicit_stack = os.environ.get("OTEL_GRAFANA_STACK_ID") or os.environ.get(
        "GRAFANA_STACK_SLUG"
    )
    if explicit_stack and explicit_stack.strip():
        return explicit_stack.strip()

    # Render luôn đặt RENDER_EXTERNAL_HOSTNAME = "<service>.onrender.com".
    hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME") or os.environ.get(
        "RENDER_EXTERNAL_URL"
    )
    if not hostname:
        return None

    # Nếu là URL đầy đủ thì bỏ phần giao thức.
    hostname = hostname.split("//", 1)[-1]
    slug = hostname.split(".", 1)[0]
    return slug.strip() if slug else None


def _scope_headers_from_authorization(headers: list[str]) -> list[str]:
    """Derive Grafana scope headers from the OTLP Authorization header."""

    for header in headers:
        key, _, value = header.partition("=")
        if key.lower() != "authorization":
            continue

        auth_value = value.strip()
        if not auth_value.lower().startswith("basic "):
            continue

        encoded_credentials = auth_value[6:].strip()
        credentials = _decode_basic_credentials(encoded_credentials)
        if not credentials:
            continue

        username, _ = credentials
        slug, _ = _extract_grafana_meta(username)
        if not slug:
            continue

        return [
            f"X-Scope-OrgID={slug}",
            f"X-Grafana-Org-Id={slug}",
        ]

    return []


def _log_authorization_diagnostics(headers: list[str]) -> None:
    """Ghi log debug về header Authorization (không lộ bí mật)."""

    if not logger.isEnabledFor(logging.DEBUG):
        return

    for item in headers:
        if not item.lower().startswith("authorization="):
            continue

        _, _, value = item.partition("=")
        scheme_value = value.strip()
        if not scheme_value:
            logger.debug("Authorization header tồn tại nhưng rỗng.")
            return

        scheme_lower = scheme_value.lower()
        if scheme_lower.startswith("basic "):
            encoded = scheme_value[6:].strip()
            credentials = _decode_basic_credentials(encoded)
            if not credentials:
                logger.debug(
                    "Authorization Basic không thể giải mã. Kiểm tra lại chuỗi base64."
                )
                return

            username, password = credentials
            slug, meta = _extract_grafana_meta(username)
            masked_user = (username[:8] + "…") if username else "(none)"
            region = None
            if meta:
                region = meta.get("m", {}).get("r")
            logger.debug(
                "Authorization Basic đã cấu hình (user=%s, password_length=%d, slug=%s, region=%s)",
                masked_user,
                len(password),
                slug or "(unknown)",
                region or "(unknown)",
            )
            return

        if scheme_lower.startswith("bearer "):
            token = scheme_value[7:].strip()
            logger.debug("Authorization Bearer đã cấu hình (token_length=%d)", len(token))
            return

        logger.debug("Authorization header sử dụng scheme không nhận diện: %s", scheme_value)
        return
        try:
            decoded = base64.b64decode(encoded_credentials).decode()
        except (ValueError, UnicodeDecodeError):
            continue

        username, _, _ = decoded.partition(":")
        if not username.startswith("glc_"):
            continue

        grafana_meta = username[4:]
        padded_meta = grafana_meta + "=" * (-len(grafana_meta) % 4)
        try:
            meta_payload = base64.b64decode(padded_meta).decode()
            meta = json.loads(meta_payload)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            continue

        candidate = str(meta.get("o", "")).strip()
        if not candidate:
            continue

        return [
            f"X-Scope-OrgID={candidate}",
            f"X-Grafana-Org-Id={candidate}",
        ]

    return []


def _ensure_grafana_scope_header() -> None:
    """Append Grafana Cloud scope header when missing.

    Render chỉ cho phép thiết lập biến môi trường dạng chuỗi. Người dùng
    thường cài `OTEL_EXPORTER_OTLP_HEADERS` với token nhưng bỏ quên header
    `X-Scope-OrgID`. Thiếu header này Grafana không biết stack nào để gán
    traces nên trả về lỗi 401 như thông báo "legacy auth cannot be upgraded".

    Nếu phát hiện biến `OTEL_GRAFANA_STACK_ID` (hoặc fallback
    `GRAFANA_STACK_SLUG`) thì tự động nối thêm header còn thiếu trước khi
    khởi tạo exporter. Cơ chế này không ghi đè những cấu hình đã có sẵn.
    """

    headers_raw = os.environ.get("OTEL_EXPORTER_OTLP_HEADERS", "")
    header_items = [
        _normalise_header_encoding(item.strip())
        for item in headers_raw.split(",")
        if item.strip()
    ]

    traces_headers_raw = os.environ.get("OTEL_EXPORTER_OTLP_TRACES_HEADERS")
    traces_headers_defined = bool(traces_headers_raw and traces_headers_raw.strip())
    traces_header_items = []
    if traces_headers_defined:
        traces_header_items = [
            _normalise_header_encoding(item.strip())
            for item in traces_headers_raw.split(",")
            if item.strip()
        ]

    scope_headers = []
    for candidate in header_items + traces_header_items:
        clower = candidate.lower()
        if clower.startswith("x-scope-orgid=") or clower.startswith(
            "x-grafana-org-id="
        ) or clower.startswith("x-org-id="):
            scope_headers.append(candidate)

    if not scope_headers:
        stack_id = _infer_stack_id()
        scope_source = "env"
        if stack_id:
            scope_headers = [
                f"X-Scope-OrgID={stack_id}",
                f"X-Grafana-Org-Id={stack_id}",
            ]
        else:
            scope_headers = _scope_headers_from_authorization(
                header_items + traces_header_items
            )
            scope_source = "authorization"

        if not scope_headers:
            logger.warning(
                "Chưa thể tự suy ra Grafana stack slug. Vui lòng đặt biến"
                " OTEL_GRAFANA_STACK_ID hoặc GRAFANA_STACK_SLUG."
            )
            return

        if scope_source == "env":
            logger.info(
                "Đã tự động bổ sung các header Grafana scope (%s) cho OTLP exporter",
                ", ".join(scope_headers),
            )
        else:
            logger.info(
                "Đã suy ra Grafana org ID từ Authorization và bổ sung header (%s)",
                ", ".join(scope_headers),
            )

    if not _has_scope_header(header_items):
        header_items.extend(scope_headers)
    if traces_headers_defined:
        if not _has_scope_header(traces_header_items):
            traces_header_items.extend(scope_headers)
        _ensure_authorization_header(header_items, traces_header_items)
        _ensure_authorization_header(traces_header_items, header_items)
        _ensure_env_header("OTEL_EXPORTER_OTLP_TRACES_HEADERS", traces_header_items)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "OTLP trace headers sau đồng bộ: %s",
                _header_keys(traces_header_items),
            )
    elif traces_headers_raw is not None and not traces_headers_raw.strip():
        # Nếu biến tồn tại nhưng rỗng, loại bỏ để exporter dùng chung cấu hình tổng quát.
        os.environ.pop("OTEL_EXPORTER_OTLP_TRACES_HEADERS", None)

    if not _has_authorization(header_items):
        logger.warning(
            "Không tìm thấy header Authorization trong OTEL_EXPORTER_OTLP_HEADERS. "
            "Grafana sẽ trả về 401 nếu thiếu thông tin xác thực."
        )
    else:
        _log_authorization_diagnostics(header_items)

    _ensure_env_header("OTEL_EXPORTER_OTLP_HEADERS", header_items)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "OTLP headers sau đồng bộ: %s",
            _header_keys(header_items),
        )


_ensure_grafana_scope_header()

if logger.isEnabledFor(logging.DEBUG):
    logger.debug(
        "OTLP headers hiện tại: %s",
        os.environ.get("OTEL_EXPORTER_OTLP_HEADERS", "(trống)"),
    )
    logger.debug(
        "OTLP trace headers hiện tại: %s",
        os.environ.get("OTEL_EXPORTER_OTLP_TRACES_HEADERS", "(trống)"),
    )

otlp_exporter = OTLPSpanExporter()

# 3. Gắn exporter vào provider
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# 4. Đặt nó làm provider mặc định toàn cục
trace.set_tracer_provider(provider)
# --- Kết thúc thiết lập OpenTelemetry ---


app = FastAPI(title="Plant Disease Detection API", version="1.0.0")

# --- (ĐÃ THÊM) Gắn OpenTelemetry vào ứng dụng FastAPI ---
FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)


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
