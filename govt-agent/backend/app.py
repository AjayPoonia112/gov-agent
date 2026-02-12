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

#------------------
#Test Shreya
#--------------------
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Gov Agent</title>
      <style>
        :root{
          --bg: #0f172a;
          --card: #111827;
          --accent: #22d3ee;
          --text: #e5e7eb;
          --muted: #9ca3af;
        }
        * { box-sizing: border-box; }
        body {
          margin:0; padding:0;
          font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
          background: radial-gradient(1200px 600px at 80% -10%, rgba(34,211,238,0.15), transparent 60%), var(--bg);
          color: var(--text);
          min-height: 100dvh;
          display: grid;
          place-items: center;
        }
        .card {
          width: min(680px, 92vw);
          background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 16px;
          padding: 28px 28px 24px;
          backdrop-filter: blur(8px);
          box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        }
        .badge {
          display: inline-flex; align-items: center; gap: 8px;
          background: rgba(34,211,238,0.12);
          color: #a5f3fc;
          padding: 6px 10px;
          border: 1px solid rgba(34,211,238,0.35);
          border-radius: 999px;
          font-size: 12px; letter-spacing: .35px;
        }
        h1 {
          margin: 14px 0 10px;
          font-size: clamp(24px, 3.5vw, 34px);
          line-height: 1.2;
        }
        p.lead { color: var(--muted); margin: 0 0 18px; font-size: 15px; }
        .cta {
          display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px;
        }
        .btn {
          appearance: none; border: 0; cursor: pointer;
          border-radius: 12px; padding: 12px 16px; font-weight: 600;
          transition: transform .06s ease, box-shadow .2s ease, background .2s ease;
        }
        .btn-primary {
          background: linear-gradient(90deg, #22d3ee, #06b6d4);
          color: #06232a; box-shadow: 0 8px 22px rgba(34,211,238,0.35);
        }
        .btn-primary:hover { transform: translateY(-1px); }
        .btn-ghost {
          background: rgba(255,255,255,0.06); color: var(--text);
          border: 1px solid rgba(255,255,255,0.12);
        }
        .grid {
          display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 22px;
        }
        .feature {
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 12px; padding: 14px;
        }
        .feature h3 { margin: 0 0 6px; font-size: 14px; }
        .muted { color: var(--muted); font-size: 13px; }
        .footer {
          margin-top: 18px; display:flex; justify-content: space-between; align-items:center;
          color: var(--muted); font-size: 12px;
        }
        @media (max-width: 720px) {
          .grid { grid-template-columns: 1fr; }
        }
      </style>
    </head>
    <body>
      <main class="card" role="main" aria-label="Government Scheme Eligibility Agent">
        <span class="badge" aria-label="Status badge">✅ Live • Gov Agent</span>
        <h1>How are you, <span style="color:#22d3ee">Shreya</span>?</h1>
        <p class="lead">Welcome to your Government Scheme Eligibility Assistant. Check your eligibility, get step-by-step instructions, and download a personalized guide.</p>

        <div class="cta">
          <a class="btn btn-primary" href="/healthz" aria-label="Check API Health">Check API Health</a>
          <a class="btn btn-ghost" href="https://wa.me/14155238886" target="_blank" rel="noreferrer" aria-label="Open WhatsApp Sandbox">Open WhatsApp Sandbox</a>
        </div>

        <div class="grid" aria-label="Highlights">
          <div class="feature">
            <h3>🎯 Simple Questions</h3>
            <div class="muted">Answer in Bengali / Hindi / English. We’ll ask only what’s needed.</div>
          </div>
          <div class="feature">
            <h3>⚖️ Eligibility Match</h3>
            <div class="muted">Rules-based engine maps your profile to central & state schemes.</div>
          </div>
          <div class="feature">
            <h3>🧾 PDF Guide</h3>
            <div class="muted">Get a one‑page personalized guide with steps and documents.</div>
          </div>
          <div class="feature">
            <h3>💬 WhatsApp First</h3>
            <div class="muted">Chat from your phone; perfect for low‑literacy & low‑bandwidth users.</div>
          </div>
        </div>

        <div class="footer">
          <span>Made for communities • Kolkata</span>
          <span>v0.1 • FastAPI on Render</span>
        </div>
      </main>
    </body>
    </html>
    """
    #--------------
    #test shreya
    #--------------------

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
