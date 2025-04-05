# --- reports/generate_pdf.py (PDF Generator) ---

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

def generate_pdf_report(company_name, summary_text, filename="reputation_report.pdf"):
    filepath = os.path.join("reports", filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(50, 750, f"Reputation Report for {company_name}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Date: {datetime.date.today().isoformat()}")
    text_object = c.beginText(50, 700)
    text_object.textLines(summary_text)
    c.drawText(text_object)
    c.save()
    return filepath