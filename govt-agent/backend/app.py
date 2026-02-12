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
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Shreya's Interactive Space ✨</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{
    --bg1:#0f172a; --bg2:#1e293b; --accent:#22d3ee; --accent2:#38bdf8; --text:#e2e8f0; --muted:#94a3b8;
  }
  *{box-sizing:border-box}
  body{
    margin:0; padding:0; font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
    background: linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg1));
    background-size: 300% 300%;
    animation: bgflow 12s ease infinite;
    color: var(--text); overflow-x:hidden;
  }
  @keyframes bgflow{0%{background-position:0 50%}50%{background-position:100% 50%}100%{background-position:0 50%}}

  .container{max-width:1100px; margin:auto; padding:48px 20px; animation:fadeIn 1.1s ease-out}
  @keyframes fadeIn{from{opacity:0; transform: translateY(24px);}to{opacity:1; transform: translateY(0);}}

  .title{
    font-size: clamp(28px, 4.8vw, 48px); font-weight: 800; text-align:center; margin: 0 0 8px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), #a5f3fc);
    -webkit-background-clip: text; color: transparent; animation: float 3s ease-in-out infinite;
  }
  @keyframes float{0%{transform:translateY(0)}50%{transform:translateY(-8px)}100%{transform:translateY(0)}}

  .subtitle{ text-align:center; color:var(--muted); margin:0 0 22px; }

  .actions{ display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-bottom:26px; }
  .btn{
    display:inline-flex; align-items:center; gap:8px; padding:12px 16px; border-radius:12px; font-weight:700;
    text-decoration:none; transition: transform .08s ease, box-shadow .25s ease, background .25s ease;
  }
  .btn:hover{ transform: translateY(-1px); }
  .btn-primary{
    background: linear-gradient(90deg, var(--accent), var(--accent2)); color:#06232a;
    box-shadow: 0 8px 22px rgba(34,211,238,0.35);
  }
  .btn-ghost{
    background: rgba(255,255,255,0.06); color:var(--text); border:1px solid rgba(255,255,255,0.12);
  }

  .grid{
    display:grid; grid-template-columns: repeat(12, 1fr); gap:18px; margin-top: 10px;
  }
  .card{
    grid-column: span 12;
    background: rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:18px; padding:20px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
    transition: transform .25s ease;
  }
  .card:hover{ transform: translateY(-3px); }

  .section-title{ font-size:20px; color: var(--accent2); margin:4px 0 12px; font-weight:800; letter-spacing:.3px; }

  .hobbies{ display:flex; gap:12px; flex-wrap:wrap; }
  .badge{
    padding:10px 14px; border-radius:12px; font-weight:700;
    background: rgba(34,211,238,0.18); border:1px solid rgba(34,211,238,0.38);
    animation: pulse 2.6s infinite;
  }
  @keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.06)}100%{transform:scale(1)}}

  .image-row{ display:flex; flex-wrap:wrap; gap:16px; margin-top:8px; }
  .image-row a{ display:inline-block; border-radius:16px; overflow:hidden; }
  .image-row img{
    width: 220px; height: 220px; object-fit: cover; display:block;
    transition: transform .35s ease, box-shadow .35s ease; border:1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 18px rgba(0,0,0,0.5);
  }
  .image-row img:hover{ transform: scale(1.12) rotate(2deg); box-shadow: 0 12px 28px rgba(34,211,238,0.45); }

  /* Responsive columns */
  @media (min-width: 740px){
    .span-6{ grid-column: span 6; }
  }

  .video-wrap{
    position: relative; padding-top: 56.25%; /* 16:9 */
    width: 100%; border-radius: 16px; overflow: hidden; border:1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 30px rgba(0,0,0,0.45); background: #0b1324; margin-top: 12px;
  }
  .video-wrap iframe{
    position:absolute; top:0; left:0; width:100%; height:100%; border:0;
  }

  .footer{ color:var(--muted); text-align:center; margin-top:16px; font-size:12px; }
</style>
</head>
<body>

  <div class="container">
    <h1 class="title">How are you, Shreya? 💙</h1>
    <p class="subtitle">Welcome to your interactive space — hobbies, cute vibes, and your channel!</p>

    <div class="actions">
      <a class="btn btn-primary" href="https://www.youtube.com/@somewhatshreyaa" target="_blank" rel="noopener">
        ▶️ Visit Shreya’s YouTube Channel
      </a>
      <a class="btn btn-ghost" href="/healthz">🩺 Check API Health</a>
    </div>

    <section class="grid">
      <div class="card span-6">
        <div class="section-title">💫 Your Hobbies</div>
        <div class="hobbies">
          <span class="badge">😴 Sleeping</span>
          <span class="badge">🍽️ Eating</span>
          <span class="badge">🎶 Music</span>
          <span class="badge">📷 Aesthetic Pics</span>
        </div>
      </div>

      <div class="card span-6">
        <div class="section-title">📣 Channel Spotlight</div>
        <p style="margin:0 0 8px;color:var(--muted)">Click to explore your latest shorts & videos on YouTube.</p>
        <a class="btn btn-primary" href="https://www.youtube.com/@somewhatshreyaa" target="_blank" rel="noopener">Open Channel</a>
      </div>

      <div class="card">
        <div class="section-title">🐻 Fresh Bear Pics</div>
        <div class="image-row">
          <!-- Bear Images (new set) -->
          <a href="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?auto=format&fit=crop&w=600&q=60" alt="Cute bear 1">
          </a>
          <a href="https://images.unsplash.com/photo-1508672019048-805c876b67e2?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1508672019048-805c876b67e2?auto=format&fit=crop&w=600&q=60" alt="Polar bear">
          </a>
          <a href="https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=600&q=60" alt="Brown bear closeup">
          </a>
        </div>
      </div>

      <div class="card">
        <div class="section-title">🍦 Ice‑Cream Aesthetic</div>
        <div class="image-row">
          <!-- Ice-cream Images (new set) -->
          <a href="https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?auto=format&fit=crop&w=600&q=60" alt="Ice-cream cones">
          </a>
          <a href="https://images.unsplash.com/photo-1542444459-db63c9f5f10d?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1542444459-db63c9f5f10d?auto=format&fit=crop&w=600&q=60" alt="Scoop of ice-cream">
          </a>
          <a href="https://images.unsplash.com/photo-1464347744102-11db6282f854?auto=format&fit=crop&w=1600&q=60" target="_blank" rel="noopener">
            <img src="https://images.unsplash.com/photo-1464347744102-11db6282f854?auto=format&fit=crop&w=600&q=60" alt="Colorful ice-cream">
          </a>
        </div>
      </div>

      <div class="card">
        <div class="section-title">🎬 Featured Short</div>
        <p style="margin:0 0 8px;color:var(--muted)">Enjoy this YouTube Short right here on the page.</p>
        <div class="video-wrap">
          <!-- Embed Shorts: switch /shorts/{id} → /embed/{id} -->
          <iframe
            src="https://www.youtube.com/embed/0yGxtEFgO5g"
            title="YouTube Shorts"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen
          ></iframe>
        </div>
        <div style="margin-top:10px;">
          <a class="btn btn-ghost" href="https://www.youtube.com/shorts/0yGxtEFgO5g" target="_blank" rel="noopener">Open on YouTube ↗</a>
        </div>
      </div>

    </section>

    <div class="footer">Made with 💙 • Interactive UI • FastAPI on Render</div>
  </div>
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


