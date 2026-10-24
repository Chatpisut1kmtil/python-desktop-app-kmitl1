import customtkinter as ctk
from tkinter import messagebox, filedialog
from config import DEFAULT_EXPENSE_CATEGORIES, DEFAULT_INCOME_CATEGORIES, THEME_COLORS
from components.modal_dialogs import TransactionModalDialog
from utils.exporter import ReportExporter

class TransactionsView(ctk.CTkFrame):
    def __init__(self, master, db_manager, on_refresh_needed=None):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager
        self.on_refresh_needed = on_refresh_needed

        self._setup_layout()
        self.refresh_data()

    def _setup_layout(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 10))

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="ประวัติรายการธุรกรรม (Transactions)",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        )
        title_lbl.pack(side="left")

        export_btn = ctk.CTkButton(
            header_frame,
            text="ส่งออกเป็นไฟล์ CSV",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0D9488",
            hover_color="#0F766E",
            command=self._export_csv,
            width=130
        )
        export_btn.pack(side="right")

        # แถบค้นหาและตัวกรอง
        filter_bar = ctk.CTkFrame(self, corner_radius=10)
        filter_bar.pack(fill="x", padx=24, pady=(0, 14))

        self.search_entry = ctk.CTkEntry(
            filter_bar,
            placeholder_text="ค้นหาโน้ต หรือ หมวดหมู่...",
            width=240
        )
        self.search_entry.pack(side="left", padx=12, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_data())

        self.type_filter = ctk.CTkOptionMenu(
            filter_bar,
            values=["ทั้งหมด", "รายรับ", "รายจ่าย"],
            command=lambda val: self.refresh_data(),
            width=110
        )
        self.type_filter.set("ทั้งหมด")
        self.type_filter.pack(side="left", padx=6, pady=10)

        reset_btn = ctk.CTkButton(
            filter_bar,
            text="ล้างตัวกรอง",
            fg_color="transparent",
            border_width=1,
            width=80,
            command=self._reset_filters
        )
        reset_btn.pack(side="right", padx=12, pady=10)

        # พื้นที่แสดงตารางรายการ
        list_container = ctk.CTkFrame(self, corner_radius=12)
        list_container.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        th_frame = ctk.CTkFrame(list_container, height=36, corner_radius=8, fg_color=("#E2E8F0", "#1E293B"))
        th_frame.pack(fill="x", padx=10, pady=(10, 4))

        ctk.CTkLabel(th_frame, text="วันที่", font=ctk.CTkFont(size=12, weight="bold"), width=100, anchor="w").pack(side="left", padx=(14, 10))
        ctk.CTkLabel(th_frame, text="หมวดหมู่ & บันทึก", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkLabel(th_frame, text="ช่องทางชำระ", font=ctk.CTkFont(size=12, weight="bold"), width=120, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(th_frame, text="จำนวนเงิน", font=ctk.CTkFont(size=12, weight="bold"), width=120, anchor="e").pack(side="left", padx=10)
        ctk.CTkLabel(th_frame, text="จัดการ", font=ctk.CTkFont(size=12, weight="bold"), width=110, anchor="center").pack(side="right", padx=14)

        self.scroll_frame = ctk.CTkScrollableFrame(list_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=(0, 10))

    def _reset_filters(self):
        self.search_entry.delete(0, "end")
        self.type_filter.set("ทั้งหมด")
        self.refresh_data()

    def refresh_data(self):
        search = self.search_entry.get().strip()
        type_selected = self.type_filter.get()

        db_type = None
        if type_selected == "รายรับ":
            db_type = "income"
        elif type_selected == "รายจ่าย":
            db_type = "expense"

        items = self.db.get_all_transactions(
            tx_type=db_type,
            search_keyword=search if search else None
        )

        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if not items:
            lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="ไม่พบข้อมูลรายการที่ตรงตามเงื่อนไข",
                text_color=THEME_COLORS["text_muted"],
                font=ctk.CTkFont(size=13)
            )
            lbl.pack(pady=40)
            return

        for tx in items:
            row = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
            row.pack(fill="x", pady=2, padx=4)

            is_inc = tx["type"] == "income"
            sign = "+" if is_inc else "-"
            amt_color = THEME_COLORS["success"] if is_inc else THEME_COLORS["danger"]

            ctk.CTkLabel(
                row,
                text=tx["date"],
                font=ctk.CTkFont(size=12),
                width=100,
                anchor="w"
            ).pack(side="left", padx=(14, 10), pady=8)

            note_str = f" - {tx['note']}" if tx["note"] else ""
            desc_text = f"{tx['category']}{note_str}"
            ctk.CTkLabel(
                row,
                text=desc_text,
                font=ctk.CTkFont(size=12, weight="bold" if is_inc else "normal"),
                anchor="w"
            ).pack(side="left", fill="x", expand=True, padx=10)

            ctk.CTkLabel(
                row,
                text=tx["payment_method"],
                font=ctk.CTkFont(size=11),
                text_color=THEME_COLORS["text_muted"],
                width=120,
                anchor="w"
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                row,
                text=f"{sign}฿{tx['amount']:,.2f}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=amt_color,
                width=120,
                anchor="e"
            ).pack(side="left", padx=10)

            btn_box = ctk.CTkFrame(row, fg_color="transparent", width=110)
            btn_box.pack(side="right", padx=10)

            edit_btn = ctk.CTkButton(
                btn_box,
                text="แก้ไข",
                width=45,
                height=28,
                fg_color="transparent",
                border_width=1,
                hover_color=("#CBD5E1", "#334155"),
                command=lambda item=tx: self._open_edit_dialog(item)
            )
            edit_btn.pack(side="left", padx=2)

            del_btn = ctk.CTkButton(
                btn_box,
                text="ลบ",
                width=45,
                height=28,
                fg_color="transparent",
                border_width=1,
                border_color=THEME_COLORS["danger"],
                hover_color=("#FEE2E2", "#7F1D1D"),
                text_color=THEME_COLORS["danger"],
                command=lambda tid=tx["id"]: self._delete_item(tid)
            )
            del_btn.pack(side="left", padx=2)

    def _open_edit_dialog(self, item):
        TransactionModalDialog(
            self,
            self.db,
            transaction_data=item,
            on_saved_callback=self._on_item_saved
        )

    def _delete_item(self, tx_id):
        if messagebox.askyesno("ยืนยัน", "ต้องการลบรายการนี้ใช่หรือไม่?"):
            self.db.delete_transaction(tx_id)
            self._on_item_saved()

    def _on_item_saved(self):
        self.refresh_data()
        if self.on_refresh_needed:
            self.on_refresh_needed()

    def _export_csv(self):
        items = self.db.get_all_transactions()
        if not items:
            messagebox.showinfo("แจ้งเตือน", "ยังไม่มีข้อมูลสำหรับส่งออก")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="FlowBudget_Report.csv"
        )
        if file_path:
            success, msg = ReportExporter.export_transactions_to_csv(items, file_path)
            if success:
                messagebox.showinfo("สำเร็จ", msg)
            else:
                messagebox.showerror("ข้อผิดพลาด", msg)
