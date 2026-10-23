import sqlite3
from datetime import datetime
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        # เปิดการเชื่อมต่อ SQLite และเปิดการใช้งาน Foreign Key
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        # สร้างตารางข้อมูลถ้ายังไม่มีในระบบ
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ตารางบันทึกธุรกรรม รายรับ-รายจ่าย
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    payment_method TEXT DEFAULT 'เงินสด',
                    note TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # ตารางเก็บเพดานงบประมาณรายเดือน
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE NOT NULL,
                    monthly_limit REAL NOT NULL CHECK(monthly_limit >= 0),
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # ตั้งค่างบเริ่มต้นให้ถ้ายังไม่มีข้อมูล
            cursor.execute("SELECT COUNT(*) FROM budgets")
            if cursor.fetchone()[0] == 0:
                default_budgets = [
                    ("อาหาร & เครื่องดื่ม", 6000.0),
                    ("การเดินทาง", 3000.0),
                    ("ค่าที่พัก & สาธารณูปโภค", 8000.0),
                    ("ช้อปปิ้ง & ไลฟ์สไตล์", 2500.0),
                    ("ความบันเทิง", 1500.0)
                ]
                cursor.executemany("""
                    INSERT OR IGNORE INTO budgets (category, monthly_limit)
                    VALUES (?, ?)
                """, default_budgets)

            conn.commit()

    # --- ฟังก์ชันจัดการข้อมูล (CRUD) ---

    def add_transaction(self, tx_date, tx_type, category, amount, payment_method="เงินสด", note=""):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (date, type, category, amount, payment_method, note)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tx_date, tx_type, category, float(amount), payment_method, note.strip()))
            conn.commit()
            return cursor.lastrowid

    def update_transaction(self, tx_id, tx_date, tx_type, category, amount, payment_method, note):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET date = ?, type = ?, category = ?, amount = ?, payment_method = ?, note = ?
                WHERE id = ?
            """, (tx_date, tx_type, category, float(amount), payment_method, note.strip(), tx_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_transaction(self, tx_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_transactions(self, limit=None, tx_type=None, category=None, search_keyword=None):
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if tx_type and tx_type != "ทั้งหมด":
            query += " AND type = ?"
            params.append(tx_type)

        if category and category != "ทุกหมวดหมู่":
            query += " AND category = ?"
            params.append(category)

        if search_keyword:
            query += " AND (note LIKE ? OR category LIKE ?)"
            params.extend([f"%{search_keyword}%", f"%{search_keyword}%"])

        query += " ORDER BY date DESC, id DESC"

        if limit:
            query += f" LIMIT {int(limit)}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    # --- ฟังก์ชันคำนวณและสรุปยอดเงิน ---

    def get_financial_summary(self, month=None, year=None):
        now = datetime.now()
        target_year = str(year) if year else now.strftime("%Y")
        target_month = f"{int(month):02d}" if month else now.strftime("%m")
        prefix = f"{target_year}-{target_month}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # รวมรายรับเดือนนี้
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0.0) FROM transactions
                WHERE type = 'income' AND date LIKE ?
            """, (f"{prefix}%",))
            total_income = cursor.fetchone()[0]

            # รวมรายจ่ายเดือนนี้
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0.0) FROM transactions
                WHERE type = 'expense' AND date LIKE ?
            """, (f"{prefix}%",))
            total_expense = cursor.fetchone()[0]

            # รวมยอดเงินคงเหลือสะสมทั้งหมด
            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM transactions WHERE type = 'income'")
            all_time_income = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM transactions WHERE type = 'expense'")
            all_time_expense = cursor.fetchone()[0]

            current_balance = all_time_income - all_time_expense
            
            # คำนวณอัตราการออม (%)
            savings_rate = 0.0
            if total_income > 0:
                savings_rate = ((total_income - total_expense) / total_income) * 100

            return {
                "month_income": total_income,
                "month_expense": total_expense,
                "month_net": total_income - total_expense,
                "all_time_balance": current_balance,
                "savings_rate": max(savings_rate, 0.0)
            }

    def get_category_breakdown(self, tx_type="expense", month=None, year=None):
        # รวมรายจ่ายแยกตามหมวดหมู่ สำหรับทำกราฟ Donut
        now = datetime.now()
        target_year = str(year) if year else now.strftime("%Y")
        target_month = f"{int(month):02d}" if month else now.strftime("%m")
        prefix = f"{target_year}-{target_month}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category, SUM(amount) as total_amount
                FROM transactions
                WHERE type = ? AND date LIKE ?
                GROUP BY category
                ORDER BY total_amount DESC
            """, (tx_type, f"{prefix}%"))
            return [dict(row) for row in cursor.fetchall()]

    def get_monthly_trend(self, months_count=5):
        # ดึงยอดรายรับ-รายจ่ายย้อนหลังแยกรายเดือน สำหรับทำ Bar Chart
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT strftime('%Y-%m', date) as month_str,
                       SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income_total,
                       SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense_total
                FROM transactions
                GROUP BY month_str
                ORDER BY month_str DESC
                LIMIT ?
            """, (months_count,))
            rows = cursor.fetchall()
            return [dict(r) for r in reversed(rows)]

    # --- ฟังก์ชันจัดการงบประมาณ (Budget) ---

    def get_all_budgets_with_usage(self, month=None, year=None):
        now = datetime.now()
        target_year = str(year) if year else now.strftime("%Y")
        target_month = f"{int(month):02d}" if month else now.strftime("%m")
        prefix = f"{target_year}-{target_month}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.category, b.monthly_limit,
                       COALESCE(SUM(t.amount), 0.0) as spent
                FROM budgets b
                LEFT JOIN transactions t 
                    ON b.category = t.category 
                    AND t.type = 'expense' 
                    AND t.date LIKE ?
                GROUP BY b.category, b.monthly_limit
                ORDER BY b.monthly_limit DESC
            """, (f"{prefix}%",))
            return [dict(row) for row in cursor.fetchall()]

    def set_budget_limit(self, category, limit_amount):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO budgets (category, monthly_limit)
                VALUES (?, ?)
                ON CONFLICT(category) DO UPDATE SET
                    monthly_limit = excluded.monthly_limit,
                    updated_at = CURRENT_TIMESTAMP
            """, (category, float(limit_amount)))
            conn.commit()
