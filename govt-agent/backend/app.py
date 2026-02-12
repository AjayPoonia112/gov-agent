import os, json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
from dotenv import load_dotenv
from typing import Dict, Any
from twilio.twiml.messaging_response import MessagingResponse

from backend.schemas import UserProfile, EligibilityResponse
from backend.rules_engine import find_matches
from backend.pdf_generator import build_pdf

load_dotenv()
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="Gov Scheme Eligibility Backend", version="0.1.0")

# --- Load KB (JSON for MVP) ---
with open(os.path.join(os.path.dirname(__file__), "data/schemes.json"), "r", encoding="utf-8") as f:
    SCHEMES = json.load(f)

# --- Simple in-memory sessions for WhatsApp ---
SESSIONS: Dict[str, Dict[str, Any]] = {}

# --- Utility: build eligibility summary dicts ---
def summarize_matches(matches):
    summary = []
    for m in matches:
        s = m["scheme"]
        summary.append({
            "scheme_id": s["scheme_id"],
            "scheme_name": s["scheme_name"],
            "benefits": s.get("benefits"),
            "documents_required": s.get("documents_required", []),
            "application_steps": s.get("application_steps", []),
            "official_url": s.get("official_url"),
            "score": m["score"],
            "reasons": m["reasons"]
        })
    return summary

# -----------------------------
# Health check
# -----------------------------
@app.get("/healthz")
def health():
    return {"status": "ok"}

# -----------------------------
# Eligibility API
# -----------------------------
@app.post("/eligibility", response_model=EligibilityResponse)
def eligibility(profile: UserProfile):
    user = profile.model_dump()
    matches = find_matches(user, SCHEMES, user_state=user.get("state", "ALL"))
    summary = summarize_matches(matches)
    return {"eligible_schemes": summary}

# -----------------------------
# PDF API (optional)
# -----------------------------
@app.post("/pdf")
def pdf(profile: UserProfile):
    res = eligibility(profile)  # reuse
    pdf_path = build_pdf(profile.model_dump(), res["eligible_schemes"], lang="en")
    return FileResponse(pdf_path, media_type="application/pdf", filename="guide.pdf")

# -----------------------------
# WhatsApp Webhook (Twilio Sandbox)
# -----------------------------
@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Twilio will POST form-encoded data.
    We respond with TwiML XML.
    """
    form = await request.form()
    from_ = form.get("From")
    body = (form.get("Body") or "").strip()

    resp = MessagingResponse()
    msg = resp.message()

    session = SESSIONS.get(from_, {"lang": "bn", "stage": 0, "profile": {}})
    stage = session["stage"]

    # Basic flow (MVP)
    if stage == 0:
        msg.body("স্বাগতম! ভাষা নির্বাচন করুন:\n1) বাংলা  2) हिन्दी  3) English")
        session["stage"] = 1

    elif stage == 1:
        mapping = {"1": "bn", "2": "hi", "3": "en"}
        session["lang"] = mapping.get(body, "bn")
        msg.body("আপনার পেশা কী? (farmer/student/worker/other)")
        session["stage"] = 2

    elif stage == 2:
        occ = body.lower()
        session["profile"]["occupation"] = occ
        if occ == "farmer":
            msg.body("আপনি কি কৃষিজমির মালিক? (yes/no)")
            session["stage"] = 21
        else:
            msg.body("আপনার বার্ষিক আয় (₹) কত?")
            session["stage"] = 3

    elif stage == 21:
        session["profile"]["land_owned"] = body.lower().startswith("y")
        msg.body("বার্ষিক আয় (₹) কত?")
        session["stage"] = 3

    elif stage == 3:
        # Parse income safely
        try:
            income = int(body.replace(",", "").strip())
        except Exception:
            income = None
        session["profile"]["annual_income"] = income
        msg.body("রেশন কার্ড আছে কি? (yes/no)")
        session["stage"] = 4

    elif stage == 4:
        session["profile"]["has_ration_card"] = body.lower().startswith("y")
        # Call eligibility
        r = eligibility(UserProfile(**session["profile"]))
        schemes = r["eligible_schemes"]
        if schemes:
            lines = [f"- {s['scheme_name']}" for s in schemes[:3]]
            msg.body("আপনি সম্ভবত যোগ্য:\n" + "\n".join(lines) + "\nPDF পেতে 1 লিখুন।")
            session["stage"] = 5
        else:
            msg.body("কিছু পাওয়া যায়নি। আরো তথ্য দিন: বয়স, রাজ্য কোড (যেমন WB)। আবার শুরু করতে 'Hi' লিখুন।")
            session["stage"] = 2

    elif stage == 5:
        if body.strip() == "1":
            # Generate PDF and (in production) send as media via WhatsApp API (requires media hosting)
            msg.body("পিডিএফ প্রস্তুত হচ্ছে… অনুগ্রহ করে ওয়েবে ডাউনলোড করুন: /pdf এপিআই শীঘ্রই যুক্ত হবে।")
            session["stage"] = 0
        else:
            msg.body("ধন্যবাদ! সাহায্য চাইলে 'Hi' লিখুন।")
            session["stage"] = 0

    SESSIONS[from_] = session
    return Response(content=str(resp), media_type="application/xml")