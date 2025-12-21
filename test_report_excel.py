import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import os
from datetime import datetime

# ==========================================
# CẤU HÌNH
# ==========================================
TARGET_FILE = "main1.py"
TIMEOUT = 45 
REPORT_FILE = "Ket_Qua_Test_Final.xlsx"

# Danh sách toàn cục lưu kết quả
TEST_RESULTS = []

def log_result(test_name, status, note=""):
    """Hàm lưu kết quả vào danh sách"""
    TEST_RESULTS.append({
        "Thời gian": datetime.now().strftime("%H:%M:%S"),
        "Tên Test Case": test_name,
        "Trạng thái": status,
        "Ghi chú": note
    })

@pytest.fixture(scope="session", autouse=True)
def export_excel_after_all_tests():
    """Tự động xuất Excel sau khi chạy xong tất cả"""
    yield # Đợi test chạy xong...
    
    print("\n\n-----------------------------------")
    print(">>> ĐANG TẠO FILE BÁO CÁO EXCEL...")
    
    if not TEST_RESULTS:
        log_result("System Check", "SKIPPED", "Không có dữ liệu test")

    try:
        df = pd.DataFrame(TEST_RESULTS)
        file_path = os.path.join(os.getcwd(), REPORT_FILE)
        df.to_excel(file_path, index=False, engine='openpyxl')
        print(f">>> [THÀNH CÔNG] File đã lưu tại: {file_path}")
        print("-----------------------------------\n")
    except Exception as e:
        print(f">>> [LỖI] Không thể ghi file Excel: {e}")

# ==========================================
# CÁC BÀI TEST (ĐÃ SỬA LỖI SIDEBAR)
# ==========================================

def test_01_check_sidebar():
    """Kiểm tra Sidebar (Sửa lỗi: dùng .get để an toàn)"""
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        
        # SỬA LỖI Ở ĐÂY: Dùng .get("selectbox") thay vì .selectbox trực tiếp
        sb_list = at.sidebar.get("selectbox")
        
        if sb_list:
            log_result("TC_01: Sidebar UI", "PASSED", f"Tìm thấy Menu (Có {len(sb_list[0].options)} trang)")
        else:
            # Nếu không tìm thấy, thử đợi thêm một chút hoặc kiểm tra lại
            log_result("TC_01: Sidebar UI", "FAILED", "Không tìm thấy widget Selectbox trong Sidebar")
            pytest.fail("Mất Sidebar")
            
    except Exception as e:
        log_result("TC_01: Sidebar UI", "ERROR", str(e))
        raise e

def test_02_check_gallery_page():
    """Kiểm tra trang Bộ sưu tập"""
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        
        # Dùng .get an toàn
        sb_list = at.sidebar.get("selectbox")
        if sb_list:
            sb_list[0].select("Bộ sưu tập").run(timeout=TIMEOUT)
            
            # Kiểm tra tiêu đề
            headers = at.get("header")
            found = any("Bộ sưu tập" in h.value for h in headers)
            
            if found:
                log_result("TC_02: Trang Bộ Sưu Tập", "PASSED", "Chuyển trang thành công, hiển thị đúng Header")
            else:
                log_result("TC_02: Trang Bộ Sưu Tập", "FAILED", "Đã chuyển trang nhưng không thấy Header")
                pytest.fail("Lỗi hiển thị trang")
        else:
             pytest.fail("Không thể chuyển trang vì mất Sidebar")

    except Exception as e:
        log_result("TC_02: Trang Bộ Sưu Tập", "ERROR", str(e))

def test_03_check_home_features():
    """Kiểm tra trang chủ"""
    try:
        at = AppTest.from_file(TARGET_FILE).run(timeout=TIMEOUT)
        
        # Dùng .get an toàn
        markdowns = at.get("markdown")
        found = any("Tính năng nổi bật" in m.value for m in markdowns)
        
        if found:
            log_result("TC_03: Trang Chủ", "PASSED", "Hiển thị đầy đủ phần Tính năng nổi bật")
        else:
            log_result("TC_03: Trang Chủ", "FAILED", "Thiếu nội dung trang chủ")
            
    except Exception as e:
        log_result("TC_03: Trang Chủ", "ERROR", str(e))