import os
from pathlib import Path

# ตำแหน่งไฟล์และฐานข้อมูล
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = os.path.join(BASE_DIR, "finance_data.db")

APP_NAME = "FlowBudget"
APP_SUBTITLE = "Personal Finance Tracker"
WINDOW_SIZE = "1180x720"
MIN_WINDOW_SIZE = (1000, 640)

# หมวดหมู่เริ่มต้นสำหรับรายจ่าย
DEFAULT_EXPENSE_CATEGORIES = [
    "อาหาร & เครื่องดื่ม",
    "การเดินทาง",
    "ค่าที่พัก & สาธารณูปโภค",
    "ช้อปปิ้ง & ไลฟ์สไตล์",
    "ความบันเทิง",
    "สุขภาพ & การแพทย์",
    "การศึกษา",
    "อื่นๆ"
]

# หมวดหมู่สำหรับรายรับ
DEFAULT_INCOME_CATEGORIES = [
    "เงินเดือน",
    "งานเสริม (Freelance)",
    "การลงทุน & เงินปันผล",
    "ของขวัญ / โบนัส",
    "รายรับอื่นๆ"
]

# วิธีการชำระเงิน
PAYMENT_METHODS = ["เงินสด", "โอนเงิน / QR Code", "บัตรเครดิต", "E-Wallet"]

# โค้ดสีหลักที่ใช้ในแอป
THEME_COLORS = {
    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
    "card_dark": "#1E293B",
    "card_light": "#FFFFFF",
    "bg_dark": "#0F172A",
    "bg_light": "#F8FAFC",
    "text_muted": "#94A3B8"
}
