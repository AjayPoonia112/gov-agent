import os
from flask import Flask, Response

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Happy Birthday Shreya 🎂</title>

<style>
body{
  margin:0;
  font-family: system-ui, Arial;
  color:white;
  text-align:center;
  background: linear-gradient(135deg,#ff6ec7,#7366ff);
  overflow:hidden;
}

/* Center container */
.container{
  height:100vh;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:20px;
}

/* Card */
.card{
  background: rgba(255,255,255,0.1);
  padding:30px;
  border-radius:20px;
  backdrop-filter: blur(10px);
  box-shadow:0 10px 30px rgba(0,0,0,0.3);
}

/* Button */
button{
  padding:14px 22px;
  border:none;
  border-radius:12px;
  font-size:16px;
  font-weight:bold;
  cursor:pointer;
  color:white;
  background:linear-gradient(90deg,#ff4081,#7c4dff);
}

button:hover{
  transform: scale(1.05);
}

/* Hidden message */
.message{
  display:none;
  margin-top:20px;
  animation:fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn{
  from{opacity:0; transform:translateY(15px);}
  to{opacity:1;}
}

/* Floating emojis */
.float{
  position:fixed;
  top:-20px;
  animation:fall linear forwards;
}

@keyframes fall{
  to{
    transform:translateY(110vh);
    opacity:0;
  }
}

/* Heading glow */
.glow{
  font-size:2rem;
  font-weight:800;
  animation:glow 1.5s infinite alternate;
}

@keyframes glow{
  from{ text-shadow:0 0 10px #fff;}
  to{ text-shadow:0 0 25px #ffd700;}
}
</style>
</head>

<body>

<div class="container">

  <div class="card">
    <h1>🎂 Celebrate Shreya's Birthday 🎉</h1>
    
    <button id="btn">Click to Reveal Surprise 🎁</button>

    <div id="msg" class="message">
      <h2 class="glow">🎉 Happy Birthday Shreya Gupta 🎂</h2>
      <p>
        May this beautiful day bring you endless joy, success, and happiness 🌸✨<br><br>
        May all your dreams come true, and your life be filled with love, laughter, and positivity 💖<br><br>
      </p>

      <p>
        🎂 Stay blessed <br>
        🎈 Keep smiling <br>
        🎁 Shine always  
      </p>

      <div style="font-size:2rem;margin-top:10px;">
        🎉 🎂 🎈 🎁 🌸 💫
      </div>
    </div>

    <br>
    <button id="party">Celebrate More 🎊</button>
  </div>

</div>

<script>
const btn = document.getElementById("btn");
const msg = document.getElementById("msg");
const party = document.getElementById("party");

// Floating emojis (confetti)
function launch(count=60){
  const emojis = ["🎉","🎂","🎈","🌸","✨","🎁","💖","🌟"];
  for(let i=0;i<count;i++){
    const e = document.createElement("div");
    e.className="float";
    e.innerText = emojis[Math.floor(Math.random()*emojis.length)];
    e.style.left = Math.random()*100 + "vw";
    e.style.fontSize = (16 + Math.random()*20) + "px";
    e.style.animationDuration = (2+Math.random()*3)+"s";
    document.body.appendChild(e);
    setTimeout(()=>e.remove(),4000);
  }
}

// Reveal Birthday message
btn.onclick = ()=>{
  if(msg.style.display==="block"){
    msg.style.display="none";
    btn.innerText="Click to Reveal Surprise 🎁";
  }else{
    msg.style.display="block";
    btn.innerText="Hide Message ✖️";
    launch(80);
  }
};

// Extra celebration
party.onclick = ()=> launch(120);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return Response(HTML, mimetype="text/html")

@app.route("/healthz")
def healthz():
    return {"status":"ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
