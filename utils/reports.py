from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from datetime import datetime

def generate_pdf_report(claim_details, risk_score, reasons):
    """
    Generates a PDF report for a given claim.
    Returns bytes.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Health Insurance Fraud Investigation Report")
    
    # Date
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Line
    c.setStrokeColor(colors.black)
    c.line(50, height - 80, width - 50, height - 80)
    
    # Claim Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 110, "Claim Details")
    
    c.setFont("Helvetica", 12)
    y_pos = height - 130
    for key, value in claim_details.items():
        c.drawString(50, y_pos, f"{key}: {value}")
        y_pos -= 20
        
    # Risk Score
    y_pos -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, f"Fraud Risk Score: {risk_score}/100")
    
    if risk_score > 80:
        c.setFillColor(colors.red)
        c.drawString(250, y_pos, "CRITICAL RISK")
    elif risk_score > 50:
        c.setFillColor(colors.orange)
        c.drawString(250, y_pos, "HIGH RISK")
    else:
        c.setFillColor(colors.green)
        c.drawString(250, y_pos, "LOW RISK")
        
    c.setFillColor(colors.black)
    
    # Explanations
    y_pos -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, "Key Risk Factors (SHAP Analysis):")
    
    c.setFont("Helvetica", 12)
    y_pos -= 20
    for reason in reasons:
        c.drawString(60, y_pos, f"• {reason}")
        y_pos -= 20
        
    # Signatures
    y_pos -= 60
    c.setFont("Helvetica", 12)
    c.drawString(50, y_pos, "Auditor Signature: _______________________")
    c.drawString(350, y_pos, "Date: _______________________")
    
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
