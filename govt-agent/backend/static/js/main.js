const nameInput = document.getElementById('name');
const startBtn = document.getElementById('startBtn');
const genderSection = document.getElementById('genderSection');
const genderSelect = document.getElementById('gender');
const message = document.getElementById('message');
const successModal = document.getElementById('successModal');
const closeModal = document.getElementById('closeModal');
const confettiRoot = document.getElementById('confetti');

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

startBtn.addEventListener('click', ()=>{
  clearMessage();
  const name = nameInput.value;
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
  const name = nameInput.value.trim();
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
nameInput.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter'){ startBtn.click(); }
});
``
