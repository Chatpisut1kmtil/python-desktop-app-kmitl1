"""
FlowBudget - Automated PowerPoint Presentation Generator (KMITL Group of 3 Members)
Creates 'FlowBudget_Presentation.pptx' with exact real names, student IDs, and emails.
"""

import sys
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    print("[!] python-pptx is required. Run: pip install python-pptx")
    sys.exit(1)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 Widescreen
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    PRIMARY = RGBColor(56, 189, 248)    # Sky 400
    TEXT_WHITE = RGBColor(248, 250, 252)
    TEXT_MUTED = RGBColor(148, 163, 184)

    slides_content = [
        {
            "slide_num": "1",
            "presenter": "สมาชิกทุกคนในกลุ่ม (3 คน)",
            "title": "FlowBudget - Smart Personal Finance Tracker",
            "subtitle": "โปรแกรมบริหารจัดการรายรับ-รายจ่ายและวิเคราะห์การเงินส่วนบุคคลบนเดสก์ท็อป",
            "points": [
                "สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง (KMITL)",
                "อาจารย์ผู้สอน: อาจารย์ไพบูลย์ พงษ์วงศ์ตระกูล",
                "วิชา: การพัฒนาซอฟต์แวร์และการนำเสนอโครงงาน (Python Desktop Application)",
                "สมาชิกในกลุ่ม 3 คน และหน้าที่ความรับผิดชอบ:",
                "  1. นายฉัตรพิศุทธิ์ เพียรธานี (รหัสนักศึกษา 69030037) - UI/UX Design & Dashboard Controller (Lead)",
                "  2. นายนพรักตน์ ราชภักดี (รหัสนักศึกษา 69030122) - Database Architecture & Backend Logic",
                "  3. นายเตชวิชญ์ อัจกลับ (รหัสนักศึกษา 69030089) - CRUD Operations, Data Analytics & Budget (GitHub: Tofu-png)"
            ]
        },
        {
            "slide_num": "2",
            "presenter": "นายฉัตรพิศุทธิ์ เพียรธานี",
            "title": "2. ความเป็นมาของโครงงาน (Background & Motivation)",
            "subtitle": "ปัญหาด้านการบริหารการเงินส่วนบุคคลในยุคเศรษฐกิจปัจจุบัน",
            "points": [
                "พฤติกรรมทางการเงินของคนรุ่นใหม่และนักศึกษาส่วนใหญ่มักประสบปัญหา 'เงินรั่วไหล' ไม่รู้ว่าเงินหายไปไหนในแต่ละเดือน",
                "แอปพลิเคชันบนสมาร์ทโฟนทั่วไปมักพ่วงโฆษณา ต้องจ่ายเงินรายเดือน และกังวลเรื่องความเป็นส่วนตัวของข้อมูลการเงิน",
                "การใช้ Excel ทั่วไปมีความซับซ้อน ต้องเขียนสูตรเอง และไม่ตอบโจทย์ความสะดวกรวดเร็วในการใช้งานประจำวัน",
                "จึงเกิดแนวคิดพัฒนา FlowBudget แอปพลิเคชันเดสก์ท็อปที่เก็บข้อมูลในเครื่อง ปลอดภัย ใช้งานง่าย และวิเคราะห์ผลลัพธ์ผ่านกราฟสถิติได้แบบเรียลไทม์"
            ]
        },
        {
            "slide_num": "3",
            "presenter": "นายฉัตรพิศุทธิ์ เพียรธานี",
            "title": "3. วัตถุประสงค์ของโครงงาน (Objectives)",
            "subtitle": "เป้าหมายหลักของการพัฒนาซอฟต์แวร์",
            "points": [
                "1. เพื่อพัฒนาแอปพลิเคชัน Desktop ด้วยภาษา Python ที่มีส่วนต่อประสานผู้ใช้ (GUI) ที่ทันสมัยและใช้งานง่าย",
                "2. เพื่อพัฒนาระบบบันทึก จัดการ และค้นหาประวัติรายรับ-รายจ่าย (CRUD) ที่แม่นยำ ปลอดภัย และไร้โฆษณารบกวน",
                "3. เพื่อสร้างระบบสรุปผลสถิติและกราฟแสดงผลสัดส่วนค่าใช้จ่าย (Donut Chart & Monthly Trend) โดยใช้ Matplotlib",
                "4. เพื่อสร้างระบบควบคุมงบประมาณ (Budget Alert) พร้อมแถบเตือนสี เขียว/เหลือง/แดง เมื่อค่าใช้จ่ายใกล้เต็มหรือเกินเกณฑ์",
                "5. เพื่อรองรับการส่งออกข้อมูลประวัติธุรกรรมเป็นไฟล์ CSV นำไปเปิดใน Microsoft Excel ได้อย่างสมบูรณ์"
            ]
        },
        {
            "slide_num": "4",
            "presenter": "นายฉัตรพิศุทธิ์ เพียรธานี & นายเตชวิชญ์ อัจกลับ",
            "title": "4. ขีดความสามารถ และสาธิตตัวอย่างโปรแกรม (Demo & Features)",
            "subtitle": "การทำงานของโปรแกรม FlowBudget ที่พัฒนาเสร็จสมบูรณ์",
            "points": [
                "✨ Financial Summary Cards: ยอดคงเหลือรวม, รายรับเดือนนี้, รายจ่ายเดือนนี้, อัตราการออม (%)",
                "⚡ Dynamic Transaction Logging: ฟอร์มบันทึกพร้อมช่องทางชำระ (เงินสด, โอน, บัตร, E-Wallet) และระบบค้นหา Realtime",
                "📊 Data Visualization: Donut Chart สัดส่วนค่าใช้จ่ายแยกตามหมวดหมู่ + Bar Chart รายรับ/รายจ่าย 5 เดือนย้อนหลัง",
                "🎯 Budget Threshold Progress: แจ้งเตือนสถานะงบประมาณอัตโนมัติ (ปกติ <75%, เฝ้าระวัง 75-99%, เกินงบ >=100%)",
                "🌗 Dual Mode Appearance: สลับธีม Dark Mode และ Light Mode ได้อย่างราบรื่น",
                "📁 Data Export Engine: ส่งออกข้อมูลประวัติการเงินออกมาเป็นไฟล์ CSV (UTF-8 with BOM รองรับภาษาไทย 100%)"
            ]
        },
        {
            "slide_num": "5",
            "presenter": "นายนพรักตน์ ราชภักดี",
            "title": "5. โมเดลการพัฒนาซอฟต์แวร์ (Agile / Scrum Methodology)",
            "subtitle": "การแบ่งบทบาทหน้าที่ของสมาชิก 3 คนตามระเบียบวิธีพัฒนาซอฟต์แวร์",
            "points": [
                "เลือกใช้โมเดล Agile แบบ Scrum Framework แบ่งรอบการทำงานเป็น 3 Sprints ย่อย (Sprint ละ 1 สัปดาห์):",
                "  • Sprint 1: วิเคราะห์ความต้องการ ออกแบบ ER-Diagram และเขียนฐานข้อมูล SQLite",
                "  • Sprint 2: พัฒนา UI Components ด้วย CustomTkinter และฟอร์ม Modal สำหรับ CRUD",
                "  • Sprint 3: นำโมดูลกราฟ Matplotlib และระบบ Budget มาต่อเชื่อม พร้อมทดสอบ Integration Testing",
                "หน้าที่ความรับผิดชอบของสมาชิกทั้ง 3 คน:",
                "  • นายฉัตรพิศุทธิ์ เพียรธานี: UI/UX & Frontend Lead (รับผิดชอบ config.py, components/nav_bar.py, dashboard_view.py)",
                "  • นายนพรักตน์ ราชภักดี: Scrum Master & Backend Lead (รับผิดชอบ database/db_manager.py, utils/exporter.py)",
                "  • นายเตชวิชญ์ อัจกลับ: Full-Stack Logic & QA (รับผิดชอบ transactions_view.py, modal_dialogs.py, analytics_view.py, budget_view.py)"
            ]
        },
        {
            "slide_num": "6",
            "presenter": "นายนพรักตน์ ราชภักดี",
            "title": "6. สถาปัตยกรรมและโครงสร้างของโครงงาน (System Architecture)",
            "subtitle": "การออกแบบเชิงสถาปัตยกรรมแบบ Modular Separation of Concerns (MVC)",
            "points": [
                "สถาปัตยกรรมระบบแบ่งออกเป็น 4 ชั้นเลเยอร์ (Layered Architecture):",
                "  1. Presentation Layer (views/ & components/): แสดงผลผ่าน CustomTkinter ตอบสนองการโต้ตอบของผู้ใช้",
                "  2. Business Logic Layer (main.py & utils/): ควบคุมการไหลของข้อมูล การสลับหน้า และการ Export ข้อมูล",
                "  3. Data Access Layer (database/db_manager.py): จัดการติดต่อ SQLite ด้วย Parameterized Queries ป้องกัน Injection",
                "  4. Storage Layer: ฐานข้อมูลไฟล์เดี่ยว 'finance_data.db' ภายในเครื่อง ปลอดภัยและพกพาง่าย",
                "ตารางฐานข้อมูลหลัก: transactions (ตารางบันทึกการเงิน) และ budgets (ตารางเพดานงบประมาณรายหมวดหมู่)"
            ]
        },
        {
            "slide_num": "7",
            "presenter": "นายเตชวิชญ์ อัจกลับ",
            "title": "7. อธิบายโค้ดส่วนสำคัญของโปรแกรม (Code Walkthrough)",
            "subtitle": "เจาะลึกโครงสร้างโค้ดและการออกแบบที่เป็นมาตรฐานวิศวกรรมซอฟต์แวร์",
            "points": [
                "1. Database Connection & Aggregation (db_manager.py):",
                "   - ใช้ Context Manager (`with self.get_connection() as conn:`) ป้องกัน Database Lock และ Memory Leak",
                "   - คำนวณยอดเงินด้วยคำสั่ง SQL Aggregate Functions: `SUM()`, `strftime()` ช่วยเพิ่มประสิทธิภาพการประมวลผล",
                "2. Dynamic Chart Integration (analytics_view.py):",
                "   - ฝัง Matplotlib FigureCanvasTkAgg ลงใน CTkFrame โดยตรง ปรับโทนสีกราฟให้เข้ากับ Dark Mode อัตโนมัติ",
                "3. Robust Form Validation (modal_dialogs.py):",
                "   - ตรวจสอบรูปแบบวันที่ (YYYY-MM-DD) ด้วย `datetime.strptime()` และเช็คจำนวนเงินให้เป็นตัวเลขมากกว่า 0 เสมอ"
            ]
        },
        {
            "slide_num": "8",
            "presenter": "นายเตชวิชญ์ อัจกลับ",
            "title": "8. ปัญหาที่พบและแนวทางแก้ไข (Challenges & Solutions)",
            "subtitle": "อุปสรรคทางเทคนิคระหว่างการพัฒนาและการแก้ปัญหาอย่างเป็นระบบ",
            "points": [
                "❌ ปัญหาที่ 1: การพล็อตกราฟ Matplotlib แล้วสีพื้นหลังขาวสว่าง ขัดแย้งกับ Dark Mode ของแอปพลิเคชัน",
                "   ✅ แนวทางแก้: ตรวจสอบสถานะ Dark Mode แล้วใช้คำสั่ง `fig.patch.set_facecolor('#1E293B')` ปรับสีพื้นหลังและตัวหนังสือ",
                "❌ ปัญหาที่ 2: การส่งออกไฟล์ CSV เป็นภาษาไทยแล้วเปิดใน Microsoft Excel มีปัญหาตัวอักษรเป็นภาษาต่างดาว",
                "   ✅ แนวทางแก้: กำหนด Encoding ตอนเขียนไฟล์เป็น `utf-8-sig` (ใส่ BOM) ทำให้ Excel อ่านภาษาไทยได้สมบูรณ์ 100%",
                "❌ ปัญหาที่ 3: เมื่อเพิ่มหรือลบรายการ ยอดเงินหน้า Dashboard ไม่ยอมอัปเดตทันที",
                "   ✅ แนวทางแก้: นำรูปแบบ Callback Function (`on_refresh_needed`) มาใช้เพื่อ Trigger ทุก View ให้รีเฟรชข้อมูลพร้อมกัน"
            ]
        },
        {
            "slide_num": "9",
            "presenter": "นายนพรักตน์ ราชภักดี",
            "title": "9. การนำไปประยุกต์ใช้งานและแนวทางพัฒนาต่อยอด (Future Work)",
            "subtitle": "ประโยชน์ในการใช้งานจริงและการต่อยอดในระดับอุตสาหกรรม",
            "points": [
                "การนำไปประยุกต์ใช้งานจริงในชีวิตประจำวัน:",
                "  • ใช้งานสำหรับนักเรียน นักศึกษา และบุคคลทั่วไป เพื่อฝึกวินัยทางการเงินและลดรายจ่ายฟุ่มเฟือย",
                "  • ใช้งานสำหรับร้านค้าขนาดเล็ก (SME) ในการลงบันทึกรับจ่ายเงินสดย่อยหน้าร้าน และสรุปงบสิ้นเดือน",
                "แนวทางการพัฒนาต่อยอดในอนาคต (Roadmap):",
                "  1. ระบบ AI OCR สแกนสลิปโอนเงิน / ใบเสร็จแล้วกรอกข้อมูลวันที่และจำนวนเงินเข้าตารางให้อัตโนมัติ",
                "  2. ระบบสำรองข้อมูลขึ้น Cloud Storage (Google Drive / OneDrive) พร้อมการเข้ารหัสฐานข้อมูล",
                "  3. ระบบพยากรณ์ค่าใช้จ่ายล่วงหน้าโดยใช้ Machine Learning (Time Series Forecasting)"
            ]
        },
        {
            "slide_num": "10",
            "presenter": "สมาชิกทุกคน (รายงานทีละคนตาม Branch ของตนเอง)",
            "title": "10. การทำงานบน GitHub และประวัติ Commit รายบุคคล (KMITL Team)",
            "subtitle": "แสดงบันทึกวันเวลาและประวัติการพัฒนาตั้งแต่วันแรกจนถึงปัจจุบัน",
            "points": [
                "Repository: github.com/Chatpisut1kmtil/python-desktop-app-kmitl1",
                "1. นายฉัตรพิศุทธิ์ เพียรธานี (69030037) - Branch: 'feat/ui-dashboard'",
                "   - Commit 1 (2026-10-23): Setup CustomTkinter window, responsive layout and navigation sidebar",
                "   - Commit 2 (2026-10-24): Build metric summary cards, recent transactions feed and theme toggle",
                "2. นายนพรักตน์ ราชภักดี (69030122) - Branch: 'feat/database-backend'",
                "   - Commit 1 (2026-10-23): Initial schema design, create tables for transactions & budgets",
                "   - Commit 2 (2026-10-23): Implement CRUD queries, aggregate calculations and CSV exporter",
                "3. นายเตชวิชญ์ อัจกลับ (69030089 - GitHub: Tofu-png) - Branch: 'feat/crud-analytics-budget'",
                "   - Commit 1 (2026-10-24): Build transaction list view, search filter and modal dialog with validation",
                "   - Commit 2 (2026-10-24): Integrate Matplotlib charts and budget progress alert system"
            ]
        }
    ]

    for data in slides_content:
        slide = prs.slides.add_slide(blank_layout)

        # Background Card
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_DARK
        bg_shape.line.fill.background()

        # Presenter Tag (Top Right - ตามข้อกำหนดอาจารย์)
        tag_box = slide.shapes.add_textbox(Inches(7.0), Inches(0.4), Inches(5.8), Inches(0.5))
        tf_tag = tag_box.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.alignment = PP_ALIGN.RIGHT
        run_tag = p_tag.add_run()
        run_tag.text = f"👤 ผู้นำเสนอ: {data['presenter']}"
        run_tag.font.size = Pt(13)
        run_tag.font.bold = True
        run_tag.font.color.rgb = PRIMARY

        # Title Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(7.0), Inches(1.2))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        p_sub = tf_title.add_paragraph()
        p_sub.text = data["subtitle"]
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED

        # Content Card Frame
        card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
        card_shape.fill.solid()
        card_shape.fill.fore_color.rgb = CARD_BG
        card_shape.line.color.rgb = RGBColor(51, 65, 85)
        card_shape.line.width = Pt(1)

        # Bullet Points
        content_box = slide.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.7))
        tf_content = content_box.text_frame
        tf_content.word_wrap = True

        for idx, pt in enumerate(data["points"]):
            p = tf_content.paragraphs[0] if idx == 0 else tf_content.add_paragraph()
            p.text = pt
            p.font.size = Pt(14)
            p.font.color.rgb = TEXT_WHITE
            p.space_after = Pt(10)
            if pt.startswith("  "):
                p.level = 1
                p.font.size = Pt(13)
                p.font.color.rgb = RGBColor(203, 213, 225)

    output_file = "FlowBudget_Presentation.pptx"
    prs.save(output_file)
    print(f"[+] Successfully generated PowerPoint presentation: {output_file}")

if __name__ == "__main__":
    build_presentation()
