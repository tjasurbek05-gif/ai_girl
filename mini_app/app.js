// mini_app/app.js – Telegram WebApp frontend
const tg = window.Telegram.WebApp;
let selectedStyle = null;
let selectedChar = null;
let characters = [];

// UI elements
const styleScreen = document.getElementById('style-screen');
const characterScreen = document.getElementById('character-screen');
const locationScreen = document.getElementById('location-screen');

function show(screen){
  [styleScreen, characterScreen, locationScreen].forEach(s=>s.classList.add('hidden'));
  screen.classList.remove('hidden');
}

// Load characters.json from repo (same origin)
async function loadCharacters(){
  const resp = await fetch('/characters/characters.json');
  if(!resp.ok) throw new Error('Failed to fetch characters');
  return await resp.json();
}

// Style selection
document.querySelectorAll('#style-screen .card').forEach(btn=>{
  btn.addEventListener('click', async()=>{
    selectedStyle = btn.dataset.style;
    characters = await loadCharacters();
    const filtered = characters.filter(c=>c.style===selectedStyle);
    const list = document.getElementById('character-list');
    list.innerHTML='';
    filtered.forEach(c=>{
      const b=document.createElement('button');
      b.className='card';
      b.dataset.id=c.id;
      b.innerHTML=`<img src="${c.avatar||'placeholder.png'}" alt="${c.name}"><span>${c.name}</span>`;
      b.addEventListener('click',()=>{selectedChar=c.id;show(locationScreen);});
      list.appendChild(b);
    });
    show(characterScreen);
  });
});

// Back buttons
document.querySelectorAll('.back').forEach(btn=>{
  btn.addEventListener('click',()=>show(styleScreen));
});

// Location selection → send payload back
document.querySelectorAll('#location-list .card').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const payload={character_id:selectedChar,style:selectedStyle,location:btn.dataset.location};
    tg.sendData(JSON.stringify(payload));
    tg.close();
  });
});

tg.ready();
