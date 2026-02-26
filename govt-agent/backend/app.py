import os
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Are you Bhaluu? 🐻</title>

  <style>
    :root{
      --bg: #0f1226;
      --card: #171a36;
      --text: #eef1ff;
      --muted: #aab1d6;
      --primary: #7c5cff;
      --danger: #ff5c8a;
      --success: #28c76f;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;min-height:100vh;background:
        radial-gradient(1000px 500px at 10% -30%, #3b2c8f22, transparent 60%),
        radial-gradient(800px 400px at 110% 130%, #ff5c8a22, transparent 60%),
        var(--bg);
      color:var(--text);
      font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      display:flex;align-items:center;justify-content:center;padding:24px;
    }
    .container{width:100%;max-width:860px}
    .header{text-align:center;margin-bottom:20px}
    .header h1{margin:0 0 6px;font-weight:700;letter-spacing:.3px}
    .tagline{margin:0;color:var(--muted)}
    .card{
      background:linear-gradient(180deg, #1a1f4aAA, #131736AA);
      backdrop-filter: blur(8px);
      border:1px solid #ffffff22;border-radius:16px;
      padding:20px;margin:12px 0;box-shadow:0 10px 40px #00000055
    }
    .label{display:block;margin-bottom:8px;font-weight:600}
    .input-row{display:flex;gap:10px}
    input[type=text]{
      flex:1;background:#0f1233;border:1px solid #ffffff22;color:var(--text);
      padding:12px 14px;border-radius:12px;outline:none;transition:border .2s
    }
    input[type=text]:focus{border-color:var(--primary)}
    .btn{border:0;border-radius:12px;padding:12px 16px;cursor:pointer;font-weight:700}
    .btn.primary{
      background:linear-gradient(90deg, #7c5cff, #3fbfff);
      color:#fff;box-shadow:0 6px 18px #7c5cff55;transition:transform .1s
    }
    .btn.primary:active{transform:translateY(1px)}
    .select{width:100%;padding:12px 14px;border-radius:12px;background:#0f1233;border:1px solid #ffffff22;color:var(--text)}
    .hidden{display:none}
    .message{min-height:28px;margin-top:12px}
    .message.error{color:var(--danger)}
    .message.ok{color:var(--success)}
    .wave{display:inline-block;animation:wave 2.2s infinite}
    @keyframes wave{
      0%{transform:rotate(0)}20%{transform:rotate(16deg)}40%{transform:rotate(-8deg)}
      60%{transform:rotate(14deg)}80%{transform:rotate(-4deg)}100%{transform:rotate(0)}
    }
    .bg-emoji{position:fixed;inset:auto -10px 20px auto;font-size:48px;animation:float 6s ease-in-out infinite;opacity:.35}
    @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
    .footer{color:var(--muted);text-align:center;margin-top:12px}
    /* Modal */
    .modal{position:fixed;inset:0;background:#0008;display:grid;place-items:center;opacity:0;pointer-events:none;transition:opacity .25s}
    .modal.show{opacity:1;pointer-events:auto}
    .modal-content{position:relative;background:#15183a;border:1px solid #ffffff22;border-radius:16px;padding:22px;max-width:520px;width:92%;text-align:center;transform:scale(.92);animation:pop .25s cubic-bezier(.2,.7,.2,1) forwards}
    .modal-close{position:absolute;top:14px;right:14px;background:transparent;border:0;color:#fff;font-size:20px;cursor:pointer}
    @keyframes pop{to{transform:scale(1)}}
    /* Video */
    .video-wrapper{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;border:1px solid #ffffff22}
    .video-wrapper iframe{position:absolute;top:0;left:0;width:100%;height:100%}
    /* Confetti */
    .confetti{position:fixed;inset:0;pointer-events:none;overflow:hidden}
    .confetti .piece{position:absolute;top:-20px;font-size:22px;animation:fall linear forwards}
    @keyframes fall{to{transform:translateY(110vh) rotate(360deg);opacity:0}}
    .muted{color:var(--muted)}
  </style>

  <!-- Google Fonts -->
  https://fonts.googleapis.com
  https://fonts.gstatic.com
  <link
    href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap"
    relass="bg-emoji" aria-hidden="true">✨</div>
  <div class="container">
    <header class="header">
      <h1>Identity Checker <span class="wave">👋</span></h1>
      <p class="tagline">Type your name to continue. Special flow for <strong>Shreya</strong> only. 💫</p>
    </header>

    <main class="card">
      <label for="name" class="label">Your name</label>
      <div class="input-row">
        <input id="name" type="text" placeholder="e.g., Shreya" autocomplete="name" />
        <button id="startBtn" class="btn primary" aria-label="Start">Start ▶️</button>
      </div>

      <section id="genderSection" class="hidden" aria-live="polite">
        <label for="gender" class="label">Choose your gender <span class="spark">✨</span></label>
        <select id="gender" class="select">
          <option value="" selected disabled>-- Select one --</option>
          <option value="female">Female ♀️</option>
          <option value="male">Male ♂️</option>
          <option value="angel">Angel 😇</option>
          <option value="bhaluu" class="only-shreya">Bhaluu 🐻</option>
        </select>
      </section>

      <div id="message" class="message" role="status" aria-live="polite"></div>
    </main>

    <section class="channel card">
      <h2>🎬 Channel</h2>
      <p>Watch our featured Short and show some love! 💖</p>
      <div class="video-wrapper">
        https://www.youtube.com/embed/0yGxtEFgO5g
        </iframe>
      </div>
      <p class="muted">Source:
        <a href="ww.youtube.com/shorts/0yGxtEFgO5gYouTube Short</a>
      </p>
    </section>

    <footer class="footer">Made with 💙, emojis, and tiny animations.</footer>
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

  <script>
    // --- JS Logic ---

    const nameInput = null; // will be set on DOMContentLoaded
    let startBtn, genderSection, genderSelect, message, successModal, closeModal, confettiRoot;

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
      const emojis = ['🎉','✨','💫','🌟','🎊','🐻'];
      const count = 60;
      for(let i=0;i<count;i++){
        const span = document.createElement('span');
        span.className = 'piece';
        span.textContent = emojis[Math.floor(Math.random()*emojis.length)];
        span.style.left = Math.random()*100 + 'vw';
        span.style.animationDuration = (2 + Math.random()*1.5).toFixed(2) + 's';
        confettiRoot.appendChild(span);
        setTimeout(()=> span.remove(), 3500);
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

    document.addEventListener('DOMContentLoaded', () => {
      const _name = document.getElementById('name');
      startBtn = document.getElementById('startBtn');
      genderSection = document.getElementById('genderSection');
      genderSelect = document.getElementById('gender');
      message = document.getElementById('message');
      successModal = document.getElementById('successModal');
      closeModal = document.getElementById('closeModal');
      confettiRoot = document.getElementById('confetti');

      startBtn.addEventListener('click', ()=>{
        clearMessage();
        const name = _name.value;
        const sh = isShreya(name);
        showGenderSection(sh);
        // Ensure Bhaluu option only visible for Shreya
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
        const name = _name.value.trim();
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

      // Allow Enter key to trigger start
      _name.addEventListener('keydown', (e)=>{
        if(e.key === 'Enter'){ startBtn.click(); }
      });
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    # Serve the inline HTML directly
    return Response(HTML, mimetype="text/html")

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    # Local run
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
