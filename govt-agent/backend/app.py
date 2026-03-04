import os
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Happy Holi, Bhaluu! 🐻🌈</title>

  <!-- Inline Styles (Holi theme, animations, UI) -->
  <style>
    :root{
      --bg1: #0f1024;        /* deep night blue */
      --bg2: #24114a;        /* royal purple */
      --bg3: #52114f;        /* magenta */
      --text: #eef1ff;
      --muted: #aab1d6;
      --primary: #ff7ee2;    /* pink */
      --accent:  #7c5cff;    /* violet */
      --lime:    #3df29e;
      --gold:    #ffd166;
      --danger:  #ff5c8a;
      --ok:      #28c76f;
    }
    *{box-sizing:border-box}
    html, body { height: 100%; }
    body{
      margin:0; min-height:100vh;
      color:var(--text);
      font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      display:flex; align-items:center; justify-content:center; padding:24px;
      background:
        radial-gradient(1200px 600px at -10% -10%, #ff5c8a22, transparent 60%),
        radial-gradient(1200px 600px at 110% 10%, #7c5cff22, transparent 60%),
        linear-gradient(120deg, var(--bg1), var(--bg2), var(--bg3));
      background-size: 200% 200%;
      animation: holoShift 12s ease-in-out infinite alternate;
      overflow-x:hidden;
    }
    @keyframes holoShift{
      0%{background-position:0% 0%}
      100%{background-position:100% 100%}
    }
    .holi-powder{
      position:fixed; inset:0; pointer-events:none; mix-blend-mode:screen; opacity:.6;
      background:
        radial-gradient(600px 260px at 10% 15%, rgba(255,94,0,.25), transparent 60%),
        radial-gradient(500px 220px at 90% 10%, rgba(0,255,204,.25), transparent 60%),
        radial-gradient(600px 280px at 10% 90%, rgba(255,0,200,.25), transparent 60%),
        radial-gradient(600px 280px at 90% 85%, rgba(0,150,255,.25), transparent 60%);
      animation: slowFloat 10s ease-in-out infinite alternate;
    }
    @keyframes slowFloat{
      0%{transform:translateY(0)}
      100%{transform:translateY(-14px)}
    }
    .container{ width:100%; max-width:980px; }
    .header{ text-align:center; margin-bottom:20px }
    .header h1{ margin:0 0 8px; font-weight:800; letter-spacing:.4px }
    .tagline{ margin:0; color:var(--muted) }

    .grid{
      display:grid; gap:16px;
      grid-template-columns: 1fr;
    }
    @media (min-width: 860px){
      .grid{ grid-template-columns: 1.2fr .8fr; }
    }

    .card{
      background: linear-gradient(180deg, #1a1f4aAA, #131736AA);
      backdrop-filter: blur(10px);
      border:1px solid #ffffff2a;
      border-radius:18px;
      padding:22px;
      box-shadow: 0 16px 50px #00000066;
    }
    .card h2{ margin-top:0 }

    .label{ display:block; margin-bottom:8px; font-weight:700; }
    .input-row{ display:flex; gap:10px; }
    input[type=text]{
      flex:1;
      background:#0f1233; border:1px solid #ffffff2a;
      color:var(--text); padding:12px 14px; border-radius:12px; outline:none;
      transition:border .2s, box-shadow .2s;
    }
    input[type=text]:focus{
      border-color:var(--accent);
      box-shadow:0 0 0 3px #7c5cff33;
    }
    .btn{
      border:0; border-radius:12px; padding:12px 16px; cursor:pointer; font-weight:800;
      display:inline-flex; align-items:center; gap:8px;
      background:linear-gradient(90deg, var(--primary), var(--accent));
      color:#fff; box-shadow:0 8px 24px #00000055; transition:transform .06s;
    }
    .btn:active{ transform: translateY(1px) }
    .btn.ghost{
      background: transparent; border:1.5px solid #ffffff33; color:#fff;
    }
    .select{
      width:100%; padding:12px 14px; border-radius:12px;
      background:#0f1233; border:1px solid #ffffff2a; color:var(--text);
    }

    .hidden{ display:none }
    .message{ min-height:28px; margin-top:12px; }
    .message.error{ color:var(--danger) }
    .message.ok{ color:var(--ok) }

    /* Waving hand */
    .wave{ display:inline-block; animation: wave 2.2s infinite }
    @keyframes wave{
      0%{transform:rotate(0)}
      20%{transform:rotate(16deg)}
      40%{transform:rotate(-8deg)}
      60%{transform:rotate(14deg)}
      80%{transform:rotate(-4deg)}
      100%{transform:rotate(0)}
    }

    /* Modal */
    .modal{ position:fixed; inset:0; background:#0008; display:grid; place-items:center;
            opacity:0; pointer-events:none; transition:opacity .25s }
    .modal.show{ opacity:1; pointer-events:auto }
    .modal-content{
      position:relative; background:#101437; border:1px solid #ffffff2a;
      border-radius:16px; padding:24px; width:min(560px, 92%); text-align:center;
      transform:scale(.92); animation: pop .25s cubic-bezier(.2,.7,.2,1) forwards
    }
    .modal-close{
      position:absolute; top:12px; right:12px; background:transparent; border:0; color:#fff;
      font-size:20px; cursor:pointer
    }
    @keyframes pop{ to{ transform:scale(1)} }

    /* Confetti */
    .confetti{ position:fixed; inset:0; pointer-events:none; overflow:hidden }
    .confetti .piece{ position:absolute; top:-20px; font-size:22px; animation:fall linear forwards }
    @keyframes fall{ to{ transform:translateY(110vh) rotate(360deg); opacity:0 } }

    /* Blessing box */
    .bless{
      display:none; margin-top:14px; padding:14px; border-radius:14px;
      border:1px dashed #ffffff44; background: #ffffff0d;
      animation: rise .35s ease-out both;
    }
    @keyframes rise{ from{ opacity:0; transform: translateY(8px) } to{ opacity:1; transform:none } }

    /* Sparkle floating emoji */
    .sparkle{
      position:fixed; right:14px; bottom:18px; font-size:32px; opacity:.7;
      animation: drift 7s ease-in-out infinite;
    }
    @keyframes drift{
      0%{ transform: translateY(0) rotate(0) }
      50%{ transform: translateY(-10px) rotate(12deg) }
      100%{ transform: translateY(0) rotate(0) }
    }

    .muted{ color:var(--muted) }
    .footer{ color:var(--muted); text-align:center; margin-top:12px }
    .chip{
      display:inline-flex; align-items:center; gap:8px; padding:8px 12px;
      border-radius:999px; background:#ffffff1a; border:1px solid #ffffff2a;
    }
  </style>
</head>
<body>
  <div class="holi-powder"></div>
  <div class="sparkle" aria-hidden="true">✨</div>

  <div class="container">
    <header class="header">
      <h1>🌈 Happy Holi, <span class="chip">Bhaluu 🐻 <span class="wave">👋</span></span></h1>
      <p class="tagline">Colours, laughter, and blessings—let joy splash everywhere today!</p>
    </header>

    <div class="grid">
      <!-- Left: App -->
      <main class="card">
        <h2>Identity Checker</h2>
        <label for="name" class="label">Your name</label>
        <div class="input-row">
          <input id="name" type="text" placeholder="e.g., Shreya" autocomplete="name" />
          <button id="startBtn" class="btn" aria-label="Start">
            <span>Start</span> ▶️
          </button>
        </div>

        <section id="genderSection" class="hidden" aria-live="polite">
          <label for="gender" class="label">Choose your gender <span>✨</span></label>
          <select id="gender" class="select">
            <option value="" selected disabled>-- Select one --</option>
            <option value="female">Female ♀️</option>
            <option value="male">Male ♂️</option>
            <option value="angel">Angel 😇</option>
            <option value="bhaluu" class="only-shreya">Bhaluu 🐻</option>
          </select>
        </section>

        <div id="message" class="message" role="status" aria-live="polite"></div>

        <hr style="border:0;border-top:1px solid #ffffff22;margin:18px 0">

        <h3>🎁 Blessings for Holi</h3>
        <button id="blessBtn" class="btn ghost">Click here</button>
        <div id="blessBox" class="bless">
          <p style="margin:0 0 8px">
            <strong>Holi Blessing:</strong> May your days burst with colours of courage, calm and kindness—every shade bringing you closer to your happiest self. 🌸🌼
          </p>
          <p style="margin:0">
            <em>Life-Affirming Wish:</em> May you receive everything you truly wish for in life—at the right time, in the right way, with the right heart. 🌟
          </p>
        </div>
      </main>

      <!-- Right: Channel -->
      <section class="card">
        <h2>🎬 Channel</h2>
        <p>Watch our featured Short and show some love! 💖</p>
        <div class="video-wrapper" style="border-radius:12px;border:1px solid #ffffff22">
          <iframe
            title="YouTube Short"
            src="https://www.youtube.com/embed/0yGxtEFgO5g"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope;      </section>
    </div>

    <footer class="footer">Made with 💙, colours, and tiny animations. Happy Holi! 🎉</footer>
  </div>

  <!-- Success Modal -->
  <div id="successModal" class="modal" aria-hidden="true" role="dialog" aria-labelledby="modalTitle" aria-modal="true">
    <div class="modal-content">
      <button class="modal-close" id="closeModal" aria-label="Close">✖️</button>
      <h3 id="modalTitle">🎉 Hurah! 🎉</h3>
      <p>Hurah you have successfully identify your self — you are <strong>BHALUU 🐻</strong>!</p>
      <p>Have a nice day bhaluuu! 🌈✨</p>
    </div>
  </div>

  <!-- Confetti Container -->
  <div id="confetti" class="confetti" aria-hidden="true"></div>

  <!-- Inline Script -->
  <script>
    // Element refs
    const nameInputEl = document.getElementById('name');
    const startBtn = document.getElementById('startBtn');
    const genderSection = document.getElementById('genderSection');
    const genderSelect = document.getElementById('gender');
    const message = document.getElementById('message');
    const successModal = document.getElementById('successModal');
    const closeModal = document.getElementById('closeModal');
    const confettiRoot = document.getElementById('confetti');

    const blessBtn = document.getElementById('blessBtn');
    const blessBox = document.getElementById('blessBox');

    function isShreya(name){
      if(!name) return false;
      return name.trim().toLowerCase() === 'shreya';
    }

    function showGenderSection(show){
      genderSection.classList.toggle('hidden', !show);
      if(!show){
        genderSelect.value = '';
      }
    }

    function showError(text){
      message.textContent = text;
      message.classList.remove('ok');
      message.classList.add('error');
    }

    function clearMessage(){
      message.textContent = '';
      message.classList.remove('error','ok');
    }

    function spawnConfetti(){
      const emojis = ['🎉','✨','💫','🌟','🎊','🫧','🎈','🟡','🟣','🟢','🔵','🔴','🐻'];
      const count = 80;
      for(let i=0;i<count;i++){
        const span = document.createElement('span');
        span.className = 'piece';
        span.textContent = emojis[Math.floor(Math.random()*emojis.length)];
        span.style.left = Math.random()*100 + 'vw';
        span.style.animationDuration = (2 + Math.random()*1.8).toFixed(2) + 's';
        span.style.fontSize = (18 + Math.random()*10).toFixed(0) + 'px';
        confettiRoot.appendChild(span);
        setTimeout(()=> span.remove(), 4200);
      }
    }

    function openModal(){
      successModal.classList.add('show');
      successModal.setAttribute('aria-hidden','false');
      spawnConfetti();
    }

    function closeModalNow(){
      successModal.classList.remove('show');
      successModal.setAttribute('aria-hidden','true');
    }

    startBtn.addEventListener('click', ()=>{
      clearMessage();
      const name = nameInputEl.value;
      const sh = isShreya(name);

      // Toggle section
      showGenderSection(sh);

      // Bhaluu visible only for Shreya
      [...genderSelect.options].forEach(opt=>{
        if(opt.value === 'bhaluu'){
          opt.hidden = !sh;
        }
      });

      if(!sh){
        showError('Hi there! This flow is for Shreya only ✋');
      }
    });

    genderSelect.addEventListener('change', ()=>{
      clearMessage();
      const val = genderSelect.value;
      const name = nameInputEl.value.trim();
      if(isShreya(name)){
        if(val === 'bhaluu'){
          openModal();
        } else if(['male','female','angel'].includes(val)){
          showError('❌ Shreya, you are not belonging to this gender.');
        }
      }
    });

    closeModal.addEventListener('click', closeModalNow);
    successModal.addEventListener('click', (e)=>{ if(e.target === successModal) closeModalNow(); });

    // Enter to trigger start
    nameInputEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter'){ startBtn.click(); } });

    // Blessings button
    blessBtn.addEventListener('click', ()=>{
      blessBox.style.display = (blessBox.style.display === 'block') ? 'none' : 'block';
      if (blessBox.style.display === 'block') spawnConfetti();
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
