// Bailey MetaZoo: the television.
// Static and the VHS on-screen display until a tape goes in; then the chosen
// short plays from YouTube's privacy-enhanced player. The tape list is built
// from assets/data/youtube.json, refreshed by a scheduled GitHub Action.
(function () {
  var tv = document.querySelector('[data-tv]');
  if (!tv) return;
  var canvas = tv.querySelector('.tv__static');
  var ctx = canvas.getContext('2d');
  var player = tv.querySelector('[data-tv-player]');
  var insert = tv.querySelector('[data-tv-insert]');
  var state = tv.querySelector('[data-tv-state]');
  var dateEl = tv.querySelector('[data-tv-date]');
  var titleEl = tv.querySelector('[data-tv-title]');
  var tapes = Array.prototype.slice.call(document.querySelectorAll('.tape'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var current = tapes[0];
  var playing = false;
  var running = false;
  var last = 0;

  // Snow: a small canvas of random grey pixels, scaled up
  var img = ctx.createImageData(canvas.width, canvas.height);
  function snow() {
    var d = img.data;
    for (var i = 0; i < d.length; i += 4) {
      var v = (Math.random() * 200) | 0;
      d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  }
  function loop(t) {
    if (!running) return;
    if (t - last > 55) { snow(); last = t; }
    requestAnimationFrame(loop);
  }
  function startSnow() { if (reduce) { snow(); return; } if (!running) { running = true; requestAnimationFrame(loop); } }
  function stopSnow() { running = false; }

  // Only animate while the set is on screen
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) {
      if (e[0].isIntersecting && !playing) startSnow(); else stopSnow();
    }).observe(tv);
  } else { startSnow(); }

  function select(tape) {
    current = tape;
    tapes.forEach(function (t) { t.setAttribute('aria-pressed', String(t === tape)); });
    dateEl.textContent = tape.getAttribute('data-date');
    titleEl.textContent = tape.getAttribute('data-title');
  }

  // Picking another tape ejects the one playing: back to static, STOP, and the
  // "Insert tape" button, so every tape goes in the same way.
  var pending = 0;
  function eject() {
    clearTimeout(pending);
    player.innerHTML = '';
    playing = false;
    tv.classList.remove('is-playing', 'is-loading');
    state.textContent = 'STOP ■';
    insert.hidden = false;
    startSnow();
  }

  function play() {
    var id = current.getAttribute('data-id');
    tv.classList.add('is-loading');
    state.textContent = 'PLAY ▶';
    insert.hidden = true;
    var go = function () {
      player.innerHTML = '';
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&playsinline=1&rel=0&modestbranding=1';
      f.title = current.getAttribute('data-title');
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      player.appendChild(f);
      playing = true;
      stopSnow();
      tv.classList.remove('is-loading');
      tv.classList.add('is-playing');
    };
    if (reduce) go(); else pending = setTimeout(go, 650);
  }

  insert.addEventListener('click', play);
  tapes.forEach(function (t) {
    t.addEventListener('click', function () {
      eject();
      select(t);
      // On a phone the list sits below the set: bring the TV (and its button) back into view
      var r = tv.getBoundingClientRect();
      if (r.top < 0 || r.bottom > window.innerHeight) tv.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
      insert.focus({ preventScroll: true });
    });
  });
})();
