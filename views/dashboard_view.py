import customtkinter as ctk
from datetime import datetime
from config import THEME_COLORS
from components.modal_dialogs import TransactionModalDialog

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db_manager, on_refresh_needed=None):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager
        self.on_refresh_needed = on_refresh_needed

        self._setup_layout()
        self.refresh_data()

    def _setup_layout(self):
        # ส่วนหัวด้านบน
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 14))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        self.greeting_lbl = ctk.CTkLabel(
            title_box,
            text="ภาพรวมการเงิน (Dashboard)",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        )
        self.greeting_lbl.pack(anchor="w")

        now_str = datetime.now().strftime("%B %Y")
        self.date_sub_lbl = ctk.CTkLabel(
            title_box,
            text=f"ประจำเดือน: {now_str}",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=THEME_COLORS["text_muted"]
        )
        self.date_sub_lbl.pack(anchor="w")

        add_btn = ctk.CTkButton(
            header_frame,
            text="+ บันทึกรายการใหม่",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            height=38,
            corner_radius=8,
            command=self._open_add_modal
        )
        add_btn.pack(side="right")

        # การ์ดสรุปตัวเลขสถิติ 4 ใบ
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=24, pady=(0, 16))
        for col in range(4):
            self.cards_frame.grid_columnconfigure(col, weight=1)

        self.card_balance = self._create_metric_card(
            self.cards_frame, 0, "ยอดเงินคงเหลือรวม", "฿0.00", THEME_COLORS["primary"]
        )
        self.card_income = self._create_metric_card(
            self.cards_frame, 1, "รายรับเดือนนี้", "฿0.00", THEME_COLORS["success"]
        )
        self.card_expense = self._create_metric_card(
            self.cards_frame, 2, "รายจ่ายเดือนนี้", "฿0.00", THEME_COLORS["danger"]
        )
        self.card_savings = self._create_metric_card(
            self.cards_frame, 3, "อัตราการออม", "0.0%", THEME_COLORS["warning"]
        )

        # รายการธุรกรรมล่าสุด
        content_frame = ctk.CTkFrame(self, corner_radius=12)
        content_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        content_header = ctk.CTkFrame(content_frame, fg_color="transparent")
        content_header.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            content_header,
            text="รายการล่าสุด (Recent Transactions)",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        ).pack(side="left")

        self.recent_scroll = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
        self.recent_scroll.pack(fill="both", expand=True, padx=14, pady=(0, 12))

    def _create_metric_card(self, parent, col, title, initial_val, accent_color):
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")

        title_lbl = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=THEME_COLORS["text_muted"]
        )
        title_lbl.pack(anchor="w", padx=14, pady=(12, 2))

        val_lbl = ctk.CTkLabel(
            card,
            text=initial_val,
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=accent_color
        )
        val_lbl.pack(anchor="w", padx=14, pady=(0, 12))
        return val_lbl

    def _open_add_modal(self):
        TransactionModalDialog(self, self.db, on_saved_callback=self._on_item_saved)

    def _on_item_saved(self):
        self.refresh_data()
        if self.on_refresh_needed:
            self.on_refresh_needed()

    def refresh_data(self):
        summary = self.db.get_financial_summary()

        self.card_balance.configure(text=f"฿{summary['all_time_balance']:,.2f}")
        self.card_income.configure(text=f"+฿{summary['month_income']:,.2f}")
        self.card_expense.configure(text=f"-฿{summary['month_expense']:,.2f}")
        self.card_savings.configure(text=f"{summary['savings_rate']:.1f}%")

        for widget in self.recent_scroll.winfo_children():
            widget.destroy()

        recent_items = self.db.get_all_transactions(limit=6)

        if not recent_items:
            empty_lbl = ctk.CTkLabel(
                self.recent_scroll,
                text="ยังไม่มีข้อมูลรายการ กดปุ่ม '+ บันทึกรายการใหม่' ด้านบนเพื่อเริ่มต้น",
                text_color=THEME_COLORS["text_muted"],
                font=ctk.CTkFont(family="Segoe UI", size=13)
            )
            empty_lbl.pack(pady=30)
            return

        for item in recent_items:
            row_frame = ctk.CTkFrame(self.recent_scroll, corner_radius=8)
            row_frame.pack(fill="x", pady=3, padx=2)

            is_inc = item["type"] == "income"
            sign = "+" if is_inc else "-"
            amt_color = THEME_COLORS["success"] if is_inc else THEME_COLORS["danger"]

            left_box = ctk.CTkFrame(row_frame, fg_color="transparent")
            left_box.pack(side="left", padx=12, pady=8)

            cat_lbl = ctk.CTkLabel(
                left_box,
                text=f"{item['category']}",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
            )
            cat_lbl.pack(anchor="w")

            note_detail = f"{item['date']} • {item['payment_method']}"
            if item["note"]:
                note_detail += f" ({item['note']})"

            sub_lbl = ctk.CTkLabel(
                left_box,
                text=note_detail,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=THEME_COLORS["text_muted"]
            )
            sub_lbl.pack(anchor="w")

            amt_lbl = ctk.CTkLabel(
                row_frame,
                text=f"{sign}฿{item['amount']:,.2f}",
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                text_color=amt_color
            )
            amt_lbl.pack(side="right", padx=14)
