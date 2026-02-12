from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import tempfile

def build_pdf(user, eligible_schemes, lang="en"):
    fd, path = tempfile.mkstemp(suffix=".pdf")
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    margin = 2*cm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - margin, "Eligibility & Application Guide")
    y = height - margin - 1*cm

    c.setFont("Helvetica", 10)
    for k in ["state", "district", "occupation", "annual_income"]:
        if user.get(k) is not None:
            c.drawString(margin, y, f"{k.capitalize()}: {user.get(k)}"); y -= 0.5*cm
    y -= 0.3*cm

    for s in eligible_schemes[:3]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, f"• {s['scheme_name']}"); y -= 0.5*cm
        c.setFont("Helvetica", 10)
        if s.get("benefits"):
            c.drawString(margin, y, f"Benefits: {s['benefits']}"); y -= 0.45*cm
        if s.get("documents_required"):
            c.drawString(margin, y, f"Docs: {', '.join(s['documents_required'])}"); y -= 0.45*cm
        if s.get("application_steps"):
            c.drawString(margin, y, "Steps:"); y -= 0.4*cm
            for step in s["application_steps"][:4]:
                c.drawString(margin+0.5*cm, y, f"- {step}"); y -= 0.4*cm
        if s.get("official_url"):
            c.drawString(margin, y, f"Official: {s['official_url']}"); y -= 0.5*cm

        y -= 0.3*cm
        if y < 3*cm:
            c.showPage()
            y = height - margin

    c.save()
    return path