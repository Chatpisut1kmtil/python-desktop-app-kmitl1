import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from config import DEFAULT_EXPENSE_CATEGORIES, DEFAULT_INCOME_CATEGORIES, PAYMENT_METHODS, THEME_COLORS

class TransactionModalDialog(ctk.CTkToplevel):
    def __init__(self, master, db_manager, transaction_data=None, on_saved_callback=None):
        super().__init__(master)
        self.db = db_manager
        self.tx_data = transaction_data
        self.on_saved = on_saved_callback

        is_edit = transaction_data is not None
        self.title("แก้ไขรายการ" if is_edit else "เพิ่มรายการใหม่")
        self.geometry("460x560")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self._build_form()

    def _build_form(self):
        container = ctk.CTkFrame(self, corner_radius=12)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        header_text = "แก้ไขรายการธุรกรรม" if self.tx_data else "บันทึกรายรับ - รายจ่าย"
        title_lbl = ctk.CTkLabel(
            container,
            text=header_text,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        )
        title_lbl.pack(pady=(10, 16))

        # เลือกประเภท (รายจ่าย / รายรับ)
        type_frame = ctk.CTkFrame(container, fg_color="transparent")
        type_frame.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(type_frame, text="ประเภทรายการ:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w")
        self.type_var = ctk.StringVar(value=self.tx_data["type"] if self.tx_data else "expense")
        self.type_segmented = ctk.CTkSegmentedButton(
            type_frame,
            values=["expense", "income"],
            variable=self.type_var,
            command=self._on_type_change
        )
        self.type_segmented.pack(fill="x", pady=(4, 0))

        # วันที่ (YYYY-MM-DD)
        date_frame = ctk.CTkFrame(container, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(date_frame, text="วันที่ (ปี-เดือน-วัน เช่น 2026-10-25):", font=ctk.CTkFont(size=12)).pack(anchor="w")
        default_date = self.tx_data["date"] if self.tx_data else datetime.now().strftime("%Y-%m-%d")
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="2026-10-25")
        self.date_entry.insert(0, default_date)
        self.date_entry.pack(fill="x", pady=(4, 0))

        # หมวดหมู่
        cat_frame = ctk.CTkFrame(container, fg_color="transparent")
        cat_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(cat_frame, text="หมวดหมู่:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        
        initial_cats = DEFAULT_EXPENSE_CATEGORIES if self.type_var.get() == "expense" else DEFAULT_INCOME_CATEGORIES
        self.cat_menu = ctk.CTkOptionMenu(cat_frame, values=initial_cats)
        if self.tx_data and self.tx_data["category"] in initial_cats:
            self.cat_menu.set(self.tx_data["category"])
        else:
            self.cat_menu.set(initial_cats[0])
        self.cat_menu.pack(fill="x", pady=(4, 0))

        # จำนวนเงิน
        amount_frame = ctk.CTkFrame(container, fg_color="transparent")
        amount_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(amount_frame, text="จำนวนเงิน (บาท):", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.amount_entry = ctk.CTkEntry(amount_frame, placeholder_text="0.00")
        if self.tx_data:
            self.amount_entry.insert(0, str(self.tx_data["amount"]))
        self.amount_entry.pack(fill="x", pady=(4, 0))

        # ช่องทางการชำระ
        pay_frame = ctk.CTkFrame(container, fg_color="transparent")
        pay_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(pay_frame, text="ช่องทางการชำระเงิน:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.pay_menu = ctk.CTkOptionMenu(pay_frame, values=PAYMENT_METHODS)
        if self.tx_data and self.tx_data["payment_method"] in PAYMENT_METHODS:
            self.pay_menu.set(self.tx_data["payment_method"])
        else:
            self.pay_menu.set(PAYMENT_METHODS[0])
        self.pay_menu.pack(fill="x", pady=(4, 0))

        # โน้ตบันทึกเพิ่มเติม
        note_frame = ctk.CTkFrame(container, fg_color="transparent")
        note_frame.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(note_frame, text="บันทึกช่วยจำ (ไม่บังคับ):", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.note_entry = ctk.CTkEntry(note_frame, placeholder_text="เช่น ข้าวกลางวัน, กาแฟ...")
        if self.tx_data and self.tx_data["note"]:
            self.note_entry.insert(0, self.tx_data["note"])
        self.note_entry.pack(fill="x", pady=(4, 0))

        # ปุ่มบันทึกและยกเลิก
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(20, 10))

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="ยกเลิก",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.destroy,
            width=100
        )
        cancel_btn.pack(side="left", padx=(0, 10))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="บันทึก",
            fg_color=THEME_COLORS["primary"],
            hover_color=THEME_COLORS["primary_hover"],
            command=self._handle_save,
            width=160
        )
        save_btn.pack(side="right")

    def _on_type_change(self, selected_type):
        cats = DEFAULT_EXPENSE_CATEGORIES if selected_type == "expense" else DEFAULT_INCOME_CATEGORIES
        self.cat_menu.configure(values=cats)
        self.cat_menu.set(cats[0])

    def _handle_save(self):
        # ตรวจสอบความถูกต้องของข้อมูล (Validation)
        date_val = self.date_entry.get().strip()
        try:
            datetime.strptime(date_val, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("แจ้งเตือน", "กรุณาระบุวันที่ในรูปแบบ YYYY-MM-DD เช่น 2026-10-25")
            return

        try:
            amount_val = float(self.amount_entry.get().strip())
            if amount_val <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("แจ้งเตือน", "กรุณากรอกจำนวนเงินเป็นตัวเลขที่มากกว่า 0")
            return

        category_val = self.cat_menu.get()
        type_val = self.type_var.get()
        payment_val = self.pay_menu.get()
        note_val = self.note_entry.get().strip()

        if self.tx_data:
            self.db.update_transaction(
                self.tx_data["id"], date_val, type_val, category_val, amount_val, payment_val, note_val
            )
        else:
            self.db.add_transaction(date_val, type_val, category_val, amount_val, payment_val, note_val)

        if self.on_saved:
            self.on_saved()

        self.destroy()
