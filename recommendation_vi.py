# -*- coding: utf-8 -*-
"""
Khuyến nghị xử lý (tiếng Việt) cho hệ thống nhận diện bệnh cây trồng.

Lưu ý quan trọng:
- Luôn tuân thủ NHÃN THUỐC/BIG BOOK tại địa phương (tên thương phẩm, hoạt chất,
  liều lượng, thời gian cách ly PHI, thời gian cách ly vào vườn REI…).
- Ưu tiên IPM (quản lý dịch hại tổng hợp) và luân phiên nhóm FRAC/IRAC/HRAC để giảm kháng thuốc.
- Nội dung mang tính tham khảo học thuật; không thay thế tư vấn kỹ thuật tại chỗ.
"""

# =========================
# Khối khuyến nghị chung
# =========================

DEFAULT_HEALTHY = """\
**Tình trạng: Lá khỏe**
- Duy trì chăm sóc: tưới tiêu hợp lý, bón phân cân đối (N-P-K + hữu cơ).
- Tăng đề kháng: bổ sung vi lượng (Ca, Mg, Zn, B) khi cần.
- Phòng ngừa: vệ sinh vườn, loại bỏ lá già/khô; theo dõi định kỳ nấm/khuẩn/côn trùng.
"""

IPM_BLOCK = """\
**✅ IPM – Quản lý dịch hại tổng hợp**
- **Giống, giá thể, cây con sạch bệnh**; xử lý hạt/khay theo quy định cho phép.
- **Luân canh & quản lý tàn dư**: vùi/tiêu hủy tàn dư bệnh; hạn chế gieo trồng liên tiếp cùng họ cây.
- **Thông thoáng tán**: tỉa cành/lá gốc; tưới gốc, tránh ẩm lá buổi chiều.
- **Bón cân đối**: tránh dư đạm; bổ sung Ca–Mg–B–Zn khi thiếu; tăng hữu cơ/vi sinh cải tạo đất.
- **Giám sát dịch hại** (scouting): theo dõi tuần–đợt; phun khi **vượt ngưỡng** khuyến cáo.
- **Luân phiên hoạt chất** theo **FRAC/IRAC/HRAC**; không lặp một nhóm quá 2 lần liên tiếp.
"""

SAFETY_MEDICAL = """\
**🩺 An toàn & Y tế khi pha–phun**
- **PPE**: găng hóa chất, kính, khẩu trang/respirator đạt chuẩn, quần áo dài tay, ủng; không ăn/uống/hút thuốc khi pha–phun.
- **Pha thuốc** nơi thoáng; tránh gió ngược; không trộn nếu nhãn **cấm phối**.
- **REI/PHI**: tuân thủ thời gian cách ly vào vườn (**REI**) và cách ly thu hoạch (**PHI**).
- **Sau phun**: rửa tay, tắm, thay đồ; xử lý bao bì theo quy định, **không** xả ra nguồn nước.
- **Sự cố & sơ cứu**:
  - **Hít phải**: chuyển ngay ra nơi thoáng, nới lỏng quần áo; theo dõi hô hấp.
  - **Dính da/mắt**: rửa dưới nước sạch 15–20 phút.
  - **Nuốt phải**: **không gây nôn** trừ khi có hướng dẫn y tế; mang nhãn thuốc tới cơ sở y tế.
  - Liên hệ **115** hoặc cơ sở y tế/TT chống độc địa phương.
"""

RESISTANCE_NOTES = """\
**🧬 Ghi chú kháng thuốc**
- **FRAC 3 (DMI/triazole)**, **FRAC 11 (QoI/strobilurin)**, **FRAC 1 (MBC)**… dễ kháng nếu lạm dụng.
- Luân phiên **cơ chế khác nhau**; dùng **hỗn hợp** theo nhãn khi được phép; hạn chế số lần/niên vụ.
"""

# =========================
# Từ điển khuyến nghị theo lớp
# =========================

