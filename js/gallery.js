// Photographs: opens a plate full size, with previous/next within its collection.
(function () {
  var dialog = document.getElementById('lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var img = dialog.querySelector('img');
  var cap = dialog.querySelector('figcaption');
  var list = [];
  var index = 0;
  var opener = null;

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

  function show() {
    var btn = list[index];
    var thumb = btn.querySelector('img');
    img.src = btn.getAttribute('data-full');
    img.alt = thumb.alt;
    cap.textContent = btn.getAttribute('data-caption');
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
  dialog.addEventListener('close', function () { if (opener) opener.focus(); img.src = ''; });
  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft') step(-1);
  });
})();
