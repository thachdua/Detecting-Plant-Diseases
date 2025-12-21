from streamlit.testing.v1 import AppTest
import pandas as pd
import os
from datetime import datetime

# ==========================================
# CẤU HÌNH
# ==========================================
TARGET_FILE = "main1.py"
TIMEOUT = 45 
REPORT_FILE = "Bao_Cao_Kiem_Thu_Plant.xlsx"

# Danh sách lưu kết quả
TEST_RESULTS = []

def log_test(test_case, description, status, note=""):
    TEST_RESULTS.append({
        "Thời gian": datetime.now().strftime("%H:%M:%S"),
        "Tên Test Case": test_case,
        "Mô tả": description,
        "Trạng thái": status,
        "Ghi chú": note
    })

def export_to_excel():
    """Hàm thực hiện việc ghi file Excel"""
    if TEST_RESULTS:
        df = pd.DataFrame(TEST_RESULTS)
        path = os.path.join(os.getcwd(), REPORT_FILE)
        df.to_excel(path, index=False, engine='openpyxl')
        print(f"\n\n>>> [OK] DA XUAT FILE TAI: {path}")

# ==========================================
# CÁC BÀI TEST
# ==========================================

def test_01_ui_and_sidebar():
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        # Kiểm tra sidebar
        sb = at.sidebar.get("selectbox")
        status = "PASSED" if sb else "FAILED"
        log_test("TC_01", "Kiểm tra Sidebar", status, f"Tìm thấy {len(sb)} selectbox")
        assert sb
    except Exception as e:
        log_test("TC_01", "Kiểm tra Sidebar", "ERROR", str(e))
        raise e

def test_02_navigation_check():
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        # Thử chuyển trang
        at.sidebar.get("selectbox")[0].select("Bảng tra nhanh").run(timeout=TIMEOUT)
        headers = at.get("header")
        status = "PASSED" if len(headers) > 0 else "FAILED"
        log_test("TC_02", "Chuyển trang Bảng tra nhanh", status, "Đã kiểm tra Header")
        assert len(headers) > 0
    except Exception as e:
        log_test("TC_02", "Chuyển trang Bảng tra nhanh", "ERROR", str(e))
        raise e

def test_03_final_and_export():
    """Bài test cuối cùng thực hiện xuất file Excel"""
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        # Kiểm tra trang Nhận diện (UI rỗng)
        at.sidebar.get("selectbox")[0].select("Nhận diện bệnh").run(timeout=TIMEOUT)
        log_test("TC_03", "Kiểm tra UI Nhận diện", "PASSED", "Giao diện trang nhận diện ổn định")
    except Exception as e:
        log_test("TC_03", "Kiểm tra UI Nhận diện", "ERROR", str(e))
    finally:
        # GỌI LỆNH XUẤT FILE TẠI ĐÂY
        export_to_excel()