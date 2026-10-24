import csv

class ReportExporter:
    @staticmethod
    def export_transactions_to_csv(transactions, filepath):
        # บันทึกข้อมูลออกมาเป็นไฟล์ CSV โดยใช้ utf-8-sig เพื่อให้อ่านภาษาไทยใน Excel ได้
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8-sig") as csv_file:
                fieldnames = ["ID", "วันที่", "ประเภท", "หมวดหมู่", "จำนวนเงิน (บาท)", "ช่องทางการชำระ", "บันทึก"]
                writer = csv.writer(csv_file)
                writer.writerow(fieldnames)

                for tx in transactions:
                    tx_type_th = "รายรับ" if tx["type"] == "income" else "รายจ่าย"
                    writer.writerow([
                        tx["id"],
                        tx["date"],
                        tx_type_th,
                        tx["category"],
                        f"{tx['amount']:,.2f}",
                        tx["payment_method"],
                        tx["note"] or "-"
                    ])
            return True, f"บันทึกไฟล์สำเร็จ: {filepath}"
        except Exception as e:
            return False, f"ไม่สามารถส่งออกข้อมูลได้: {str(e)}"
