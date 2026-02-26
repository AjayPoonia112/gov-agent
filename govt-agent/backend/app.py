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
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Shreya • Identity Check ✨</title>
<style>
  :root{
    --bg1:#0f172a; --bg2:#1e293b; --accent:#22d3ee; --accent2:#38bdf8; --text:#e2e8f0; --muted:#94a3b8;
    --ok:#10b981; --warn:#f59e0b; --err:#ef4444;
  }
  *{box-sizing:border-box}
  body{
    margin:0; padding:0; font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
    background: linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg1));
    background-size: 300% 300%; animation: bgflow 12s ease infinite;
    color: var(--text); overflow-x:hidden;
  }
  @keyframes bgflow{0%{background-position:0 50%}50%{background-position:100% 50%}100%{background-position:0 50%}}
  .container{max-width:1100px; margin:auto; padding:48px 18px; animation:fadeIn 0.9s ease-out}
  @keyframes fadeIn{from{opacity:0; transform: translateY(18px);}to{opacity:1; transform: translateY(0);}}
  .title{
    font-size: clamp(28px, 4.6vw, 48px); font-weight: 800; text-align:center; margin: 0 0 8px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), #a5f3fc);
    -webkit-background-clip: text; color: transparent; animation: float 3s ease-in-out infinite;
  }
  @keyframes float{0%{transform:translateY(0)}50%{transform:translateY(-6px)}100%{transform:translateY(0)}}
  .subtitle{ text-align:center; color:var(--muted); margin:0 0 20px; }

  .panel{
    background: rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:18px; padding:18px; margin-top:12px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
  }
  .panel:hover{ transform: translateY(-2px); transition: transform .25s ease; }

  .section-title{ font-size:20px; color: var(--accent2); margin:4px 0 12px; font-weight:800; letter-spacing:.3px; display:flex; align-items:center; gap:8px;}
  .row{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; }
  .input{
    flex:1 1 260px; display:flex; align-items:center; gap:10px;
    background: rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.14);
    padding:12px 14px; border-radius:14px;
  }
  .input input{
    width:100%; background: transparent; color:var(--text); border:0; outline:0; font-size:16px;
  }
  .btn{
    display:inline-flex; align-items:center; gap:8px; padding:12px 16px; border-radius:12px; font-weight:700;
    text-decoration:none; transition: transform .08s ease, box-shadow .25s ease, background .25s ease; cursor:pointer; border:0;
  }
  .btn:hover{ transform: translateY(-1px); }
  .btn-primary{
    background: linear-gradient(90deg, var(--accent), var(--accent2)); color:#06232a;
    box-shadow: 0 8px 22px rgba(34,211,238,0.35);
  }
  .btn-ghost{
    background: rgba(255,255,255,0.06); color:var(--text); border:1px solid rgba(255,255,255,0.12);
  }

  /* Gender section hidden by default; becomes visible with .show */
  .gender-wrap{ display:none; margin-top:12px; }
  .gender-wrap.show{ display:block; }

  .genders{ display:flex; gap:10px; flex-wrap:wrap; }
  .radio{
    position:relative; display:inline-flex; align-items:center; gap:10px;
    padding:10px 12px; border-radius:12px; font-weight:700; cursor:pointer;
    background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.14);
    user-select:none;
  }
  .radio input{ display:none; }
  .radio span{ opacity:0.9 }
  /* Style checked option (avoid :has for broader support) */
  .radio input:checked + span{
    outline:2px solid var(--accent2); border-radius:8px; padding:2px 6px;
    box-shadow: 0 6px 18px rgba(56,189,248,0.25);
    background: rgba(56,189,248,0.1);
  }

  .footer{ color:var(--muted); text-align:center; margin-top:18px; font-size:12px; }

  /* Modal */
  .modal{
    position:fixed; inset:0; display:none; place-items:center; background: rgba(10,14,25,0.6);
    z-index: 50; padding:16px;
  }
  .modal.show{ display:grid; animation: fadeIn .2s ease-out; }
  .modal-card{
    width:min(560px, 96vw);
    background:linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.06));
    border:1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(12px);
    border-radius:18px; padding:20px; text-align:center; position:relative; overflow:hidden;
    animation: pop .18s ease-out;
  }
  @keyframes pop{from{transform:scale(.96); opacity:.6}to{transform:scale(1); opacity:1}}
  .modal h3{ margin:4px 0 8px; font-size:22px }
  .modal p{ margin:0; color:var(--text) }
  .modal .ok{ color:var(--ok) }
  .modal .err{ color:var(--err) }
  .close{
    position:absolute; top:10px; right:10px; border:0; background:transparent; color:var(--muted); font-size:20px; cursor:pointer;
  }

  .confetti{
    position:absolute; left:0; top:0; width:100%; height:100%; pointer-events:none; overflow:hidden;
  }
  .piece{
    position:absolute; font-size:22px; animation: fall 1800ms linear forwards;
  }
  @keyframes fall{
    0%{ transform: translateY(-20px) rotate(0deg); opacity:1 }
    100%{ transform: translateY(520px) rotate(420deg); opacity:0 }
  }

  .video-wrap{
    position: relative; padding-top: 56.25%;
    width: 100%; border-radius: 16px; overflow: hidden; border:1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 30px rgba(0,0,0,0.45); background: #0b1324; margin-top: 12px;
  }
  .video-wrap iframe{
    position:absolute; top:0; left:0; width:100%; height:100%; border:0;
  }

  .grid{ display:grid; grid-template-columns: repeat(12, 1fr); gap:16px; margin-top: 16px; }
  .span-6{ grid-column: span 12; }
  @media (min-width: 740px){ .span-6{ grid-column: span 6; } }
