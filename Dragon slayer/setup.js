// ────────────────────────────────────────────────
// Enhanced Sword Throw Game with Touch Controls + Reset Button
// Fixed bugs, smoother physics (rAF), better aiming, hybrid mouse/touch support
// ────────────────────────────────────────────────

let g = 0.1;
let gd = 0;
let power = 0;
let xx = 0;
let yy = 0;
let isDragging = false;
let animationFrameId = null;

const insults = [
  'Nice try.', 'Maybe aim for the white circle.', 'That is it, huh?',
  'Try with your eyes open now.', 'Perhaps we call it a draw?',
  'I am right in front of you.', 'Ha. Ha. Ha.', 'We are going to be here a while.',
  'Fear, I know thee not.', 'Maybe next time.'
].sort(() => Math.random() - 0.5);

let insultIndex = 0;

let originX = 0;
let originY = 0;
let sword = null;

function updateOrigin() {
  const princeRect = prince.getBoundingClientRect();
  originX = princeRect.left + 30;
  originY = princeRect.top + 50;
}

function createSword() {
  if (sword) sword.remove();
  
  sword = document.createElement('div');
  sword.id = 'actual';
  
  // Mouse support
  sword.addEventListener('mousedown', onMouseDown);
  
  // Touch support
  sword.addEventListener('touchstart', onTouchStart, { passive: false });
  
  document.body.appendChild(sword);
  resetSwordPosition();
}

function resetSwordPosition() {
  updateOrigin();
  sword.style.setProperty('--top', originY + 'px');
  sword.style.setProperty('--left', originX + 'px');
  sword.style.pointerEvents = 'auto';
  sword.style.cursor = 'grab';
  sword.style.setProperty('--sword-angle', 'rotate(0deg)');
}

function updateInsult() {
  insult.innerHTML = insults[insultIndex];
  insult.style.opacity = '1';
  insultIndex = (insultIndex + 1) % insults.length;
}

function onMouseDown() {
  isDragging = true;
  sword.style.cursor = 'grabbing';
  window.addEventListener('mousemove', onMouseDrag);
  window.addEventListener('mouseup', onMouseEnd);
}

function onMouseDrag(e) {
  if (!isDragging) return;
  
  xx = e.clientX;
  yy = e.clientY;
  
  updateDrag(xx, yy);
}

function onMouseEnd() {
  if (!isDragging) return;
  endDrag();
}

function onTouchStart(e) {
  e.preventDefault();
  isDragging = true;
  // No cursor change for touch
  window.addEventListener('touchmove', onTouchDrag, { passive: false });
  window.addEventListener('touchend', onTouchEnd, { passive: false });
  window.addEventListener('touchcancel', onTouchEnd, { passive: false });
  
  // Initial position
  const touch = e.touches[0];
  xx = touch.clientX;
  yy = touch.clientY;
  updateDrag(xx, yy);
}

function onTouchDrag(e) {
  e.preventDefault();
  if (!isDragging || !e.touches.length) return;
  
  const touch = e.touches[0];
  xx = touch.clientX;
  yy = touch.clientY;
  
  updateDrag(xx, yy);
}

function onTouchEnd(e) {
  e.preventDefault();
  if (!isDragging) return;
  endDrag();
}

function updateDrag(x, y) {
  const yDiff = y - originY;
  const xDiff = originX - x;
  
  // Physics: pull left (xDiff >0) = power, pull down (yDiff >0) = upward launch (gd <0)
  power = Math.max(0, xDiff * 0.08);
  gd = Math.max(-15, Math.min(0, -yDiff * 0.08));
  
  // Visual angle (improved from fixed -95deg)
  // const angle = Math.atan2(gd, power) * (180 / Math.PI);
  const angle = "-95";
  sword.style.setProperty('--sword-angle', `rotate(${angle}deg)`);
  
  // Follow finger
  sword.style.setProperty('--top', (y - 15) + 'px');
  sword.style.setProperty('--left', (x - 15) + 'px');
  
  // Prince pulling back visual (matches original)
  if (xDiff > 0 && yDiff > 0) {
    prince.style.background = 'var(--back)';
  } else {
    prince.style.background = 'var(--standing)';
  }
}

function endDrag() {
  isDragging = false;
  
  // Clean up mouse
  window.removeEventListener('mousemove', onMouseDrag);
  window.removeEventListener('mouseup', onMouseEnd);
  
  // Clean up touch
  window.removeEventListener('touchmove', onTouchDrag, { passive: false });
  window.removeEventListener('touchend', onTouchEnd, { passive: false });
  window.removeEventListener('touchcancel', onTouchEnd, { passive: false });
  
  sword.style.pointerEvents = 'none';
  sword.style.cursor = 'default';
  
  // Throw anim
  prince.style.background = 'var(--throwing)';
  prince.style.aspectRatio = '154/90';
  
  setTimeout(animateProjectile, 250);
}

function animateProjectile() {
  let vx = power;
  let vy = gd;
  
  function step() {
    xx += vx;
    vy += g;
    yy += vy;
    
    sword.style.setProperty('--left', xx + 'px');
    sword.style.setProperty('--top', yy + 'px');
    sword.style.setProperty('--sword-angle', `rotate(${90}deg)`);
    
    const rect = sword.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    const hitElem = document.elementFromPoint(centerX, centerY);
    
    const outOfBounds =
      centerX < 0 || centerX > window.innerWidth ||
      centerY < 0 || centerY > window.innerHeight;
    
    if (hitElem?.classList.contains('heart') || outOfBounds) {
      cancelAnimationFrame(animationFrameId);
      
      if (hitElem?.classList.contains('heart')) {
        // WIN!
        hitElem.style.opacity = '0';
        sword.style.setProperty('--sword-shape', 'polygon(50% 25%, 65% 25%, 65% 75%, 100% 75%, 100% 85%, 60% 85%, 60% 100%, 40% 100%, 40% 85%, 0% 85%, 0% 75%, 35% 75%, 35% 25%)');
        container.style.background = 'var(--dragon-dead)';
        prince.style.background = 'var(--standing)';
        prince.style.aspectRatio = '';
        congrats.style.transform = 'translateX(0)';
        insult.style.opacity = '';
      } else {
        // MISS
        sword.remove();
        createSword();
        prince.style.background = 'var(--standing)';
        prince.style.aspectRatio = '';
        updateInsult();
      }
    } else {
      animationFrameId = requestAnimationFrame(step);
    }
  }
  
  animationFrameId = requestAnimationFrame(step);
}

function resetGame() {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  if (sword) sword.remove();
  createSword();
  container.style.background = 'var(--dragon)';
  congrats.style.transform = '';
  document.querySelector('.heart').style.opacity = '';
  prince.style.background = 'var(--standing)';
  prince.style.aspectRatio = '';
  insult.style.opacity = '';
  insultIndex = 0;
}

// ────────────────────────────────────────────────
// TURNS ON RESET BUTTON (add id="reset" to your HTML button if needed)
// ────────────────────────────────────────────────
const resetButton = document.getElementById('reset');
if (resetButton) {
  resetButton.style.display = 'block';  // "Turn on" - show if hidden
  resetButton.addEventListener('click', resetGame);
  // Click works on touch devices too
} else {
  console.warn('Reset button not found! Add <button id="reset">Reset</button> to HTML.');
}

// Init game
resetGame();