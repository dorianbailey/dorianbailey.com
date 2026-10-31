// Bookings: "Book now" opens a small calendar. Picking a date fills in a short request
// ("I'd like to book a photo shoot on Saturday, November 14, 2026") that is emailed to
// Dorian through FormSubmit. If that can't be reached, the visitor's own email app opens
// with the same request written out, so nothing is lost.
(function () {
  var buttons = document.querySelectorAll('[data-book]');
  if (!buttons.length || !window.HTMLDialogElement) return;
  var me = document.currentScript || document.querySelector('script[src*="book.js"]');
  var TO = me.getAttribute('data-to');
  var TO_ESTATE = me.getAttribute('data-to-estate') || TO;     // estate sales have their own inbox
  var PHOTO_TYPES = (me.getAttribute('data-photo-types') || '').split('|').filter(Boolean);

  var SERVICES = {
    photo: {
      name: 'Photo shoot', title: 'Book a photo shoot', ask: 'I’d like to book a photo shoot on',
      extra: { key: 'Type of photography', options: PHOTO_TYPES.concat(['Something else']) }
    },
    estate: {
      name: 'Estate sale', title: 'Request an estate sale', ask: 'I’d like to request an estate sale with Better Selling With Bailey on',
      extra: { key: 'Town', placeholder: 'North East, Erie, Harborcreek…' }
    },
    ads: {
      name: 'Advertising on OddWay', title: 'Book a call about advertising', ask: 'I’d like to set up a call about advertising on Take The OddWay on',
      extra: { key: 'Business or brand', placeholder: 'Your business' }
    }
  };
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function day0(d) { return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function longDate(d) { return DAYS[d.getDay()] + ', ' + MONTHS[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear(); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var today = day0(new Date());
  var first = new Date(today); first.setDate(first.getDate() + 1);             // earliest bookable day: tomorrow
  var last = new Date(today); last.setFullYear(last.getFullYear() + 1);         // up to a year ahead

  var dialog = document.createElement('dialog');
  dialog.className = 'book';
  dialog.setAttribute('aria-labelledby', 'book-title');
  document.body.appendChild(dialog);
  var service, view, picked, preset;

  function shell(inner) {
    dialog.innerHTML = '<div class="book__head"><p class="book__kicker">Bookings available now</p>' +
      '<h2 class="book__title" id="book-title">' + esc(SERVICES[service].title) + '</h2>' +
      '<button class="book__close" type="button" aria-label="Close">Close</button></div>' + inner;
    dialog.querySelector('.book__close').addEventListener('click', function () { dialog.close(); });
  }

  // ---------- Step 1: the calendar
  function calendar() {
    var y = view.getFullYear(), m = view.getMonth();
    var startDay = new Date(y, m, 1).getDay(), n = new Date(y, m + 1, 0).getDate();
    var cells = '';
    for (var i = 0; i < startDay; i++) cells += '<span></span>';
    for (var d = 1; d <= n; d++) {
      var dt = new Date(y, m, d), off = dt < first || dt > last;
      var sel = picked && dt.getTime() === picked.getTime();
      cells += '<button type="button" class="cal__day' + (sel ? ' is-picked' : '') + (dt.getTime() === today.getTime() ? ' is-today' : '') + '"' +
        ' data-d="' + d + '"' + (off ? ' disabled' : '') + ' aria-label="' + longDate(dt) + '"' + (sel ? ' aria-pressed="true"' : '') + '>' + d + '</button>';
    }
    var canPrev = new Date(y, m, 1) > new Date(first.getFullYear(), first.getMonth(), 1);
    var canNext = new Date(y, m + 1, 1) <= last;
    shell('<p class="book__lede">Choose a date and Dorian Bailey will confirm by email.</p>' +
      '<div class="cal" role="group" aria-label="Choose a date">' +
      '<div class="cal__bar"><button type="button" class="cal__nav" data-step="-1" aria-label="Previous month"' + (canPrev ? '' : ' disabled') + '>&lsaquo;</button>' +
      '<p class="cal__month" aria-live="polite">' + MONTHS[m] + ' ' + y + '</p>' +
      '<button type="button" class="cal__nav" data-step="1" aria-label="Next month"' + (canNext ? '' : ' disabled') + '>&rsaquo;</button></div>' +
      '<div class="cal__week" aria-hidden="true"><span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span></div>' +
      '<div class="cal__grid">' + cells + '</div></div>');
    dialog.querySelectorAll('.cal__nav').forEach(function (b) {
      b.addEventListener('click', function () { view = new Date(y, m + Number(b.getAttribute('data-step')), 1); calendar(); focusDay(); });
    });
    dialog.querySelectorAll('.cal__day').forEach(function (b) {
      b.addEventListener('click', function () { picked = new Date(y, m, Number(b.getAttribute('data-d'))); form(); });
    });
    dialog.querySelector('.cal__grid').addEventListener('keydown', function (e) {
      var steps = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
      if (!steps || !e.target.classList.contains('cal__day')) return;
      e.preventDefault();
      var next = new Date(y, m, Number(e.target.getAttribute('data-d')) + steps);
      if (next < first || next > last) return;
      if (next.getMonth() !== m) { view = new Date(next.getFullYear(), next.getMonth(), 1); calendar(); }
      var t = dialog.querySelector('.cal__day[data-d="' + next.getDate() + '"]'); if (t) t.focus();
    });
  }
  function focusDay() {
    var t = dialog.querySelector('.cal__day.is-picked:not([disabled])') || dialog.querySelector('.cal__day:not([disabled])');
    if (t) t.focus();
  }

  // ---------- Step 2: the request, written out with the chosen date
  function form() {
    var s = SERVICES[service], x = s.extra;
    var extra = x.options
      ? '<label class="book__field"><span>' + esc(x.key) + '</span><select name="extra">' + x.options.map(function (o) { return '<option' + (o === preset ? ' selected' : '') + '>' + esc(o) + '</option>'; }).join('') + '</select></label>'
      : '<label class="book__field"><span>' + esc(x.key) + ' <em>optional</em></span><input name="extra" type="text" autocomplete="off" placeholder="' + esc(x.placeholder || '') + '"></label>';
    shell('<p class="book__date"><span>' + esc(s.name) + '</span> ' + esc(longDate(picked)) + ' <button type="button" class="book__change">Change date</button></p>' +
      '<form class="book__form" novalidate>' +
      '<label class="book__field"><span>Name</span><input name="name" type="text" autocomplete="name" required></label>' +
      '<label class="book__field"><span>Email</span><input name="email" type="email" autocomplete="email" required></label>' +
      '<label class="book__field"><span>Phone <em>optional</em></span><input name="phone" type="tel" autocomplete="tel"></label>' +
      extra +
      '<label class="book__field"><span>Your request</span><textarea name="message" rows="4">Hi Dorian, ' + esc(s.ask) + ' ' + esc(longDate(picked)) + '.</textarea></label>' +
      '<input class="book__honey" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<p class="book__error" role="alert" hidden></p>' +
      '<div class="btn-row"><button class="btn" type="submit">Send request</button></div>' +
      '<p class="book__fine">Sent to Dorian Bailey by email. <a href="' + (me.getAttribute('data-privacy') || '/privacy/') + '">Privacy</a></p>' +
      '</form>');
    dialog.querySelector('.book__change').addEventListener('click', function () { calendar(); focusDay(); });
    var f = dialog.querySelector('form');
    f.querySelector('input[name="name"]').focus();
    f.addEventListener('submit', function (e) { e.preventDefault(); send(f); });
  }

  // ---------- Step 3: send, or hand over to the visitor's email app
  function inbox() { return service === 'estate' ? TO_ESTATE : TO; }
  function send(f) {
    var s = SERVICES[service], err = f.querySelector('.book__error');
    var v = function (n) { var el = f.elements[n]; return el ? el.value.trim() : ''; };
    if (!v('name') || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) {
      err.textContent = 'Please add your name and a valid email address so Dorian can reply.'; err.hidden = false; return;
    }
    if (v('_honey')) { done(v('email'), true); return; }   // a bot filled the hidden field
    var subject = 'Booking request: ' + s.name + ', ' + longDate(picked);
    var payload = {
      _subject: subject, _template: 'table', _replyto: v('email'),
      Service: s.name, Date: longDate(picked), Name: v('name'), email: v('email'), Phone: v('phone') || '—'
    };
    payload[s.extra.key] = v('extra') || '—';
    payload.Request = v('message');
    var btn = f.querySelector('button[type="submit"]');
    btn.disabled = true; btn.textContent = 'Sending…';
    fetch('https://formsubmit.co/ajax/' + inbox(), {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload)
    }).then(function (r) { return r.json(); }).then(function (data) {
      if (data && (data.success === true || data.success === 'true')) done(v('email'), true);
      else fallback(subject, payload);
    }).catch(function () { fallback(subject, payload); });
  }
  function fallback(subject, p) {
    var body = Object.keys(p).filter(function (k) { return k.charAt(0) !== '_'; }).map(function (k) {
      return k === 'Request' ? '\n' + p[k] : (k === 'email' ? 'Email' : k) + ': ' + p[k];
    }).join('\n');
    window.location.href = 'mailto:' + inbox() + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    done(p.email, false);
  }
  function done(email, sent) {
    shell(sent
      ? '<div class="book__done"><p class="book__big">Request sent.</p><p>Dorian Bailey will reply to <strong>' + esc(email) + '</strong> to confirm ' + esc(longDate(picked)) + '.</p>' +
        '<div class="btn-row"><button class="btn" type="button" data-close>Done</button></div></div>'
      : '<div class="book__done"><p class="book__big">Almost there.</p><p>Your email app should open with the request written out; press send to finish. If it doesn&rsquo;t, write to <a href="mailto:' + esc(inbox()) + '">' + esc(inbox()) + '</a>.</p>' +
        '<div class="btn-row"><button class="btn" type="button" data-close>Done</button></div></div>');
    dialog.querySelector('[data-close]').addEventListener('click', function () { dialog.close(); });
    dialog.querySelector('[data-close]').focus();
  }

  function open(kind, type) {
    service = SERVICES[kind] ? kind : 'photo';
    preset = type || '';
    picked = null;
    // Open on this month, or on next month when less than a week of this one is left
    var monthEnd = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
    view = new Date(first.getFullYear(), first.getMonth() + (monthEnd - first.getDate() < 6 ? 1 : 0), 1);
    calendar();
    document.documentElement.classList.add('book-open');
    dialog.showModal();
    focusDay();
  }
  dialog.addEventListener('close', function () { document.documentElement.classList.remove('book-open'); });
  dialog.addEventListener('click', function (e) {
    if (e.target !== dialog) return;
    var r = dialog.getBoundingClientRect();
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
  });
  buttons.forEach(function (b) { b.addEventListener('click', function () { open(b.getAttribute('data-book'), b.getAttribute('data-book-type')); }); });
})();
