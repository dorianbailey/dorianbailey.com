// Photography: opens a plate full size, with previous/next (buttons, arrow keys
// or swipe) within its collection. Neighbouring plates are preloaded.
(function () {
  var dialog = document.getElementById('lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var img = dialog.querySelector('img');
  var cap = dialog.querySelector('figcaption');
  var list = [];
  var index = 0;
  var opener = null;
  var cache = {};

  document.querySelectorAll('.gallery').forEach(function (gallery) {
    var buttons = Array.prototype.slice.call(gallery.querySelectorAll('button.frame'));
    buttons.forEach(function (btn, i) {
      btn.addEventListener('click', function () {
        list = buttons; index = i; opener = btn;
        show();
        dialog.showModal();
      });
    });
  });

  function preload(i) {
    var b = list[(i + list.length) % list.length];
    var src = b && b.getAttribute('data-full');
    if (src && !cache[src]) { cache[src] = new Image(); cache[src].src = src; }
  }

  function show() {
    var btn = list[index];
    var src = btn.getAttribute('data-full');
    img.classList.add('is-loading');
    img.onload = function () { img.classList.remove('is-loading'); };
    img.src = src;
    if (img.complete) img.classList.remove('is-loading');
    img.alt = btn.querySelector('img').alt;
    cap.textContent = btn.getAttribute('data-caption');
    preload(index + 1); preload(index - 1);
  }

  function step(d) {
    if (!list.length) return;
    index = (index + d + list.length) % list.length;
    opener = list[index];
    show();
  }

  dialog.querySelector('.lightbox__close').addEventListener('click', function () { dialog.close(); });
  dialog.querySelector('.lightbox__prev').addEventListener('click', function () { step(-1); });
  dialog.querySelector('.lightbox__next').addEventListener('click', function () { step(1); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { if (opener) opener.focus(); img.removeAttribute('src'); });
  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft') step(-1);
  });

  // Swipe left/right on touch screens
  var x0 = null, y0 = null;
  dialog.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  dialog.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) step(dx < 0 ? 1 : -1);
    x0 = y0 = null;
  }, { passive: true });
})();
