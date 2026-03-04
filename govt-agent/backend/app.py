import os
from flask import Flask, Response

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#6c2bd9" />
  <title>Happy Holi, Everyone! 🌈 + Snake</title>

  <style>
    :root{
      --bg-a:#0f1024;--bg-b:#25115a;--bg-c:#6c2bd9;
      --ink:#eef1ff;--muted:#b8bfe5;--accent:#ff6ec7;--vio:#7c5cff;
      --ok:#21d49b;--warn:#ffb703;--danger:#ff5c8a;
      --glass:#131736aa; --line:#ffffff22;
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
      display:flex; align-items:flex-start; justify-content:center;
      padding:clamp(12px,3vw,22px);
      -webkit-tap-highlight-color: transparent;
    }
    @keyframes bgShift{0%{background-position:0% 0%}100%{background-position:100% 100%}}

    /* Gulal mist */
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

    .wrap{width:min(980px, 100%); margin:auto; display:grid; gap:clamp(12px,2.8vw,18px)}
    @media (min-width: 900px){
      .wrap{grid-template-columns: 1fr 1fr;}
    }

    header{ grid-column: 1/-1; text-align:center; margin-bottom:4px }
    h1{ margin:.25rem 0 .5rem; font-weight:800; font-size:clamp(1.3rem,4.6vw,2.3rem) }
    .tag{ color:var(--muted); margin:0 .5rem }
    .chip{ display:inline-flex; align-items:center; gap:.5rem; padding:.4rem .8rem;
      border-radius:999px; border:1px solid #ffffff2a; background:#ffffff14 }

    .card{
      background:linear-gradient(180deg, #1a1f4aAA, var(--glass));
      backdrop-filter: blur(10px);
      border:1px solid var(--line); border-radius:16px;
      padding:clamp(14px,3.2vw,22px); box-shadow:0 14px 38px #0008;
    }
    .stack{ display:grid; gap:clamp(12px,2.2vw,16px) }

    .btn{
      appearance:none; border:0; border-radius:14px; cursor:pointer;
      padding:clamp(12px,3vw,14px) clamp(16px,4.2vw,18px);
      font-weight:800; color:white; width:100%;
      background:linear-gradient(90deg, var(--accent), var(--vio));
      box-shadow:0 10px 24px #0007;
      display:inline-flex; align-items:center; justify-content:center; gap:.6rem;
      transition:transform .06s, filter .15s;
      touch-action:manipulation;
    }
    .btn:active{ transform:translateY(1px) }
    .btn.secondary{ background:transparent; border:1.6px solid #ffffff33; color:var(--ink) }
    .row{ display:flex; gap:10px; flex-wrap:wrap }
    .row > .btn{ flex:1 1 auto; min-width:140px }

    .bless{
      display:none; border-radius:14px; border:1px dashed #ffffff3a;
      background:#ffffff10; padding:clamp(12px,3vw,16px);
      animation:rise .28s ease-out both;
    }
    @keyframes rise{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
    .bless h2{margin:.2rem 0 .4rem; font-size:clamp(1.05rem,3.8vw,1.2rem)}
    .bless p{margin:.35rem 0; line-height:1.55}
    .muted{ color:var(--muted) }
    footer{ grid-column:1/-1; text-align:center; color:var(--muted); margin-top:8px; font-size:.95rem }

    /* Snake board */
    .board-wrap{
      display:grid; gap:12px; justify-items:center;
    }
    canvas#board{
      width: min(96vw, 480px);
      height: min(96vw, 480px);
      border-radius:14px; border:1px solid var(--line);
      background: #0b0f2d;
      touch-action:none; /* prevent pull-to-refresh on Android */
      box-shadow: inset 0 0 0 1px #ffffff10, 0 10px 28px #0008;
    }
    .score{ font-weight:800; }
    .tiny{ font-size:.9rem; color:var(--muted) }

    /* Confetti */
    .confetti{ position:fixed; inset:0; pointer-events:none; overflow:hidden }
    .piece{ position:absolute; top:-24px; animation:fall linear forwards; will-change: transform }
    @keyframes fall{ to{ transform:translateY(110vh) rotate(360deg); opacity:0 } }

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

  <div class="wrap">
    <header>
      <h1>🌈 Happy Holi, <span class="chip">Everyone </span></h1>
      <p class="tag">Colours, laughter, and blessings—let joy splash everywhere today!</p>
    </header>

    <!-- Holi Blessing -->
    <main class="card stack" role="main">
      <h2>💖 Holi Blessings</h2>
      <button id="blessBtn" class="btn" aria-expanded="false" aria-controls="blessCard">
        <span>Click here for your Holi blessing</span> 🎁
      </button>

      <section id="blessCard" class="bless" role="region" aria-live="polite">
        <h2>Blessing for You</h2>
        <p>May your days burst with the colours of courage, calm, and kindness—and may every shade lead you toward deeper joy and gentle victories. ✨</p>
        <p><em>Holi Wish:</em> May you get everything you truly want in life — at the right time, in the right way, with the right heart. 🌟</p>
        <p class="muted">— With love and light, Happy Holi! 🎉</p>
      </section>

      <div class="row">
        <button id="colorsBtn" class="btn secondary">Play colours 🌸🌼</button>
      </div>
    </main>

    <!-- Snake Game -->
    <section class="card stack" aria-label="Snake Game">
      <h2>🐍 Snake — Splash the Colours!</h2>
      <div class="board-wrap">
        <canvas id="board" width="480" height="480" aria-label="Snake game board"></canvas>
        <div class="row" style="width:100%;max-width:520px">
          <button id="startBtn" class="btn">Start ▶️</button>
          <button id="pauseBtn" class="btn secondary">Pause ⏸️</button>
          <button id="resetBtn" class="btn secondary">Reset 🔄</button>
        </div>
        <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap">
          <div class="score">Score: <span id="score">0</span></div>
          <div class="tiny">Use ⌨️ Arrow keys / WASD or swipe on mobile.</div>
        </div>
      </div>
    </section>

    <footer>Created by Ajay Poonia. Happy Holi! 🎉</footer>
  </div>

  <div id="confetti" class="confetti" aria-hidden="true"></div>

  <script>
    /* ---------- Confetti ---------- */
    const confettiEl = document.getElementById('confetti');
    function spawnConfetti(burst=70){
      const emojis = ['🎉','✨','🎊','🌸','🌼','🟡','🟣','🟢','🔵','🔴','🫧','🎈','🌈'];
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

    /* ---------- Blessing toggle ---------- */
    const blessBtn  = document.getElementById('blessBtn');
    const blessCard = document.getElementById('blessCard');
    const colorsBtn = document.getElementById('colorsBtn');

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
    colorsBtn.addEventListener('click', ()=> spawnConfetti(90));

    /* ---------- Snake Game ---------- */
    const board = document.getElementById('board');
    const ctx = board.getContext('2d');
    const scoreEl = document.getElementById('score');
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Responsive canvas (devicePixelRatio aware)
    function fitCanvas(){
      const cssSize = Math.min(window.innerWidth*0.96, 480, window.innerHeight*0.66);
      const dpr = window.devicePixelRatio || 1;
      board.style.width = cssSize + 'px';
      board.style.height = cssSize + 'px';
      board.width = Math.floor(cssSize * dpr);
      board.height = Math.floor(cssSize * dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
      cellSize = Math.floor(cssSize / cols);
    }

    // Grid and state
    const cols = 20, rows = 20;
    let cellSize = 24;
    let snake, dir, nextDir, food, running=false, loop=null, speed=140, score=0, touched=false;
    function initGame(){
      score = 0; scoreEl.textContent = '0';
      snake = [{x:10,y:10},{x:9,y:10},{x:8,y:10}];
      dir = {x:1,y:0}; nextDir = {x:1,y:0};
      placeFood();
      draw();
    }

    function placeFood(){
      while(true){
        const fx = (Math.random()*cols)|0;
        const fy = (Math.random()*rows)|0;
        if(!snake.some(s=>s.x===fx && s.y===fy)){ food = {x:fx,y:fy}; return; }
      }
    }

    function tick(){
      dir = nextDir;
      const head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};
      // Wall collision → game over
      if(head.x<0 || head.y<0 || head.x>=cols || head.y>=rows) return gameOver();
      // Self collision
      if(snake.some((s,i)=> i>0 && s.x===head.x && s.y===head.y)) return gameOver();

      snake.unshift(head);
      if(head.x===food.x && head.y===food.y){
        score++; scoreEl.textContent = String(score);
        spawnConfetti(35);
        placeFood();
        // slight speed-up
        if(speed>80 && score%3===0){
          speed -= 6;
          if(loop){ clearInterval(loop); loop = setInterval(step, speed); }
        }
      }else{
        snake.pop();
      }
      draw();
    }

    function draw(){
      // bg
      ctx.fillStyle = '#0b0f2d';
      ctx.fillRect(0,0,board.width,board.height);
      // grid (subtle)
      ctx.strokeStyle = 'rgba(255,255,255,.05)';
      ctx.lineWidth = 1;
      for(let i=1;i<cols;i++){
        ctx.beginPath(); ctx.moveTo(i*cellSize,0); ctx.lineTo(i*cellSize,rows*cellSize); ctx.stroke();
      }
      for(let j=1;j<rows;j++){
        ctx.beginPath(); ctx.moveTo(0,j*cellSize); ctx.lineTo(cols*cellSize,j*cellSize); ctx.stroke();
      }
      // food
      drawCell(food.x, food.y, '#ffd166'); // gold
      // snake
      snake.forEach((s,idx)=>{
        const color = idx===0 ? '#21d49b' : '#7c5cff';
        drawCell(s.x, s.y, color);
      });
    }

    function drawCell(x,y,color){
      ctx.fillStyle = color;
      const pad = Math.max(1, Math.floor(cellSize*0.12));
      ctx.fillRect(x*cellSize+pad, y*cellSize+pad, cellSize-2*pad, cellSize-2*pad);
    }

    function step(){ if(running) tick(); }

    function start(){
      if(running) return;
      running = true;
      loop = setInterval(step, speed);
    }
    function pause(){
      running = false;
    }
    function reset(){
      running = false;
      if(loop) clearInterval(loop);
      speed = 140;
      initGame();
    }
    function gameOver(){
      running = false;
      if(loop) clearInterval(loop);
      spawnConfetti(120);
      // overlay text
      ctx.fillStyle = 'rgba(0,0,0,.45)';
      ctx.fillRect(0,0,board.width,board.height);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 28px system-ui, -apple-system, Segoe UI, Roboto, Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Game Over', board.width/2, board.height/2 - 10);
      ctx.font = 'normal 16px system-ui, -apple-system, Segoe UI, Roboto, Arial';
      ctx.fillText('Tap Reset 🔄 to play again', board.width/2, board.height/2 + 18);
    }

    // Controls
    startBtn.addEventListener('click', start);
    pauseBtn.addEventListener('click', pause);
    resetBtn.addEventListener('click', reset);

    // Keyboard
    const keyDirs = {
      ArrowUp:{x:0,y:-1}, ArrowDown:{x:0,y:1}, ArrowLeft:{x:-1,y:0}, ArrowRight:{x:1,y:0},
      KeyW:{x:0,y:-1}, KeyS:{x:0,y:1}, KeyA:{x:-1,y:0}, KeyD:{x:1,y:0}
    };
    function opposite(a,b){ return a.x === -b.x && a.y === -b.y; }
    window.addEventListener('keydown',(e)=>{
      const nd = keyDirs[e.code];
      if(!nd) return;
      e.preventDefault();
      if(!opposite(nd, dir)) nextDir = nd;
    }, {passive:false});

    // Touch / swipe
    let ts = null;
    board.addEventListener('touchstart',(e)=>{ if(e.touches[0]) ts = {x:e.touches[0].clientX, y:e.touches[0].clientY}; }, {passive:true});
    board.addEventListener('touchend',(e)=>{
      if(!ts) return;
      const t = e.changedTouches[0]; if(!t) return;
      const dx = t.clientX - ts.x, dy = t.clientY - ts.y;
      const ax = Math.abs(dx), ay = Math.abs(dy);
      if(Math.max(ax,ay) < 18) return; // tiny moves ignored
      let nd;
      if(ax>ay) nd = dx>0 ? {x:1,y:0} : {x:-1,y:0};
      else      nd = dy>0 ? {x:0,y:1} : {x:0,y:-1};
      if(!opposite(nd, dir)) nextDir = nd;
      ts = null;
    }, {passive:true});

    // Resize handling & init
    window.addEventListener('resize', ()=>{ fitCanvas(); draw(); });
    fitCanvas(); initGame();
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


