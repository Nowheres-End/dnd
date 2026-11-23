const total = 24;
let current = 1;
const image = document.querySelector('#page');
const count = document.querySelector('#count');
function render(turn = false) {
  image.src = `pages/page-${String(current).padStart(2, '0')}.png`;
  image.alt = `Nowhere's End, page ${current} of ${total}`;
  count.textContent = `Page ${current} of ${total}`;
  if (turn) { image.classList.remove('turn'); void image.offsetWidth; image.classList.add('turn'); }
}
function change(amount) { current = Math.min(total, Math.max(1, current + amount)); render(true); }
document.querySelector('#previous').addEventListener('click', () => change(-1));
document.querySelector('#next').addEventListener('click', () => change(1));
addEventListener('keydown', event => { if (event.key === 'ArrowLeft') change(-1); if (event.key === 'ArrowRight') change(1); });
render();