RECOMMENDATIONS = {
    # Apple
    'Apple___Apple_scab': """\
**Táo – Đốm ghẻ (Apple scab – *Venturia inaequalis*)**
- Vệ sinh vườn: thu gom & tiêu hủy lá/quả rụng có bệnh.
- Tỉa tán thông thoáng, giảm ẩm lá.
- Phun phòng/điều trị giai đoạn nảy lộc → rụng cánh hoa → sau nở hoa:
  **mancozeb/chlorothalonil (FRAC M)**; luân phiên **difenoconazole/tebuconazole (FRAC 3)**,
  **myclobutanil (FRAC 3)**; kết hợp **QoI (FRAC 11)** nếu khuyến cáo địa phương cho phép.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Apple___Black_rot': """\
**Táo – Thối đen (*Botryosphaeria obtusa*)**
- Cắt bỏ cành/quả khô (mummy) mang ổ bệnh; tiêu hủy xa vườn. Khử trùng dụng cụ sau mỗi vết cắt.
- Phun bảo vệ quanh thời kỳ nhạy cảm (hoa–đậu quả):
  **mancozeb/captan (FRAC M)**; cân nhắc **thiophanate-methyl (FRAC 1)** theo nhãn.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Apple___Cedar_apple_rust': """\
**Táo – Rỉ sắt tuyết tùng (*Gymnosporangium* spp.)**
- Giảm nguồn bệnh: tránh trồng gần *Juniperus*; tỉa bỏ u sáp trên tuyết tùng sau mưa.
- Phun **myclobutanil/tebuconazole (FRAC 3)** giai đoạn nẩy lộc đến sau nở hoa; luân phiên nhóm khác nếu cần.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Apple___healthy': DEFAULT_HEALTHY,

    # Blueberry
    'Blueberry___healthy': DEFAULT_HEALTHY,

    # Cherry
    'Cherry_(including_sour)___Powdery_mildew': """\
**Anh đào – Phấn trắng (Powdery mildew)**
- Tỉa cành thông thoáng; tưới gốc, tránh ướt lá chiều tối.
- Phun: **lưu huỳnh (sulfur, FRAC M2)**, **kalium bicarbonate**, luân phiên **myclobutanil/quinoxyfen/DMI (FRAC 3)** theo nhãn.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Cherry_(including_sour)___healthy': DEFAULT_HEALTHY,

    # Corn (maize)
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': """\
**Ngô – Đốm lá xám (Gray Leaf Spot – *Cercospora* spp.)**
- Luân canh; vùi tàn dư sau thu hoạch; giống kháng khi có.
- Phun khi vượt ngưỡng (VT–R1): **QoI (FRAC 11)/DMI (FRAC 3)** như azoxystrobin, propiconazole
  theo khuyến cáo địa phương; tránh lặp nhóm.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Corn_(maize)___Common_rust_': """\
**Ngô – Rỉ sắt thông thường (*Puccinia sorghi*)**
- Giống kháng/ít nhiễm; theo dõi sớm trong điều kiện ẩm mát.
- Phun **DMI/QoI** theo nhãn khi mật độ/diện lá bệnh tăng nhanh; bảo vệ lá trên cùng trước và sau trỗ.
""" + IPM_BLOCK,

    'Corn_(maize)___Northern_Leaf_Blight': """\
**Ngô – Cháy lá Bắc (*Exserohilum turcicum*)**
- Luân canh, quản lý tàn dư; giống kháng.
- Phun **DMI/QoI** giai đoạn VT–R1 khi tỷ lệ lá bệnh vượt ngưỡng khu vực.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Corn_(maize)___healthy': DEFAULT_HEALTHY,

    # Grape
    'Grape___Black_rot': """\
**Nho – Thối đen (*Guignardia bidwellii*)**
- Thu gom “quả xác ướp”, lá bệnh; tỉa tán thông thoáng.
- Bảo vệ từ trước nở hoa đến sau đậu quả:
  **mancozeb/captan (FRAC M)**; luân phiên **DMI (FRAC 3)**/**QoI (FRAC 11)**.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Grape___Esca_(Black_Measles)': """\
**Nho – Esca / Black Measles (bệnh gỗ phức hợp)**
- Không có điều trị dứt điểm khi nặng. Cắt bỏ cành nặng/bị sọc; cân nhắc loại bỏ cây nghiêm trọng.
- Tránh cắt tỉa khi ẩm cao; khử trùng kéo/cưa; giảm stress (tưới–dinh dưỡng–nhiệt).
""" + IPM_BLOCK,

    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': """\
**Nho – Đốm cháy lá (Isariopsis)**
- Quản lý tàn dư; tán thông thoáng.
- Phun phòng: **mancozeb/đồng (FRAC M)**; luân phiên **QoI/DMI** theo nhãn vùng.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Grape___healthy': DEFAULT_HEALTHY,

    # Citrus
    'Orange___Haunglongbing_(Citrus_greening)': """\
**Cam – Vàng lá gân xanh (HLB/Greening)**
- **Chưa có thuốc chữa.** Tập trung **quản lý rầy chổng cánh**: dầu khoáng, abamectin, imidacloprid… (tuân thủ đăng ký địa phương).
- **Nhổ bỏ** cây nhiễm nặng để giảm nguồn bệnh; trồng cây **sạch bệnh**; quản lý cỏ dại ký chủ.
- Dinh dưỡng cân đối, bổ sung vi lượng để kéo dài năng suất cây nhiễm nhẹ.
""" + IPM_BLOCK,

    # Peach
    'Peach___Bacterial_spot': """\
**Đào – Đốm vi khuẩn (*Xanthomonas* spp.)**
- Giống ít nhiễm; tránh tưới phun mưa; vệ sinh tàn dư.
- Phun **đồng** (copper, FRAC M1) thời kỳ nhạy cảm; có thể phối **mancozeb** theo nhãn.
""" + IPM_BLOCK,

    'Peach___healthy': DEFAULT_HEALTHY,

    # Pepper (bell)
    'Pepper,_bell___Bacterial_spot': """\
**Ớt chuông – Đốm vi khuẩn**
- Cây giống sạch bệnh; xử lý hạt giống (nếu quy trình địa phương cho phép).
- Giảm ẩm lá kéo dài; tưới gốc.
- Phun **đồng (FRAC M1)** ± **mancozeb (FRAC M)**; quản lý bọ chích hút gây vết thương.
""" + IPM_BLOCK,

    'Pepper,_bell___healthy': DEFAULT_HEALTHY,

    # Potato
    'Potato___Early_blight': """\
**Khoai tây – Cháy lá sớm (*Alternaria* spp.)**
- Luân canh; bón cân đối, tránh dư đạm; loại bỏ lá già sát đất.
- Phun **chlorothalonil/mancozeb (FRAC M)**; luân phiên **difenoconazole (FRAC 3)**, kết hợp QoI khi cần.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Potato___Late_blight': """\
**Khoai tây – Cháy lá muộn (*Phytophthora infestans*)**
- Theo dõi dự báo dịch hại; giảm ẩm tán; che mưa (nếu có).
- Bảo vệ sớm bằng **mancozeb/chlorothalonil (FRAC M)**; khi bùng phát cân nhắc
  **cymoxanil (FRAC 27)**, **propamocarb (FRAC 28)**, **mandipropamid (FRAC 40)**,
  **metalaxyl-M/mefenoxam (FRAC 4)** theo nhãn và phác đồ kháng thuốc địa phương.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Potato___healthy': DEFAULT_HEALTHY,

    # Raspberry / Soybean
    'Raspberry___healthy': DEFAULT_HEALTHY,
    'Soybean___healthy': DEFAULT_HEALTHY,

    # Squash
    'Squash___Powdery_mildew': """\
**Bí – Phấn trắng**
- Giống kháng; thông thoáng tán; quản lý bón đạm hợp lý.
- Phun **lưu huỳnh (M2)**, **kalium bicarbonate**, luân phiên **DMI (FRAC 3)**/**QoI (FRAC 11)**/**SDHI (FRAC 7)** theo nhãn.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    # Strawberry
    'Strawberry___Leaf_scorch': """\
**Dâu tây – Cháy lá**
- Cắt bỏ lá bệnh; giảm ẩm; luân canh; tưới nhỏ giọt thay tưới phun.
- Phun phòng phù hợp (**mancozeb/đồng – FRAC M**), có thể luân phiên **DMI/QoI** nếu cần.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Strawberry___healthy': DEFAULT_HEALTHY,

    # Tomato
    'Tomato___Bacterial_spot': """\
**Cà chua – Đốm vi khuẩn (*Xanthomonas* spp.)**
- Cây con sạch bệnh; tránh ướt lá kéo dài; vệ sinh tàn dư; luân canh họ Cà.
- Phun **đồng (M1)**; có thể phối **mancozeb (M)** theo nhãn; quản lý côn trùng chích hút.
""" + IPM_BLOCK,

    'Tomato___Early_blight': """\
**Cà chua – Cháy lá sớm (*Alternaria* spp.)**
- Tỉa lá gốc; nâng giàn; tránh lá chạm đất; bón cân đối (không dư N).
- Phun **chlorothalonil/mancozeb (M)**; luân phiên **difenoconazole (3)**/**azoxystrobin (11)** theo nhãn.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Tomato___Late_blight': """\
**Cà chua – Cháy lá muộn (*Phytophthora infestans*)**
- Tránh ẩm lá; nhà màng tăng thông gió/che mưa; giám sát sát sao thời tiết ẩm mát.
- Bảo vệ sớm bằng **mancozeb/chlorothalonil (M)**; khi bùng phát dùng
  **cymoxanil (27)**, **propamocarb (28)**, **mandipropamid (40)**, **metalaxyl-M (4)** theo phác đồ địa phương.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Tomato___Leaf_Mold': """\
**Cà chua – Mốc lá (*Passalora fulva*)**
- Tăng thông gió nhà màng; giảm ẩm; loại bỏ lá bị nặng.
- Phun **chlorothalonil/copper (M)**; có thể dùng **difenoconazole (3)** theo nhãn.
""" + IPM_BLOCK,

    'Tomato___Septoria_leaf_spot': """\
**Cà chua – Đốm lá Septoria**
- Cắt bỏ lá bệnh sớm; tránh tưới phun mưa; khử trùng dụng cụ.
- Phun **chlorothalonil/mancozeb (M)**; luân phiên **DMI (3)**/**QoI (11)** nếu cần.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Tomato___Spider_mites Two-spotted_spider_mite': """\
**Cà chua–  Nhện đỏ hai chấm**
- Tăng ẩm không khí nhẹ; tắm lá nhẹ mặt dưới (không quá mức).
- Luân phiên **acaricide**: **abamectin (IRAC 6)**, **etoxazole (10B)**, **spiromesifen (23)**, **bifenazate (UN)** theo nhãn; tránh kháng chéo.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Tomato___Target_Spot': """\
**Cà chua – Đốm mục tiêu (*Corynespora cassiicola*)**
- Tỉa lá gốc, thông thoáng; loại bỏ lá bệnh; quản lý tàn dư.
- Phun **chlorothalonil/mancozeb (M)**; luân phiên **azoxystrobin (11)**/**difenoconazole (3)** theo nhãn.
""" + IPM_BLOCK + "\n" + RESISTANCE_NOTES,

    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': """\
**Cà chua – Vàng xoăn lá (TYLCV)**
- **Không có thuốc đặc trị.** Nhổ bỏ cây nhiễm nặng; vệ sinh vùng trồng.
- Quản lý **bọ phấn**: lưới chắn, bẫy dính, vệ sinh cỏ dại; hóa học theo nhãn (**imidacloprid – IRAC 4A**,
  **pyriproxyfen – IRAC 7C**, vv.).
- Dùng giống/ghép kháng nếu có; che phủ bạc hạn chế bọ phấn.
""" + IPM_BLOCK,

    'Tomato___Tomato_mosaic_virus': """\
**Cà chua – Virus khảm (ToMV/TMV)**
- Vệ sinh dụng cụ & tay; hạn chế chạm tay giữa các cây; xử lý hạt/khay theo quy trình cho phép.
- Sử dụng giống kháng; nhổ bỏ cây nhiễm nặng; khử trùng bề mặt sau canh tác.
""" + IPM_BLOCK,

    'Tomato___healthy': DEFAULT_HEALTHY,
}

# =========================
# Trả lời mặc định
# =========================

FALLBACK = """\
**Khuyến nghị chung**
- Xác định lại triệu chứng (mặt dưới lá, cuống, thân), theo dõi 2–3 ngày (chụp ảnh theo chu kỳ).
- Vệ sinh vườn, tỉa thoáng; luân canh và quản lý tàn dư.
- Cân đối dinh dưỡng; tránh dư đạm, hạn chế ẩm lá kéo dài.
- Nếu nghi nấm: cân nhắc **đồng/mancozeb/chlorothalonil** (đúng nhãn). Nghi vi khuẩn: **đồng**.
- Có côn trùng môi giới: phối hợp **biện pháp vật lý + sinh học + hóa học** theo khuyến cáo địa phương.
""" + "\n\n" + IPM_BLOCK + "\n\n" + SAFETY_MEDICAL


def get_recommendation(label: str) -> str:
    """
    Trả về khuyến nghị theo bệnh; tự động đính kèm khối An toàn & Y tế.
    """
    text = RECOMMENDATIONS.get(label, FALLBACK)
    # Đính kèm khối an toàn nếu chưa có
    if SAFETY_MEDICAL.strip() not in text:
        text = text.strip() + "\n\n" + SAFETY_MEDICAL
    return text

# =========================
# BẢNG TRA NHANH (Quick Reference)
# =========================

# Các cột: crop_disease, type, group, actives, timing, notes
QUICK_REF = [
    # Apple
    {"crop_disease":"Táo – Đốm ghẻ", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"mancozeb, chlorothalonil; difenoconazole/myclobutanil; azoxystrobin",
     "timing":"Nảy lộc → rụng cánh hoa → sau nở hoa",
     "notes":"Vệ sinh lá rụng; tán thoáng; luân phiên nhóm"},
    {"crop_disease":"Táo – Thối đen", "type":"Nấm", "group":"FRAC M / 1",
     "actives":"mancozeb, captan; thiophanate-methyl",
     "timing":"Trước–sau nở hoa, bảo vệ quả",
     "notes":"Cắt bỏ mummy; khử trùng kéo cắt"},
    {"crop_disease":"Táo – Rỉ sắt tuyết tùng", "type":"Nấm gỉ sắt", "group":"FRAC 3",
     "actives":"myclobutanil, tebuconazole",
     "timing":"Nảy lộc → sau nở hoa",
     "notes":"Tránh gần Juniperus; cắt u sáp tuyết tùng"},

    # Corn
    {"crop_disease":"Ngô – Đốm lá xám", "type":"Nấm", "group":"FRAC 3 / 11",
     "actives":"propiconazole; azoxystrobin (đơn/hỗn hợp)",
     "timing":"VT–R1 khi vượt ngưỡng",
     "notes":"Luân canh; vùi tàn dư; giống kháng"},
    {"crop_disease":"Ngô – Rỉ sắt thường", "type":"Nấm gỉ sắt", "group":"FRAC 3 / 11",
     "actives":"triazole; strobilurin",
     "timing":"Lá trên cùng trước/sau trỗ",
     "notes":"Giống kháng; theo dõi thời tiết ẩm mát"},
    {"crop_disease":"Ngô – Cháy lá Bắc", "type":"Nấm", "group":"FRAC 3 / 11",
     "actives":"DMI/QoI",
     "timing":"VT–R1 khi lá bệnh tăng nhanh",
     "notes":"Luân canh; tàn dư"},

    # Grape
    {"crop_disease":"Nho – Thối đen", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"mancozeb/captan; tebuconazole; azoxystrobin",
     "timing":"Trước nở hoa → đậu quả",
     "notes":"Nhặt quả xác ướp; tán thoáng"},
    {"crop_disease":"Nho – Esca/Black measles", "type":"Bệnh gỗ", "group":"—",
     "actives":"(không có trị dứt điểm)",
     "timing":"—",
     "notes":"Cắt bỏ cành nặng; tránh cắt khi ẩm; giảm stress"},
    {"crop_disease":"Nho – Đốm cháy lá (Isariopsis)", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"đồng/mancozeb; DMI/QoI",
     "timing":"Phòng từ sớm",
     "notes":"Tàn dư; thông thoáng"},

    # Citrus
    {"crop_disease":"Cam – HLB/Greening", "type":"Vi khuẩn (vectơ bọ chổng cánh)", "group":"IRAC 4A/7C…",
     "actives":"dầu khoáng, abamectin, imidacloprid, pyriproxyfen (theo nhãn)",
     "timing":"Quanh năm theo bọ chổng cánh",
     "notes":"Không thuốc chữa; cây sạch bệnh; nhổ bỏ cây nặng"},

    # Peach / Pepper
    {"crop_disease":"Đào – Đốm vi khuẩn", "type":"Vi khuẩn", "group":"FRAC M1 ± M",
     "actives":"đồng; + mancozeb (nếu nhãn cho phép)",
     "timing":"Thời kỳ mẫn cảm (ra lá, trước/sau nở hoa)",
     "notes":"Giống ít nhiễm; tránh tưới phun mưa"},
    {"crop_disease":"Ớt chuông – Đốm vi khuẩn", "type":"Vi khuẩn", "group":"FRAC M1 ± M",
     "actives":"đồng; + mancozeb",
     "timing":"Khi xuất hiện vết, mưa ẩm kéo dài",
     "notes":"Cây giống sạch bệnh; tưới gốc"},

    # Potato
    {"crop_disease":"Khoai tây – Cháy lá sớm", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"chlorothalonil/mancozeb; difenoconazole; azoxystrobin",
     "timing":"Bảo vệ sớm; luân phiên",
     "notes":"Tránh dư đạm; cắt lá già chạm đất"},
    {"crop_disease":"Khoai tây – Cháy lá muộn", "type":"Oomycete", "group":"FRAC M / 27 / 28 / 40 / 4",
     "actives":"mancozeb/chlorothalonil; cymoxanil; propamocarb; mandipropamid; metalaxyl-M",
     "timing":"Trước/bùng phát, theo dự báo dịch hại",
     "notes":"Giảm ẩm tán; che mưa nếu có"},

    # Squash / Strawberry
    {"crop_disease":"Bí – Phấn trắng", "type":"Nấm", "group":"FRAC M2 / 3 / 7 / 11",
     "actives":"lưu huỳnh; DMI; SDHI; QoI",
     "timing":"Ngay khi chớm bệnh",
     "notes":"Giống kháng; thoáng tán"},
    {"crop_disease":"Dâu tây – Cháy lá", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"mancozeb/đồng; DMI/QoI",
     "timing":"Phòng sớm, sau mưa",
     "notes":"Cắt lá bệnh; tưới nhỏ giọt"},

    # Tomato – fungal/bacterial/viral/mites
    {"crop_disease":"Cà chua – Đốm vi khuẩn", "type":"Vi khuẩn", "group":"FRAC M1 ± M",
     "actives":"đồng; + mancozeb",
     "timing":"Khi mới xuất hiện vết",
     "notes":"Vệ sinh tàn dư; quản lý chích hút"},
    {"crop_disease":"Cà chua – Cháy lá sớm", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"chlorothalonil/mancozeb; difenoconazole; azoxystrobin",
     "timing":"Bảo vệ sớm; luân phiên",
     "notes":"Tỉa lá gốc; nâng giàn"},
    {"crop_disease":"Cà chua – Cháy lá muộn", "type":"Oomycete", "group":"FRAC M / 27 / 28 / 40 / 4",
     "actives":"mancozeb/chlorothalonil; cymoxanil; propamocarb; mandipropamid; metalaxyl-M",
     "timing":"Trước/bùng phát, ẩm mát",
     "notes":"Thông gió/che mưa"},
    {"crop_disease":"Cà chua – Mốc lá", "type":"Nấm", "group":"FRAC M / 3",
     "actives":"chlorothalonil/copper; difenoconazole",
     "timing":"Ẩm cao trong nhà màng",
     "notes":"Tăng thông gió"},
    {"crop_disease":"Cà chua – Septoria", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"chlorothalonil/mancozeb; DMI/QoI",
     "timing":"Sau mưa, chớm vết",
     "notes":"Không tưới phun mưa"},
    {"crop_disease":"Cà chua – Nhện đỏ hai chấm", "type":"Nhện (mite)", "group":"IRAC 6 / 10B / 23 / UN",
     "actives":"abamectin; etoxazole; spiromesifen; bifenazate",
     "timing":"Khi thấy trứng/nhện non",
     "notes":"Luân phiên IRAC; tăng ẩm không khí nhẹ"},
    {"crop_disease":"Cà chua – Đốm mục tiêu", "type":"Nấm", "group":"FRAC M / 3 / 11",
     "actives":"chlorothalonil/mancozeb; difenoconazole; azoxystrobin",
     "timing":"Chớm bệnh, lá gốc",
     "notes":"Tỉa lá; xử lý tàn dư"},
    {"crop_disease":"Cà chua – TYLCV (vàng xoăn lá)", "type":"Virus (bọ phấn)", "group":"IRAC 4A / 7C …",
     "actives":"imidacloprid; pyriproxyfen; dầu khoáng (theo nhãn)",
     "timing":"Theo dõi bọ phấn",
     "notes":"Không thuốc đặc trị; giống/ghép kháng; lưới chắn"},
    {"crop_disease":"Cà chua – ToMV/TMV (khảm)", "type":"Virus (tiếp xúc)", "group":"—",
     "actives":"—",
     "timing":"—",
     "notes":"Vệ sinh tay/dụng cụ; giống kháng; nhổ cây nặng"},
]

def get_quick_ref_markdown() -> str:
    """
    Trả về Markdown bảng tra nhanh, gọn cho hiển thị trên Streamlit.
    Gợi ý: st.markdown(get_quick_ref_markdown())
    """
    headers = ["Cây/Bệnh", "Tác nhân", "Nhóm (FRAC/IRAC)", "Hoạt chất ví dụ", "Thời điểm", "Ghi chú"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"]*len(headers)) + " |"
    ]
    for row in QUICK_REF:
        lines.append("| {crop_disease} | {type} | {group} | {actives} | {timing} | {notes} |".format(**row))
    # Đính kèm nhắc An toàn & Y tế rút gọn
    lines.append("\n> **An toàn & Y tế**: PPE đầy đủ; tuân thủ **REI/PHI** trên nhãn; "
                 "không ăn/uống/hút thuốc khi pha–phun; sự cố liên hệ **115**.")
    return "\n".join(lines)
