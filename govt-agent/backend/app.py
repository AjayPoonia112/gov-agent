import os
from flask import Flask, Response

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>I'm Sorry, My Panda 🐼</title>

<style>
body{
  margin:0;
  font-family: 'Segoe UI', system-ui, Arial;
  color:white;
  text-align:center;
  background: linear-gradient(135deg,#2c3e50,#4a69bd,#6a89cc);
  background-size: 400% 400%;
  animation: gradientShift 10s ease infinite;
  overflow-x:hidden;
  min-height:100vh;
}

@keyframes gradientShift{
  0%{background-position:0% 50%;}
  50%{background-position:100% 50%;}
  100%{background-position:0% 50%;}
}

.container{
  min-height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:20px;
  gap:20px;
}

.card{
  background: rgba(255,255,255,0.12);
  padding:40px 30px;
  border-radius:25px;
  backdrop-filter: blur(15px);
  box-shadow:0 15px 40px rgba(0,0,0,0.4);
  max-width:600px;
  width:90%;
  border:1px solid rgba(255,255,255,0.2);
}

h1{
  font-size:2.2rem;
  margin-bottom:10px;
}

.panda{
  font-size:5rem;
  animation: bounce 2s infinite;
  display:inline-block;
}

@keyframes bounce{
  0%,100%{transform:translateY(0);}
  50%{transform:translateY(-15px);}
}

button{
  padding:14px 24px;
  border:none;
  border-radius:12px;
  font-size:16px;
  font-weight:bold;
  cursor:pointer;
  color:white;
  background:linear-gradient(90deg,#ff6b9d,#c06eff);
  transition: all 0.3s;
  margin:8px;
  box-shadow:0 4px 15px rgba(0,0,0,0.2);
}

button:hover{
  transform: scale(1.08);
  box-shadow:0 6px 20px rgba(0,0,0,0.3);
}

.no-btn{
  background:linear-gradient(90deg,#666,#888);
  position:relative;
  transition: all 0.2s;
}

.step{
  display:none;
  animation:fadeIn 0.6s ease-in-out;
}

.step.active{
  display:block;
}

@keyframes fadeIn{
  from{opacity:0; transform:translateY(20px);}
  to{opacity:1; transform:translateY(0);}
}

.float{
  position:fixed;
  top:-30px;
  animation:fall linear forwards;
  pointer-events:none;
  z-index:10;
}

@keyframes fall{
  to{
    transform:translateY(110vh) rotate(360deg);
    opacity:0;
  }
}

.glow{
  font-size:1.8rem;
  font-weight:800;
  animation:glow 1.8s infinite alternate;
  margin:15px 0;
}

@keyframes glow{
  from{ text-shadow:0 0 10px #fff, 0 0 20px #ff6b9d;}
  to{ text-shadow:0 0 25px #fff, 0 0 40px #c06eff;}
}

.reason{
  background:rgba(255,255,255,0.1);
  padding:15px;
  border-radius:12px;
  margin:10px 0;
  border-left:4px solid #ff6b9d;
  text-align:left;
}

.progress{
  height:8px;
  background:rgba(255,255,255,0.2);
  border-radius:10px;
  overflow:hidden;
  margin:20px 0;
}

.progress-bar{
  height:100%;
  background:linear-gradient(90deg,#ff6b9d,#c06eff);
  width:0%;
  transition: width 0.6s ease;
}

.heart{
  display:inline-block;
  animation: heartbeat 1.2s infinite;
  color:#ff4d6d;
}

@keyframes heartbeat{
  0%,100%{transform:scale(1);}
  50%{transform:scale(1.2);}
}

p{
  line-height:1.7;
  font-size:1.05rem;
}
</style>
</head>

<body>

<div class="container">

  <div class="card">

    <!-- Step 1: Opening -->
    <div class="step active" id="step1">
      <div class="panda">🐼</div>
      <h1>Hey Panda...</h1>
      <p>I know I messed up, and I need a moment of your time.<br>Can I please talk to you? 🥺</p>
      <button onclick="nextStep(2)">Okay, I'm listening 💭</button>
    </div>

    <!-- Step 2: The Apology -->
    <div class="step" id="step2">
      <div class="panda">🐼💔</div>
      <h1 class="glow">I'm Truly Sorry, Shreya</h1>
      <p>My dearest Panda, I never wanted to hurt you. If my words or actions made you feel unloved, unheard, or upset — I am deeply, genuinely sorry. 💗</p>
      <button onclick="nextStep(3)">Why should I forgive you? 🤔</button>
    </div>

    <!-- Step 3: Reasons -->
    <div class="step" id="step3">
      <h1>Because... 💫</h1>
      <div class="reason">🐼 <b>You are my Panda</b> — cute, precious, and irreplaceable.</div>
      <div class="reason">💖 <b>You are the most important person in my life</b>, and nothing changes that.</div>
      <div class="reason">🌸 <b>You make my world brighter</b> just by being in it.</div>
      <div class="reason">✨ <b>I promise to do better</b> — to listen more, care more, and love you louder.</div>
      <div class="reason">🫂 <b>Losing you isn't an option</b>. You mean everything to me.</div>
      <button onclick="nextStep(4)">Continue... 💌</button>
    </div>

    <!-- Step 4: The Question -->
    <div class="step" id="step4">
      <div class="panda">🐼🌹</div>
      <h1 class="glow">Will you forgive me, my Panda?</h1>
      <p>I promise I'll make it up to you. Every single day. 💕</p>
      <div style="margin-top:20px;">
        <button onclick="forgive()">Yes, I forgive you 💗</button>
        <button class="no-btn" id="noBtn" onmouseover="runAway()" onclick="runAway()">No 😤</button>
      </div>
    </div>

    <!-- Step 5: Forgiven -->
    <div class="step" id="step5">
      <div class="panda" style="font-size:6rem;">🐼💖</div>
      <h1 class="glow">Thank you, my Panda 🥹</h1>
      <p>You are <b>the most important person</b> in my entire world, Shreya. <span class="heart">❤️</span></p>
      <p>You're my calm in every storm, my smile on every dull day, and my favorite person to exist. 🌸</p>
      <p><b>I love you more than words can ever explain.</b> 💗<br>Thank you for being you — my sweet, adorable Panda. 🐼</p>
      <div style="font-size:2rem;margin-top:15px;">🐼 💖 🌸 ✨ 🫧 💫 🌹</div>
      <button onclick="launch(150)">Shower You With Love 💗</button>
    </div>

    <div class="progress">
      <div class="progress-bar" id="progressBar"></div>
    </div>

  </div>

</div>

<script>
let currentStep = 1;
const totalSteps = 5;

function updateProgress(){
  const pct = (currentStep / totalSteps) * 100;
  document.getElementById("progressBar").style.width = pct + "%";
}

function nextStep(n){
  document.querySelectorAll(".step").forEach(s => s.classList.remove("active"));
  document.getElementById("step" + n).classList.add("active");
  currentStep = n;
  updateProgress();
  launch(30);
}

function forgive(){
  nextStep(5);
  launch(200);
  setTimeout(()=>launch(100), 800);
  setTimeout(()=>launch(100), 1600);
}

// Runaway "No" button
function runAway(){
  const btn = document.getElementById("noBtn");
  const maxX = window.innerWidth - 100;
  const maxY = window.innerHeight - 60;
  const x = Math.random() * maxX;
  const y = Math.random() * maxY;
  btn.style.position = "fixed";
  btn.style.left = x + "px";
  btn.style.top = y + "px";
}

// Floating emojis
function launch(count=60){
  const emojis = ["🐼","💖","🌸","✨","🌹","💗","🫧","💫","🎀"];
  for(let i=0;i<count;i++){
    const e = document.createElement("div");
    e.className="float";
    e.innerText = emojis[Math.floor(Math.random()*emojis.length)];
    e.style.left = Math.random()*100 + "vw";
    e.style.fontSize = (18 + Math.random()*24) + "px";
    e.style.animationDuration = (3+Math.random()*3)+"s";
    document.body.appendChild(e);
    setTimeout(()=>e.remove(),6000);
  }
}

updateProgress();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")

@app.route("/healthz")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
