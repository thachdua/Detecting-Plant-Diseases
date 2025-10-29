# preprocessing.py
# Tiền xử lý ảnh để đưa vào mô hình nhận diện bệnh cây trồng

from __future__ import annotations
from io import BytesIO
from pathlib import Path
import re
import requests
import numpy as np
from PIL import Image, ImageOps, ImageFilter

# =========================
# CÁC TIỆN ÍCH CƠ BẢN
# =========================

def _is_url(x: str) -> bool:
    return isinstance(x, str) and x.startswith(("http://", "https://"))

def _sanitize_filename(name: str) -> str:
    name = name.strip().replace(" ", "_")
    return re.sub(r"[^-_.A-Za-z0-9]", "", name)

def load_image_any(src) -> Image.Image:
    """
    Nguồn có thể là:
      - URL (str bắt đầu bằng http/https)
      - đường dẫn file (str hoặc Path)
      - bytes hoặc file-like (ví dụ st.file_uploader trả về)
    Trả về: PIL.Image đã auto-orient theo EXIF & chuyển RGB.
    """
    if isinstance(src, (bytes, bytearray)):
        img = Image.open(BytesIO(src))
    elif hasattr(src, "read"):  # file-like (e.g., Streamlit UploadedFile)
        img = Image.open(src)
    elif _is_url(src):
        resp = requests.get(src, timeout=15)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
    else:
        p = Path(src)
        if not p.exists():
            raise FileNotFoundError(f"Không tìm thấy ảnh: {src}")
        img = Image.open(p)

    # Sửa xoay theo EXIF, bỏ alpha, convert RGB
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    return img


# =========================
# CẮT/RESIZE GIỮ TỶ LỆ
# =========================

def center_crop_square(im: Image.Image) -> Image.Image:
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return im.crop((left, top, left + side, top + side))

def letterbox_resize(im: Image.Image, target_size=(128, 128), pad_color=(255, 255, 255)) -> Image.Image:
    """
    Giữ tỷ lệ ảnh, scale sao cho cạnh dài = cạnh dài target, sau đó padding để vừa target_size.
    """
    W, H = target_size
    iw, ih = im.size
    scale = min(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    im_resized = im.resize((nw, nh), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (W, H), pad_color)
    left = (W - nw) // 2
    top = (H - nh) // 2
    canvas.paste(im_resized, (left, top))
    return canvas


# =========================
# LỌC NHIỄU (TÙY CHỌN NHẸ)
# =========================

def light_denoise(im: Image.Image, strength: str = "none") -> Image.Image:
    """
    'none' | 'median' | 'sharpen'
    - median: giảm nhiễu hột nhẹ
    - sharpen: tăng chi tiết nhẹ
    """
    if strength == "median":
        return im.filter(ImageFilter.MedianFilter(size=3))
    if strength == "sharpen":
        return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
    return im


# =========================
# HÀM CHÍNH: CHUẨN BỊ CHO MÔ HÌNH
# =========================

def prep_for_model(
    src,
    target_size=(128, 128),
    strategy: str = "letterbox",     # 'letterbox' hoặc 'center-crop'
    denoise: str = "none",           # 'none' | 'median' | 'sharpen'
    to_float32: bool = True,
    add_batch_dim: bool = True,
    normalize: str | None = None,    # None | '0_1' | 'imagenet'
):
    """
    Trả về mảng numpy shape (H, W, 3) hoặc (1, H, W, 3) tùy add_batch_dim.
    Mặc định theo code hiện tại của bạn, mô hình có thể đã có Rescaling layer bên trong,
    nên normalize=None là an toàn. Nếu cần, đặt normalize='0_1'.
    """
    im = load_image_any(src)
    im = light_denoise(im, strength=denoise)

    if strategy == "center-crop":
        im = center_crop_square(im)
        im = im.resize(target_size, Image.Resampling.LANCZOS)
    else:
        im = letterbox_resize(im, target_size, pad_color=(255, 255, 255))

    arr = np.asarray(im)  # uint8 [0..255]
    if to_float32:
        arr = arr.astype("float32")

    if normalize == "0_1":
        arr = arr / 255.0
    elif normalize == "imagenet":
        # Chuẩn ImageNet: scale 0..1 rồi trừ mean / chia std
        arr = arr / 255.0
        mean = np.array([0.485, 0.456, 0.406], dtype="float32")
        std  = np.array([0.229, 0.224, 0.225], dtype="float32")
        arr = (arr - mean) / std

    if add_batch_dim:
        arr = np.expand_dims(arr, axis=0)  # (1, H, W, 3)
    return arr


# =========================
# HÀM HỖ TRỢ TẢI NHIỀU ẢNH TỪ URL VỀ LƯU LOCAL (TÙY CHỌN)
# =========================

def download_and_save(url: str, save_dir: str | Path, filename: str | None = None) -> Path:
    """
    Tải ảnh từ URL và lưu về thư mục chỉ định.
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    if filename is None:
        filename = _sanitize_filename(Path(url).name or "image.jpg")
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filename += ".jpg"

    img = load_image_any(url)
    out_path = save_dir / filename
    img.save(out_path, quality=95, subsampling=1)
    return out_path
