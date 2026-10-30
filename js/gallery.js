// Photography gallery.
// Photos are listed in assets/photos/photos.json — see assets/photos/README.md.
// The page renders a filterable grid and a lightbox from that list.
(function () {
  var grid = document.getElementById('gallery');
  var filters = document.getElementById('gallery-filters');
  var empty = document.getElementById('gallery-empty');
  var dialog = document.getElementById('lightbox');
  if (!grid) return;

  var manifest = grid.getAttribute('data-manifest');
  var base = manifest.replace(/photos\.json$/, '');
  var photos = [];
  var current = 0;
  var visible = [];

  fetch(manifest, { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : []; })
    .catch(function () { return []; })
    .then(function (list) {
      photos = Array.isArray(list) ? list.filter(function (p) { return p && p.file; }) : [];
      if (!photos.length) { empty.hidden = false; return; }
      buildFilters();
      render('All');
    });

  function buildFilters() {
    var cats = ['All'];
    photos.forEach(function (p) {
      if (p.category && cats.indexOf(p.category) === -1) cats.push(p.category);
    });
    if (cats.length < 3) return; // no point filtering a single category
    cats.forEach(function (c) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'chip';
      b.textContent = c;
      b.setAttribute('aria-pressed', c === 'All' ? 'true' : 'false');
      b.addEventListener('click', function () {
        filters.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        render(c);
      });
      filters.appendChild(b);
    });
    filters.hidden = false;
  }

  function render(cat) {
    grid.innerHTML = '';
    visible = photos.filter(function (p) { return cat === 'All' || p.category === cat; });
    visible.forEach(function (p, i) {
      var fig = document.createElement('figure');
      fig.className = 'gallery__item';
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.setAttribute('aria-label', 'View larger: ' + (p.alt || p.title || 'photo'));
      var img = document.createElement('img');
      img.src = base + (p.thumb || p.file);
      img.alt = p.alt || '';
      img.loading = 'lazy';
      img.decoding = 'async';
      btn.appendChild(img);
      btn.addEventListener('click', function () { open(i); });
      fig.appendChild(btn);
      if (p.title) {
        var cap = document.createElement('figcaption');
        cap.textContent = p.title;
        fig.appendChild(cap);
      }
      grid.appendChild(fig);
    });
  }

  function open(i) {
    current = i;
    show();
    if (typeof dialog.showModal === 'function') dialog.showModal();
  }

  function show() {
    var p = visible[current];
    var img = dialog.querySelector('img');
    img.src = base + p.file;
    img.alt = p.alt || '';
    dialog.querySelector('p').textContent = [p.title, p.location].filter(Boolean).join(' · ');
  }

  dialog.querySelector('.lightbox__close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  document.addEventListener('keydown', function (e) {
    if (!dialog.open || !visible.length) return;
    if (e.key === 'ArrowRight') { current = (current + 1) % visible.length; show(); }
    if (e.key === 'ArrowLeft') { current = (current - 1 + visible.length) % visible.length; show(); }
  });
})();
