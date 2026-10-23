import customtkinter as ctk
from config import APP_NAME, APP_SUBTITLE, THEME_COLORS

class SidebarNavigation(ctk.CTkFrame):
    def __init__(self, master, on_navigate_callback):
        super().__init__(master, width=220, corner_radius=0)
        self.on_navigate = on_navigate_callback
        self.nav_buttons = {}
        self.active_tab = "dashboard"

        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(6, weight=1)

        # ส่วนหัวชื่อโปรแกรม
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.grid(row=0, column=0, padx=20, pady=(24, 20), sticky="ew")

        title_label = ctk.CTkLabel(
            brand_frame,
            text=APP_NAME,
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#38BDF8"
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            brand_frame,
            text=APP_SUBTITLE,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=THEME_COLORS["text_muted"]
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # รายการเมนูด้านข้าง
        items = [
            ("dashboard", "ภาพรวม (Dashboard)"),
            ("transactions", "ธุรกรรมทั้งหมด (Transactions)"),
            ("analytics", "กราฟวิเคราะห์ (Analytics)"),
            ("budget", "วางแผนงบประมาณ (Budget)")
        ]

        for idx, (key, text) in enumerate(items, start=1):
            btn = ctk.CTkButton(
                self,
                text=text,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=("#334155", "#E2E8F0"),
                hover_color=("#E2E8F0", "#334155"),
                command=lambda k=key: self._on_btn_click(k)
            )
            btn.grid(row=idx, column=0, padx=14, pady=4, sticky="ew")
            self.nav_buttons[key] = btn

        # สวิตช์สลับโหมดสี
        self.theme_switch = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            command=self._toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.select()
        self.theme_switch.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        self.set_active("dashboard")

    def _on_btn_click(self, key):
        self.set_active(key)
        if self.on_navigate:
            self.on_navigate(key)

    def set_active(self, key):
        self.active_tab = key
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(
                    fg_color=THEME_COLORS["primary"],
                    text_color="#FFFFFF",
                    hover_color=THEME_COLORS["primary_hover"]
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("#334155", "#E2E8F0"),
                    hover_color=("#E2E8F0", "#334155")
                )

    def _toggle_theme(self):
        mode = "dark" if self.theme_switch.get() == "dark" else "light"
        ctk.set_appearance_mode(mode)
