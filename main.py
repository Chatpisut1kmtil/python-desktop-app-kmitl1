import customtkinter as ctk
import os
from config import APP_NAME, WINDOW_SIZE, MIN_WINDOW_SIZE
from database.db_manager import DatabaseManager
from components.nav_bar import SidebarNavigation
from views.dashboard_view import DashboardView
from views.transactions_view import TransactionsView
from views.analytics_view import AnalyticsView
from views.budget_view import BudgetView

class FlowBudgetApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ตั้งค่าธีมเริ่มต้น
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # ตั้งค่าขนาดหน้าต่างโปรแกรม
        self.title(f"{APP_NAME} - Personal Finance Tracker")
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)

        # เชื่อมต่อฐานข้อมูล
        self.db = DatabaseManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # แถบเมนูด้านข้าง
        self.sidebar = SidebarNavigation(self, on_navigate_callback=self._switch_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # คอนเทนเนอร์สำหรับสลับหน้าจอ
        self.views_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.views_container.grid(row=0, column=1, sticky="nsew")
        self.views_container.grid_rowconfigure(0, weight=1)
        self.views_container.grid_columnconfigure(0, weight=1)

        # โหลดหน้าจอแต่ละแท็บ
        self.views = {
            "dashboard": DashboardView(self.views_container, self.db, on_refresh_needed=self._on_global_data_change),
            "transactions": TransactionsView(self.views_container, self.db, on_refresh_needed=self._on_global_data_change),
            "analytics": AnalyticsView(self.views_container, self.db),
            "budget": BudgetView(self.views_container, self.db)
        }

        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        # หน้าแรกให้เปิดที่ Dashboard
        self._switch_view("dashboard")

    def _switch_view(self, view_key):
        target_view = self.views.get(view_key)
        if target_view:
            target_view.tkraise()
            if hasattr(target_view, "refresh_data"):
                target_view.refresh_data()

    def _on_global_data_change(self):
        # เมื่อมีการเพิ่ม ลบ หรือแก้ไขข้อมูล ให้สั่งรีเฟรชทุกหน้าจอ
        for view in self.views.values():
            if hasattr(view, "refresh_data"):
                view.refresh_data()

if __name__ == "__main__":
    app = FlowBudgetApplication()
    app.mainloop()
