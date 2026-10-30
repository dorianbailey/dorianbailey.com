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

  // Easter egg: now and then, a pair of red eyes blinks in the dark footer.
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var eyes = document.querySelector('.mothman');
  if (eyes && !calm) {
    var sighting = function () {
      eyes.style.left = (6 + Math.random() * 84) + '%';
      eyes.style.top = (16 + Math.random() * 52) + '%';
      eyes.classList.remove('is-seen');
      void eyes.offsetWidth;
      eyes.classList.add('is-seen');
      setTimeout(sighting, 22000 + Math.random() * 26000);
    };
    setTimeout(sighting, 5000 + Math.random() * 7000);
  }

  // Easter egg: type "oddway" anywhere and the page loses tracking for a moment.
  var typed = '';
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey || e.key.length !== 1) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;
    typed = (typed + e.key.toLowerCase()).slice(-6);
    if (typed === 'oddway') { typed = ''; sweep(); }
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