</style>
</head>
<body>
  <div class="container">
    <h1 class="title">How are you, Shreya? 💙</h1>
    <p class="subtitle">Identify yourself (with sparkles ✨) &mdash; then explore your channel!</p>

    <!-- Name Panel -->
    <section class="panel">
      <div class="section-title">🧩 Step 1: Enter your name</div>
      <div class="row">
        <div class="input">
          <span>👤</span>
          <input id="name" type="text" placeholder="Type your name… e.g., shreya" />
        </div>
        <button id="nameGo" class="btn btn-primary">Continue →</button>
      </div>
      <p id="nameHint" style="margin:8px 2px 0; color:var(--muted); font-size:14px;">
        Tip: The gender box unlocks only when the name is <strong>shreya</strong> (case-insensitive).
      </p>

      <!-- Gender Panel (hidden until name is shreya) -->
      <div id="genderSection" class="gender-wrap">
        <div class="section-title" style="margin-top:14px;">🐻 Step 2: Choose your gender</div>
        <div class="genders" role="group" aria-label="Gender choices">
          <label class="radio"> <input type="radio" name="gender" value="female" /><span>💃 female</span> </label>
          <label class="radio"> <input type="radio" name="gender" value="male" /><span>🕺 male</span> </label>
          <label class="radio"> <input type="radio" name="gender" value="angel" /><span>😇 angel</span> </label>
          <label class="radio"> <input type="radio" name="gender" value="bhaluu" /><span>🐻 bhaluu</span> </label>
        </div>
        <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
          <button id="verify" class="btn btn-primary">Verify ✅</button>
          <button id="reset" class="btn btn-ghost">Reset ↺</button>
        </div>
      </div>
    </section>

    <!-- Channel section -->
    <section class="grid">
      <div class="panel span-6">
        <div class="section-title">📣 Channel Spotlight</div>
        <p style="margin:0 0 8px;color:var(--muted)">Click to explore your latest shorts &amp; videos on YouTube.</p>
        https://www.youtube.com/@somewhatshreyaa▶️ Visit Shreya’s YouTube Channel</a>
        <a class="btn btn-ghost" hrefa>
      </div>
      <div class="panel span-6">
        <div class="section-title">🎬 Featured Short</div>
        <p style="margin:0 0 8px;color:var(--muted)">Enjoy this YouTube Short right here on the page.</p>
        <div class="video-wrap">
          <iframe
            src="https://www.youtube.com/embed/0yGxtEFgO5g"
            title="YouTube Shorts"
            <a class="btn btn-ghost" href="https://www.youtube.com/shorts/0yGxtEFgO5</div>
      </div>
    </section>

    <div class="footer">Made with 💙 • Interactive UI • FastAPI on Render</div>
  </div>

  <!-- Modal -->
  <div id="modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
    <div class="modal-card">
      <button class="close" aria-label="Close modal" onclick="closeModal()">✖</button>
      <div id="confetti" class="confetti"></div>
      <h3 id="modalTitle">Title</h3>
      <p id="modalMsg">Message</p>
    </div>
  </div>

