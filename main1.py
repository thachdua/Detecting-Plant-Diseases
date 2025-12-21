import streamlit as st
import tensorflow as tf
import numpy as np
import base64
from pathlib import Path
from recommendation_vi import get_recommendation, get_quick_ref_markdown  # ⟵ THÊM HÀM NÀY


# =========================
# CẤU HÌNH CƠ BẢN
# =========================
st.set_page_config(
    page_title="Nhận diện bệnh cây trồng",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

ASSETS_DIR = Path("assets")

# =========================
# CSS TUỲ BIẾN (FRONTEND)
# =========================
CUSTOM_CSS = """
<style>
:root{
  --brand:#1c7c54;
  --brand-2:#3aa17e;
  --brand-3:#e6f4ef;
  --text:#0f172a;
  --muted:#64748b;
  --card-bg:#ffffff;
  --shadow:0 10px 25px rgba(16,24,40,0.08);
  --radius:18px;
}

html, body, [data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, #f7faf9 0%, #f0f7f4 100%);
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji","Segoe UI Emoji";
}

/* Ẩn watermark "Made with Streamlit" nếu bạn muốn (tùy chọn) */
/* footer {visibility: hidden;} */

h1,h2,h3{letter-spacing:0.2px}
h1{
  font-weight:800; 
  font-size: clamp(28px, 4vw, 40px);
  line-height:1.15;
}
h2{
  font-weight:700;
  margin-top: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background: white;
  border-right: 1px solid #eef2f7;
}
section[data-testid="stSidebar"] .stSelectbox, 
section[data-testid="stSidebar"] .stButton{
  padding: 4px 0 6px 0;
}

/* Card chung */
.card{
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 22px 22px;
  border: 1px solid #edf2f7;
}

/* Hero */
.hero{
  border-radius: 28px;
  padding: clamp(18px, 2vw, 26px);
  background: linear-gradient(135deg, var(--brand-3), #ffffff 40%, #f3fbf7 100%);
  border: 1px solid #e7f2ee;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: clamp(12px, 2vw, 28px);
  align-items: center;
}
.hero .title{
  font-weight: 800;
  font-size: clamp(28px, 4vw, 44px);
  color: #0b3d2e;
}
.hero .subtitle{
  color: var(--muted);
  font-size: clamp(14px, 1.5vw, 16px);
  margin-top: 8px;
}
.hero .cta{
  display:flex; gap:10px; margin-top:16px;
}
.hero .btn{
  background: var(--brand);
  color: white; 
  border: none;
  border-radius: 12px;
  padding: 10px 16px;
  font-weight: 700;
  box-shadow: 0 8px 18px rgba(28,124,84,0.18);
  cursor: pointer;
  transition: transform .06s ease-in-out, box-shadow .2s;
}
.hero .btn:hover{ transform: translateY(-1px); }
.hero .btn.secondary{
  background: #ffffff; color: var(--brand);
  border: 1px solid #cfe8de;
}

/* Badge */
.badge{
  display:inline-flex; align-items:center; gap:8px;
  background: #f0fbf6; color: #0b6849;
  border: 1px solid #cbeee0;
  padding: 6px 10px; border-radius: 999px; font-weight: 700; font-size: 12px;
}

/* Lưới thẻ tính năng */
.features{
  display:grid; grid-template-columns: repeat(3, 1fr); gap: 18px;
}
.feature{
  background: white; border-radius: var(--radius); padding: 18px;
  border: 1px solid #edf2f7; box-shadow: var(--shadow);
}
.feature h4{ margin:0 0 6px 0}
.feature p{ color: var(--muted); font-size: 14px; margin:0 }

/* Expander đẹp hơn */
details{
  background: white; border-radius: 14px; border: 1px solid #e9eef5; padding: 10px 14px;
}
summary{ cursor:pointer; font-weight:700; }

/* Thanh xác suất */
.prog{
  width: 100%; height: 10px; border-radius: 999px; background: #ecf3ef; overflow: hidden; border: 1px solid #e3ece6;
}
.prog > span{
  display:block; height: 100%; background: linear-gradient(90deg, var(--brand), var(--brand-2));
}

/* Gallery */
.gallery{
  display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
}
.gallery img{
  width: 100%; height: 180px; object-fit: cover; border-radius: 14px; border:1px solid #e8eef2;
  transition: transform .12s ease;
}
.gallery img:hover{ transform: scale(1.02) }

/* Nút chính Streamlit */
button[kind="primary"]{
  background: var(--brand);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# 1) TẢI MÔ HÌNH (CÓ CACHE)
# =========================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('trained_model.h5')

model = load_model()

# =========================
# 2) DANH MỤC LỚP (GIỮ NGUYÊN THỨ TỰ)
# =========================
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Nhóm các lớp theo loại cây để tiện lọc khi dự đoán
PLANT_TO_CLASSES = {}
for idx, cls in enumerate(CLASS_NAMES):
    plant = cls.split("___")[0]
    PLANT_TO_CLASSES.setdefault(plant, []).append((idx, cls))

PLANT_OPTIONS = sorted(PLANT_TO_CLASSES.keys())

# =========================
# 3) HÀM DỰ ĐOÁN
# =========================
def model_prediction(file):
    image = tf.keras.preprocessing.image.load_img(file, target_size=(128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.expand_dims(input_arr, axis=0)
    preds = model.predict(input_arr)
    idx = int(np.argmax(preds, axis=1)[0])
    conf = float(np.max(preds))
    prob_vec = preds[0]
    return idx, conf, prob_vec

# =========================
# TIỆN ÍCH: TẢI ẢNH & SLIDER
# =========================
def read_image_b64(path: Path):
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def image_slider_html(image_paths, height=340, interval_ms=2600):
    """
    Tạo slider ảnh đơn giản bằng HTML/JS (nhúng qua st.components.v1.html).
    Giữ nguyên f-string và dùng {{ }} cho dấu ngoặc nhọn của JS.
    """
    imgs_b64 = [read_image_b64(Path(p)) for p in image_paths if Path(p).exists()]
    if not imgs_b64:
        return "<div class='card'>Chưa tìm thấy ảnh cho slider.</div>"

    # thẻ <img> và dot
    img_tags = "\n".join([
        f"<img src='data:image/jpeg;base64,{b64}' "
        f"style='width:100%;height:{height}px;object-fit:cover;border-radius:18px;position:absolute;inset:0;opacity:0;transition:opacity .6s' />"
        for b64 in imgs_b64
    ])
    dots = "\n".join([
        "<span class='dot' style='width:8px;height:8px;border-radius:999px;background:#cfe0d9;margin:0 4px;display:inline-block;'></span>"
        for _ in imgs_b64
    ])

    html = f"""
    <div class="card" style="position:relative; overflow:hidden;">
      <div id="slider" style="position:relative; height:{height}px;">
        {img_tags}
      </div>
      <div style="position:absolute;right:14px;bottom:12px;display:flex;align-items:center;">{dots}</div>
    </div>
    <script>
      const imgs = [...document.querySelectorAll('#slider img')];
      const dots = [...document.querySelectorAll('.dot')];
      let cur = 0;
      function show(i){{
        imgs.forEach((im,idx)=>{{ im.style.opacity = (idx===i)? 1:0; }});
        dots.forEach((d,idx)=>{{ d.style.background = (idx===i)? '#1c7c54':'#cfe0d9'; }});
      }}
      show(cur);
      setInterval(()=>{{ cur = (cur+1)%imgs.length; show(cur); }}, {interval_ms});
    </script>
    """
    return html

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox(
    "Chọn trang",
    ["Home", "Giới thiệu", "Nhận diện bệnh", "Bộ sưu tập", "Bảng tra nhanh"]  # ⟵ THÊM TRANG MỚI
)

with st.sidebar:
    st.markdown("—")
    st.markdown(
        """
        <div class="card">
            <div class="badge">🌱 Gợi ý</div>
            <div style="margin-top:8px;color:#64748b">
                Ảnh rõ, đủ sáng và lá chiếm phần lớn khung hình sẽ cho kết quả tốt hơn.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# NỘI DUNG CÁC TRANG
# =========================
if app_mode == "Home":
    # HERO
    hero_img = ASSETS_DIR / "hero.jpg"  # đặt ảnh nền lớn
    logo_img = ASSETS_DIR / "logo.png"
    hero_left = f"""
    <div class="hero">
      <div>
        <div class="badge">AI for Smart Farming</div>
        <div class="title">Nhận diện bệnh cây trồng<br/>Nhanh – Chính xác – Dễ dùng</div>
        <div class="subtitle">Tải ảnh lá/cây để hệ thống phân tích và đưa ra khuyến nghị xử lý phù hợp.</div>
        <div class="cta">
          <a href="#" onclick="window.parent.postMessage({{type:'streamlit:setHash','hash':'#nhan-dien'}}, '*'); return false;">
            <button class="btn">🔎 Bắt đầu nhận diện</button>
          </a>
          <a href="#" onclick="window.parent.postMessage({{type:'streamlit:setHash','hash':'#gioi-thieu'}}, '*'); return false;">
            <button class="btn secondary">ℹ️ Tìm hiểu thêm</button>
          </a>
        </div>
      </div>
      <div>
        {"<img src='data:image/png;base64,"+read_image_b64(hero_img)+"' style='width:100%;border-radius:22px;border:1px solid #e8eef2'/>" if hero_img.exists() else ""}
      </div>
    </div>
    """
    st.markdown(hero_left, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # SLIDER ẢNH (JS)
    slider_paths = [
        ASSETS_DIR / "leaf_1.jpg",
        ASSETS_DIR / "leaf_2.jpg",
        ASSETS_DIR / "leaf_3.jpg",
    ]
    from streamlit.components.v1 import html as st_html
    st_html(image_slider_html([str(p) for p in slider_paths], height=320), height=360)

    # TÍNH NĂNG
    st.markdown("<h2>⚙️ Tính năng nổi bật</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="features">
      <div class="feature">
        <h4>Chuẩn đoán nhanh</h4>
        <p>Tải ảnh và nhận kết quả sau vài giây, không cần cài đặt phức tạp.</p>
      </div>
      <div class="feature">
        <h4>Khuyến nghị xử lý</h4>
        <p>Hiển thị hướng dẫn xử lý theo từng bệnh đã dự đoán.</p>
      </div>
      <div class="feature">
        <h4>Giao diện thân thiện</h4>
        <p>Thiết kế tối giản, tập trung vào thao tác chính, dễ dùng cho mọi đối tượng.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

elif app_mode == "Giới thiệu":
    st.markdown("<a name='gioi-thieu'></a>", unsafe_allow_html=True)
    st.header("Giới thiệu")
    st.markdown(
        """
- **Bộ dữ liệu** gồm nhiều trạng thái bệnh/khỏe cho các cây trồng phổ biến (cà chua, nho, ngô, khoai tây…).
- **Mô hình học sâu** được huấn luyện để nhận diện bệnh từ ảnh lá/cây.
- **Khuyến nghị xử lý** đi kèm giúp bạn lựa chọn phương án phù hợp (phòng/trị, canh tác).
- **Gợi ý sử dụng**: Ảnh nên rõ nét, đủ sáng; chủ thể (lá/cây) chiếm phần lớn khung hình.
        """
    )
    st.info("🔒 Mọi ảnh tải lên chỉ dùng để dự đoán trong phiên làm việc hiện tại.")

    with st.expander("📚 Bảng tra nhanh (mở để xem)"):
        st.markdown(get_quick_ref_markdown())

elif app_mode == "Bộ sưu tập":
    st.header("📸 Bộ sưu tập hình ảnh liên quan tới cây")
    # Hiển thị một lưới ảnh demo từ thư mục assets
    gallery_list = [
        ASSETS_DIR / "grape_leaf.jpg",
        ASSETS_DIR / "tomato_leaf.jpg",
        ASSETS_DIR / "corn_leaf.jpg",
        ASSETS_DIR / "leaf_1.jpg",
        ASSETS_DIR / "leaf_2.jpg",
        ASSETS_DIR / "leaf_3.jpg",
    ]
    html_imgs = []
    for p in gallery_list:
        if p.exists():
            b64 = read_image_b64(p)
            html_imgs.append(f"<img src='data:image/jpeg;base64,{b64}' alt='{p.name}'/>")
    if html_imgs:
        st.markdown(f"<div class='gallery'>{''.join(html_imgs)}</div>", unsafe_allow_html=True)
    else:
        st.warning("Chưa tìm thấy ảnh trong thư mục `assets/`. Hãy thêm ảnh và tải lại trang.")

elif app_mode == "Bảng tra nhanh":  # ⟵ TRANG MỚI
    st.header("📚 Bảng tra nhanh (IPM • FRAC/IRAC • Hoạt chất)")
    st.markdown(get_quick_ref_markdown())

else:  # Nhận diện bệnh
    st.markdown("<a name='nhan-dien'></a>", unsafe_allow_html=True)
    st.header("🔎 Nhận diện bệnh")
    with st.container():
        left, right = st.columns([1,1])
        with left:
            plant_choice = st.selectbox(
                "Chọn loại cây cần kiểm tra:",
                options=PLANT_OPTIONS,
                help="Hệ thống sẽ chỉ trả về các bệnh thuộc loại cây đã chọn."
            )
            test_image = st.file_uploader("Chọn ảnh lá/cây (jpg/png):", type=["jpg", "jpeg", "png"])
            show_btn = st.button("👁️ Hiển thị ảnh")
            predict_btn = st.button("🤖 Dự đoán")
        with right:
            st.markdown(
                """
                <div class="card">
                    <div class="badge">Hướng dẫn nhanh</div>
                    <ul style="margin-top:8px;color:#64748b">
                      <li>Ảnh rõ, ánh sáng tốt, hạn chế bóng đổ mạnh.</li>
                      <li>Lá/cây nên chiếm phần lớn khung hình.</li>
                      <li>Tránh nền phức tạp để tăng độ chính xác.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )

    if test_image and show_btn:
        st.image(test_image, use_column_width=True, caption="Ảnh đã chọn")

    if test_image and predict_btn:
        with st.spinner("Đang phân tích..."):
            idx, conf, prob_vec = model_prediction(test_image)
            # Lọc xác suất theo loại cây được chọn
            plant_classes = PLANT_TO_CLASSES.get(plant_choice, [])
            plant_indices = [i for i, _ in plant_classes]
            plant_probs = prob_vec[plant_indices]

            if plant_probs.size == 0:
                st.error("Danh sách bệnh của cây này đang trống.")
                st.stop()

            best_local_idx = int(np.argmax(plant_probs))
            best_global_idx = plant_indices[best_local_idx]
            label = CLASS_NAMES[best_global_idx]
            conf_within_group = float(plant_probs[best_local_idx])
            group_prob_sum = float(np.sum(plant_probs))
            normalized_conf = conf_within_group / group_prob_sum if group_prob_sum > 0 else 0.0

        # KẾT QUẢ
        st.markdown(
            f"""
            <div class="card">
              <div style="display:flex; align-items:center; gap:10px;">
                <span class="badge">Kết quả</span>
                <h3 style="margin:0;">{label}</h3>
              </div>
              <div style="margin-top:8px;color:#64748b">Độ tự tin trong nhóm {plant_choice}: <b>{normalized_conf:.2%}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # KHUYẾN NGHỊ
        with st.expander("📋 Khuyến nghị xử lý (Recommendation)"):
            st.markdown(get_recommendation(label))

        # TOP-5 XÁC SUẤT (thanh tiến độ đẹp)
        with st.expander(f"📈 Xác suất các lớp của {plant_choice} (Top-5)"):
            normalized_probs = plant_probs / group_prob_sum if group_prob_sum > 0 else plant_probs
            topk = sorted(
                list(zip([name for _, name in plant_classes], normalized_probs)),
                key=lambda x: x[1],
                reverse=True
            )[: min(5, len(plant_classes))]
            for cls, p in topk:
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;justify-content:space-between;margin:6px 2px;">
                      <div style="font-weight:600">{cls}</div>
                      <div style="color:#64748b">{p:.2%}</div>
                    </div>
                    <div class="prog"><span style="width:{p*100:.2f}%"></span></div>
                    """,
                    unsafe_allow_html=True
                )

    elif not test_image:
        st.info("Vui lòng chọn loại cây và tải một ảnh để bắt đầu.")