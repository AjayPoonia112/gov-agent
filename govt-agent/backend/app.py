import os
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#6c2bd9" />
  <title>Happy Holi, Ojaswini Mishra! 🐻🌈</title>

  <style>
    :root{
      --bg-a:#0f1024;--bg-b:#25115a;--bg-c:#6c2bd9;
      --ink:#eef1ff;--muted:#b8bfe5;--accent:#ff6ec7;--vio:#7c5cff;
      --ok:#21d49b;--warn:#ffb703;--danger:#ff5c8a;
      --glass: #131736aa;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0; color:var(--ink);
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background:
        radial-gradient(1400px 640px at -10% -10%, #ff5c8a26, transparent 60%),
        radial-gradient(1200px 560px at 110% 0%, #7c5cff26, transparent 60%),
        linear-gradient(120deg, var(--bg-a), var(--bg-b), var(--bg-c));
      background-size:200% 200%;
      animation:bgShift 14s ease-in-out infinite alternate;
      display:flex; align-items:center; justify-content:center;
      padding:clamp(16px,3vw,24px);
      -webkit-tap-highlight-color: transparent;
    }
    @keyframes bgShift{0%{background-position:0% 0%}100%{background-position:100% 100%}}

    /* “Gulal” mist */
    .powder{
      position:fixed; inset:0; pointer-events:none; mix-blend-mode:screen; opacity:.55;
      background:
        radial-gradient(520px 220px at 12% 12%, rgba(255,110,199,.20), transparent 60%),
        radial-gradient(520px 240px at 85% 10%, rgba(0,255,204,.18), transparent 60%),
        radial-gradient(620px 260px at 12% 88%, rgba(255,190,0,.18), transparent 60%),
        radial-gradient(560px 260px at 88% 88%, rgba(120,160,255,.18), transparent 60%);
      animation:floaty 10s ease-in-out infinite alternate;
    }
    @keyframes floaty{0%{transform:translateY(0)}100%{transform:translateY(-14px)}}

    .wrap{width:min(920px, 100%); margin:auto}
    header{ text-align:center; margin-bottom:12px }
    h1{ margin:.25rem 0 .5rem; font-weight:800; font-size:clamp(1.4rem,4.8vw,2.2rem) }
    .tag{ color:var(--muted); margin:0 .5rem }
    .chip{ display:inline-flex; align-items:center; gap:.5rem; padding:.4rem .8rem;
      border-radius:999px; border:1px solid #ffffff2a; background:#ffffff14 }

    .card{
      background:linear-gradient(180deg, #1a1f4aAA, var(--glass));
      backdrop-filter: blur(10px);
      border:1px solid #ffffff24; border-radius:16px;
      padding:clamp(14px,3.2vw,22px); box-shadow:0 14px 38px #0008;
    }

    .stack{ display:grid; gap:clamp(12px,2.6vw,16px) }

    .btn{
      appearance:none; border:0; border-radius:14px; cursor:pointer;
      padding:clamp(12px,3vw,14px) clamp(16px,4.2vw,18px);
      font-weight:800; color:white; width:100%;
      background:linear-gradient(90deg, var(--accent), var(--vio));
      box-shadow:0 10px 24px #0007;
      display:inline-flex; align-items:center; justify-content:center; gap:.6rem;
      transition:transform .06s;
      touch-action:manipulation;
    }
    .btn:active{ transform:translateY(1px) }
    .btn.secondary{
      background:transparent; border:1.6px solid #ffffff33;
    }

    .bless{
      display:none; border-radius:14px; border:1px dashed #ffffff3a;
      background:#ffffff10; padding:clamp(12px,3vw,16px);
      animation:rise .28s ease-out both;
    }
    @keyframes rise{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}

    .bless h2{margin:.2rem 0 .4rem; font-size:clamp(1.05rem,3.8vw,1.2rem)}
    .bless p{margin:.35rem 0; line-height:1.5}
    .muted{ color:var(--muted) }
    footer{ text-align:center; color:var(--muted); margin-top:10px; font-size:.95rem }

    /* Confetti */
    .confetti{ position:fixed; inset:0; pointer-events:none; overflow:hidden }
    .piece{ position:absolute; top:-24px; animation:fall linear forwards }
    @keyframes fall{ to{ transform:translateY(110vh) rotate(360deg); opacity:0 } }

    /* Mobile niceties */
    .pad{ padding:clamp(10px,3.2vw,14px) }
    .spacer{ height:10px }

    /* Reduced motion */
    @media (prefers-reduced-motion: reduce){
      body{ animation:none }
      .powder{ animation:none }
      .piece{ animation-duration: 0s !important }
    }
  </style>
</head>
<body>
  <div class="powder" aria-hidden="true"></div>

  <div class="wrap pad">
    <header>
      <h1>🌈 Happy Holi, <span class="chip">Ojaswini Mishra 🐻</span></h1>
      <p class="tag">Colours, laughter, and blessings—let joy splash everywhere today!</p>
    </header>

    <main class="card stack" role="main">
      <div class="stack">
        <button id="blessBtn" class="btn" aria-expanded="false" aria-controls="blessCard">
          <span>Click here for your Holi blessing</span> 🎁
        </button>

        <section id="blessCard" class="bless" role="region" aria-live="polite">
          <h2>💖 Blessing for You</h2>
          <p>
            May your days burst with the colours of courage, calm, and kindness, and may every shade lead you toward deeper joy and gentle victories. ✨
          </p>
          <p><em>Holi Wish:</em> May you get everything you truly want in life — at the right time, in the right way, with the right heart. 🌟</p>
          <p class="muted">— With love and light, Happy Holi! 🎉</p>
        </section>

        <button id="colorsBtn" class="btn secondary">
          Play colours 🌸🌼
        </button>
      </div>
    </main>

    <div class="spacer"></div>
    <footer>Made with 💙, colours, and tiny animations. Happy Holi! 🎉</footer>
  </div>

  <div id="confetti" class="confetti" aria-hidden="true"></div>

  <script>
    // Elements
    const blessBtn   = document.getElementById('blessBtn');
    const blessCard  = document.getElementById('blessCard');
    const colorsBtn  = document.getElementById('colorsBtn');
    const confettiEl = document.getElementById('confetti');

    // Helpers
    function spawnConfetti(burst=70){
      const emojis = ['🎉','✨','🎊','🌸','🌼','🟡','🟣','🟢','🔵','🔴','🫧','🎈'];
      for(let i=0;i<burst;i++){
        const s = document.createElement('span');
        s.className = 'piece';
        s.textContent = emojis[(Math.random()*emojis.length)|0];
        s.style.left = (Math.random()*100)+'vw';
        s.style.fontSize = (16 + Math.random()*14).toFixed(0)+'px';
        s.style.animationDuration = (2 + Math.random()*2).toFixed(2)+'s';
        confettiEl.appendChild(s);
        setTimeout(()=>s.remove(), 4500);
      }
    }

    // Toggle blessing card
    blessBtn.addEventListener('click', ()=>{
      const showing = blessCard.style.display === 'block';
      if(showing){
        blessCard.style.display = 'none';
        blessBtn.setAttribute('aria-expanded','false');
        blessBtn.innerHTML = '<span>Click here for your Holi blessing</span> 🎁';
      }else{
        blessCard.style.display = 'block';
        blessBtn.setAttribute('aria-expanded','true');
        blessBtn.innerHTML = '<span>Hide blessing</span> ✖️';
        spawnConfetti(60);
      }
    });

    // Extra colours on tap
    colorsBtn.addEventListener('click', ()=> spawnConfetti(80));

    // Make the blessing discoverable on Enter as well
    blessBtn.addEventListener('keydown', (e)=>{
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault(); blessBtn.click();
      }
    });
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html; charset=utf-8")

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

