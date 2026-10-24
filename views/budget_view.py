import customtkinter as ctk
from tkinter import messagebox
from config import THEME_COLORS, DEFAULT_EXPENSE_CATEGORIES

class BudgetView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager

        self._setup_layout()
        self.refresh_data()

    def _setup_layout(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 14))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        ctk.CTkLabel(
            title_box,
            text="วางแผนงบประมาณ (Budget Management)",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="กำหนดเพดานค่าใช้จ่ายรายหมวดหมู่เพื่อควบคุมวินัยการเงิน",
            font=ctk.CTkFont(size=12),
            text_color=THEME_COLORS["text_muted"]
        ).pack(anchor="w")

        set_btn = ctk.CTkButton(
            header_frame,
            text="ปรับตั้งค่างบประมาณ",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            command=self._open_budget_settings_modal
        )
        set_btn.pack(side="right")

        container = ctk.CTkFrame(self, corner_radius=12)
        container.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.scroll_frame = ctk.CTkScrollableFrame(container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=14, pady=14)

    def refresh_data(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        budgets = self.db.get_all_budgets_with_usage()

        if not budgets:
            ctk.CTkLabel(
                self.scroll_frame,
                text="ยังไม่มีการตั้งค่างบประมาณ กดปุ่ม 'ปรับตั้งค่างบประมาณ' เพื่อเริ่มต้น",
                text_color=THEME_COLORS["text_muted"]
            ).pack(pady=40)
            return

        for item in budgets:
            category = item["category"]
            limit = item["monthly_limit"]
            spent = item["spent"]

            ratio = (spent / limit) if limit > 0 else 0
            ratio_clamped = min(max(ratio, 0.0), 1.0)
            percentage = ratio * 100

            # ประเมินสถานะการใช้เงิน (สีเขียว / เหลือง / แดง)
            if percentage >= 100:
                status_color = THEME_COLORS["danger"]
                status_text = f"ใช้เกินงบแล้ว ({percentage:.1f}%)"
            elif percentage >= 75:
                status_color = THEME_COLORS["warning"]
                status_text = f"ใกล้เต็มงบ ({percentage:.1f}%)"
            else:
                status_color = THEME_COLORS["success"]
                status_text = f"ปกติ ({percentage:.1f}%)"

            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            card.pack(fill="x", pady=6, padx=4)

            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=16, pady=(12, 6))

            ctk.CTkLabel(
                top_row,
                text=category,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left")

            ctk.CTkLabel(
                top_row,
                text=status_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=status_color
            ).pack(side="right")

            pbar = ctk.CTkProgressBar(card, height=12, corner_radius=6)
            pbar.pack(fill="x", padx=16, pady=4)
            pbar.set(ratio_clamped)
            pbar.configure(progress_color=status_color)

            btm_row = ctk.CTkFrame(card, fg_color="transparent")
            btm_row.pack(fill="x", padx=16, pady=(4, 12))

            ctk.CTkLabel(
                btm_row,
                text=f"ใช้ไปแล้ว: ฿{spent:,.2f}",
                font=ctk.CTkFont(size=12),
                text_color=THEME_COLORS["text_muted"]
            ).pack(side="left")

            remaining = limit - spent
            rem_text = f"เหลืองบ: ฿{remaining:,.2f}" if remaining >= 0 else f"เกินงบ: ฿{abs(remaining):,.2f}"
            ctk.CTkLabel(
                btm_row,
                text=f"งบที่ตั้งไว้: ฿{limit:,.2f}  |  {rem_text}",
                font=ctk.CTkFont(size=12)
            ).pack(side="right")

    def _open_budget_settings_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("ตั้งค่างบประมาณ")
        modal.geometry("400x320")
        modal.resizable(False, False)
        modal.transient(self)
        modal.grab_set()

        container = ctk.CTkFrame(modal, corner_radius=10)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container,
            text="กำหนดเพดานงบประมาณรายเดือน",
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(pady=(6, 14))

        ctk.CTkLabel(container, text="เลือกหมวดหมู่:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        cat_menu = ctk.CTkOptionMenu(container, values=DEFAULT_EXPENSE_CATEGORIES)
        cat_menu.pack(fill="x", padx=10, pady=(2, 10))

        ctk.CTkLabel(container, text="วงเงินงบประมาณสูงสุด (บาท):", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)
        amt_entry = ctk.CTkEntry(container, placeholder_text="เช่น 5000")
        amt_entry.pack(fill="x", padx=10, pady=(2, 16))

        def save_budget():
            try:
                val = float(amt_entry.get().strip())
                if val <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงินเป็นตัวเลขที่มากกว่า 0")
                return

            self.db.set_budget_limit(cat_menu.get(), val)
            self.refresh_data()
            modal.destroy()

        ctk.CTkButton(
            container,
            text="บันทึก",
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            command=save_budget
        ).pack(fill="x", padx=10, pady=4)
