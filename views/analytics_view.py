import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")

# Set Thai font support for Windows Matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'Segoe UI', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import THEME_COLORS

class AnalyticsView(ctk.CTkFrame):
    """Visual financial analytics with embedded Matplotlib interactive charts."""

    def __init__(self, master, db_manager):
        super().__init__(master, fg_color="transparent")
        self.db = db_manager

        self._setup_layout()
        self.refresh_data()

    def _setup_layout(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 14))

        ctk.CTkLabel(
            header_frame,
            text="📈 สถิติและการวิเคราะห์เชิงลึก (Financial Analytics)",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        ).pack(side="left")

        # Top Highlights Banner
        self.highlight_frame = ctk.CTkFrame(self, corner_radius=10)
        self.highlight_frame.pack(fill="x", padx=24, pady=(0, 14))

        self.top_cat_lbl = ctk.CTkLabel(
            self.highlight_frame,
            text="🔥 หมวดหมู่ที่จ่ายมากที่สุด: กำลังประมวลผล...",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.top_cat_lbl.pack(side="left", padx=16, pady=12)

        # Charts Container (Split 2 Columns)
        self.charts_container = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_container.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.charts_container.grid_columnconfigure(0, weight=1)
        self.charts_container.grid_columnconfigure(1, weight=1)
        self.charts_container.grid_rowconfigure(0, weight=1)

        # Chart Box 1 (Pie Breakdown)
        self.box_pie = ctk.CTkFrame(self.charts_container, corner_radius=12)
        self.box_pie.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            self.box_pie,
            text="สัดส่วนค่าใช้จ่ายเดือนนี้ (Expense Distribution)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(12, 6))

        self.pie_canvas_holder = ctk.CTkFrame(self.box_pie, fg_color="transparent")
        self.pie_canvas_holder.pack(fill="both", expand=True, padx=10, pady=10)

        # Chart Box 2 (Bar Trend)
        self.box_trend = ctk.CTkFrame(self.charts_container, corner_radius=12)
        self.box_trend.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        ctk.CTkLabel(
            self.box_trend,
            text="แนวโน้มรายรับ vs รายจ่าย (Monthly Trend)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(12, 6))

        self.trend_canvas_holder = ctk.CTkFrame(self.box_trend, fg_color="transparent")
        self.trend_canvas_holder.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_data(self):
        """Redraws both charts with newest database data."""
        breakdown = self.db.get_category_breakdown(tx_type="expense")
        trend_data = self.db.get_monthly_trend(months_count=5)

        # Update Top Category banner
        if breakdown and len(breakdown) > 0 and breakdown[0]["total_amount"] > 0:
            top_item = breakdown[0]
            self.top_cat_lbl.configure(
                text=f"🔥 หมวดหมู่ที่จ่ายมากที่สุดเดือนนี้: {top_item['category']} (฿{top_item['total_amount']:,.2f})"
            )
        else:
            self.top_cat_lbl.configure(text="💡 เริ่มต้นจาก 0: ยังไม่มีข้อมูลรายการ เริ่มบันทึกเพื่อดูการวิเคราะห์")

        self._render_pie_chart(breakdown)
        self._render_trend_chart(trend_data)

    def _render_pie_chart(self, breakdown):
        for w in self.pie_canvas_holder.winfo_children():
            w.destroy()

        fig = Figure(figsize=(4.5, 3.8), dpi=90)
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_hex = "#1E293B" if is_dark else "#FFFFFF"
        text_color = "#E2E8F0" if is_dark else "#334155"

        fig.patch.set_facecolor(bg_hex)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_hex)

        valid_breakdown = [b for b in breakdown if b.get("total_amount", 0) > 0]

        if not valid_breakdown:
            ax.text(0.5, 0.5, "ยังไม่มีข้อมูลรายจ่าย\n(กดบันทึกรายการใหม่เพื่อเริ่ม)", 
                    ha="center", va="center", color=text_color, fontsize=12, fontfamily="Leelawadee UI")
            ax.axis("off")
        else:
            labels = [b["category"] for b in valid_breakdown]
            values = [b["total_amount"] for b in valid_breakdown]
            palette = ["#38BDF8", "#F43F5E", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#64748B"]

            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140,
                colors=palette[:len(values)],
                wedgeprops=dict(width=0.45, edgecolor=bg_hex),
                textprops=dict(color=text_color, fontsize=9, fontfamily="Leelawadee UI")
            )
            for autotext in autotexts:
                autotext.set_color("#FFFFFF")
                autotext.set_fontsize(8)

        canvas = FigureCanvasTkAgg(fig, master=self.pie_canvas_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _render_trend_chart(self, trend_data):
        for w in self.trend_canvas_holder.winfo_children():
            w.destroy()

        fig = Figure(figsize=(4.5, 3.8), dpi=90)
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_hex = "#1E293B" if is_dark else "#FFFFFF"
        text_color = "#E2E8F0" if is_dark else "#334155"

        fig.patch.set_facecolor(bg_hex)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_hex)

        has_data = any(t.get("income_total", 0) > 0 or t.get("expense_total", 0) > 0 for t in trend_data)

        if not has_data:
            ax.text(0.5, 0.5, "ยังไม่มีข้อมูลแนวโน้มรายเดือน\n(เริ่มต้นจาก 0)", 
                    ha="center", va="center", color=text_color, fontsize=12, fontfamily="Leelawadee UI")
            ax.axis("off")
        else:
            months = [t["month_str"] for t in trend_data]
            incomes = [t["income_total"] for t in trend_data]
            expenses = [t["expense_total"] for t in trend_data]

            import numpy as np
            x = np.arange(len(months))
            width = 0.35

            rects1 = ax.bar(x - width/2, incomes, width, label="รายรับ", color="#10B981")
            rects2 = ax.bar(x + width/2, expenses, width, label="รายจ่าย", color="#EF4444")

            ax.set_xticks(x)
            ax.set_xticklabels(months, color=text_color, fontsize=9, fontfamily="Leelawadee UI")
            ax.tick_params(colors=text_color)
            leg = ax.legend(facecolor=bg_hex, edgecolor=text_color, labelcolor=text_color)
            for text in leg.get_texts():
                text.set_fontfamily("Leelawadee UI")

            for spine in ["top", "right", "left", "bottom"]:
                ax.spines[spine].set_color("#475569" if is_dark else "#CBD5E1")

        canvas = FigureCanvasTkAgg(fig, master=self.trend_canvas_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