<script>
  const nameInput = document.getElementById('name');
  const nameGo = document.getElementById('nameGo');
  const nameHint = document.getElementById('nameHint');
  const genderSection = document.getElementById('genderSection');
  const verifyBtn = document.getElementById('verify');
  const resetBtn = document.getElementById('reset');

  function isShreya(val){
    return (val || '').trim().toLowerCase() === 'shreya';
  }
  function toggleGenderSection(show){
    if(show) genderSection.classList.add('show');
    else genderSection.classList.remove('show');
  }
  function clearRadios(){
    document.querySelectorAll('input[name="gender"]').forEach(r => r.checked = false);
  }
  function showModal(type, title, message){
    const modal = document.getElementById('modal');
    const titleEl = document.getElementById('modalTitle');
    const msgEl = document.getElementById('modalMsg');
    const confetti = document.getElementById('confetti');
    titleEl.className = (type === 'ok') ? 'ok' : 'err';
    titleEl.textContent = title;
    msgEl.textContent = message;
    confetti.innerHTML = '';
    if(type === 'ok') {
      const icons = ['🎉','✨','💫','🐻','🌟','🎊'];
      for(let i=0;i<60;i++){
        const span = document.createElement('span');
        span.className = 'piece';
        span.textContent = icons[Math.floor(Math.random()*icons.length)];
        span.style.left = Math.random()*100 + '%';
        span.style.top = (-20 - Math.random()*80) + 'px';
        span.style.animationDelay = (Math.random()*0.5)+'s';
        span.style.fontSize = (18 + Math.random()*12)+'px';
        confetti.appendChild(span);
      }
    }
    modal.classList.add('show');
  }
  function closeModal(){
    document.getElementById('modal').classList.remove('show');
  }

  // Show/hide while typing (live)
  nameInput.addEventListener('input', () => {
    const ok = isShreya(nameInput.value);
    toggleGenderSection(ok);
    nameHint.innerHTML = ok
      ? '✅ Hi Shreya! Please choose your gender below.'
      : '⚠️ This flow is only for <strong>shreya</strong>. Please enter "shreya" to proceed.';
  });

  // Also support the Continue button + Enter
  nameInput.addEventListener('keydown', (e) => { if(e.key === 'Enter'){ nameGo.click(); } });
  nameGo.addEventListener('click', () => {
    const ok = isShreya(nameInput.value);
    toggleGenderSection(ok);
    nameHint.innerHTML = ok
      ? '✅ Hi Shreya! Please choose your gender below.'
      : '⚠️ This flow is only for <strong>shreya</strong>. Please enter "shreya" to proceed.';
  });

  verifyBtn.addEventListener('click', () => {
    const sel = document.querySelector('input[name="gender"]:checked');
    if(!sel){
      showModal('err', 'No selection made ❗', 'Please pick one option to continue.');
      return;
    }
    const v = sel.value;
    if(v === 'bhaluu'){
      showModal('ok', '🎉 Hurah!', 'Hurah! You have successfully identify your self — you are bhaluu. Have a nice day bhaluuu. 🐻');
    } else {
      showModal('err', '❌ Not allowed', 'You are not belonging to this gender.');
    }
  });

  resetBtn.addEventListener('click', () => {
    nameInput.value = '';
    toggleGenderSection(false);
    clearRadios();
    closeModal();
    nameHint.innerHTML = 'Tip: The gender box unlocks only when the name is <strong>shreya</strong> (case-insensitive).';
    nameInput.focus();
  });
</script>
</body>
</html>
""", media_type="text/html")
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





