// Shared behavior: the full-screen mobile menu and the footer year.
(function () {
  var root = document.documentElement;
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    root.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () { setOpen(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (m) { if (m.matches) setOpen(false); });
  }


  // Pause the home collage while it is scrolled out of view
  var hero = document.querySelector('.frontispiece');
  if (hero && document.querySelector('.collage') && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      hero.classList.toggle('is-offscreen', !entries[0].isIntersecting);
    }).observe(hero);
  }

  // Easter egg: a pair of red eyes blinks in the dark footer now and then.
  // Catch them (click or tap) and Cryptid Highway opens.
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var eyes = document.querySelector('.mothman');
  var footer = document.querySelector('.site-footer');
  if (eyes && footer) {
    var timer = 0, watching = false;
    var sighting = function () {
      timer = 0;
      if (!watching || document.hidden || root.classList.contains('game-open')) { if (watching) next(); return; }
      eyes.style.left = (6 + Math.random() * 84) + '%';
      eyes.style.top = (16 + Math.random() * 52) + '%';
      eyes.classList.remove('is-seen', 'is-caught');
      void eyes.offsetWidth;
      eyes.classList.add('is-seen');
      next();
    };
    var next = function (soon) {
      clearTimeout(timer);
      timer = setTimeout(sighting, soon ? 2500 + Math.random() * 3000 : 14000 + Math.random() * 16000);
    };
    // Only watch while the footer is on screen, and show up soon after it arrives
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) {
        watching = e[0].isIntersecting;
        if (watching && !timer) next(true);
        if (!watching) { clearTimeout(timer); timer = 0; }
      }, { threshold: 0.3 }).observe(footer);
    } else { watching = true; next(true); }
    // Gone when it finishes blinking: no longer catchable
    eyes.addEventListener('animationend', function () { eyes.classList.remove('is-seen'); });
    eyes.addEventListener('click', function () {
      if (!eyes.classList.contains('is-seen')) return;
      eyes.classList.add('is-caught');
      setTimeout(function () { eyes.classList.remove('is-seen', 'is-caught'); openGame(); }, calm ? 0 : 420);
    });
  }

  // Cryptid Highway in a dialog, built from the footer's <template> the first time it's needed.
  var dialog = null;
  function openGame() {
    var tpl = document.getElementById('cryptid-highway');
    if (!tpl || !window.HTMLDialogElement) return;
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'game-dialog band--dark';
      dialog.setAttribute('aria-labelledby', 'game-dialog-title');
      dialog.appendChild(tpl.content.cloneNode(true));
      document.body.appendChild(dialog);
      dialog.querySelector('[data-game-close]').addEventListener('click', function () { dialog.close(); });
      // A click on the dimmed page outside the dialog closes it
      dialog.addEventListener('click', function (e) {
        if (e.target !== dialog) return;
        var r = dialog.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
      });
      dialog.addEventListener('close', function () { root.classList.remove('game-open'); });
      var s = document.createElement('script');
      s.src = eyes ? eyes.getAttribute('data-game-src') : 'js/game.js';
      document.body.appendChild(s);
    }
    if (dialog.open) return;
    root.classList.add('game-open');
    dialog.showModal();
  }

  // Easter eggs for the keyboard: type "oddway" and the page loses tracking for a moment;
  // type "mothman" and you go looking for it.
  var typed = '';
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey || e.key.length !== 1) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable], dialog')) return;
    typed = (typed + e.key.toLowerCase()).slice(-7);
    if (typed.slice(-6) === 'oddway') { typed = ''; sweep(); }
    else if (typed === 'mothman') { typed = ''; openGame(); }
  });
  function sweep() {
    if (document.querySelector('.vhs-sweep')) return;
    var o = document.createElement('div');
    o.className = 'vhs-sweep' + (calm ? ' vhs-sweep--calm' : '');
    o.setAttribute('aria-hidden', 'true');
    o.innerHTML = '<canvas width="160" height="90"></canvas><span class="vhs-sweep__band"></span>' +
      '<span class="vhs-sweep__osd vhs-sweep__osd--tl">TRACKING</span>' +
      '<span class="vhs-sweep__osd vhs-sweep__osd--bl">TAKE THE ODDWAY &#9654;</span>';
    document.body.appendChild(o);
    var c = o.querySelector('canvas'), x = c.getContext('2d'), im = x.createImageData(160, 90), t0 = performance.now();
    (function frame(t) {
      if (!o.isConnected) return;
      if (!calm) {
        for (var i = 0; i < im.data.length; i += 4) { var v = (Math.random() * 230) | 0; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
        x.putImageData(im, 0, 0);
      }
      if (t - t0 < 1700) requestAnimationFrame(frame);
    })(t0);
    setTimeout(function () { o.classList.add('is-out'); }, 1500);
    setTimeout(function () { o.remove(); }, 2000);
  }

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
