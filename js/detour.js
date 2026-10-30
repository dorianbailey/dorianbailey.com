// Take The OddWay: "Roll a detour"
// Deals one random public stop, live from OddWay's Supabase index (read-only,
// using the project's publishable key, which is public by design).
(function () {
  var root = document.querySelector('[data-detour]');
  if (!root) return;

  var API = 'https://qnsomzxhnagzjwjhetzu.supabase.co/rest/v1/stops';
  var KEY = 'sb_publishable_Ao5UP0_OGS8-tz1E_d__iA_Ix0zFcaZ';
  // Public stops per category when this page was built; a roll past the end retries from the start.
  var COUNTS = {
    'weird-history': 2626, 'roadside-oddities': 2464, 'museums': 1030, 'haunted': 423,
    'folklore': 322, 'cryptids': 82, 'ufos': 48
  };
  var LABELS = {
    'cryptids': 'Cryptids', 'folklore': 'Folklore', 'haunted': 'Haunted', 'ufos': 'UFOs',
    'weird-history': 'Weird history', 'museums': 'Museums', 'roadside-oddities': 'Roadside oddities'
  };
  var card = root.querySelector('[data-detour-card]');
  var btn = root.querySelector('[data-detour-roll]');
  var chips = root.querySelectorAll('.chip');
  var f = function (k) { return card.querySelector('[data-f="' + k + '"]'); };
  var chosen = '';
  var rolls = 0;

  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      c.setAttribute('aria-pressed', 'true');
      chosen = c.getAttribute('data-cat');
    });
  });

  function trimDesc(d) {
    if (!d) return '';
    var parts = d.match(/[^.!?]+[.!?]+/g) || [d];
    var out = parts[0];
    if (parts[1] && (out + parts[1]).length < 260) out += parts[1];
    return out.trim();
  }

  function fetchOne(cat, offset) {
    var url = API + '?select=name,slug,category,city,state,description' +
      '&category=eq.' + encodeURIComponent(cat) +
      '&public_access=in.(open,limited,roadside)&order=id&limit=1&offset=' + offset;
    return fetch(url, { headers: { apikey: KEY } }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function roll() {
    var cats = Object.keys(COUNTS);
    var cat = chosen || cats[Math.floor(Math.random() * cats.length)];
    var offset = Math.floor(Math.random() * COUNTS[cat]);
    btn.disabled = true;
    card.classList.add('is-dealing');
    fetchOne(cat, offset)
      .then(function (rows) { return rows.length ? rows : fetchOne(cat, 0); })
      .then(function (rows) {
        var s = rows[0];
        if (!s) throw new Error('empty');
        rolls += 1;
        f('cat').textContent = (LABELS[s.category] || s.category) + ', stop no. ' + rolls;
        f('name').textContent = s.name;
        f('place').textContent = [s.city, s.state].filter(Boolean).join(', ');
        f('desc').textContent = trimDesc(s.description);
        var a = f('link');
        a.href = 'https://taketheoddway.com/stops/' + encodeURIComponent(s.slug);
        a.textContent = 'Plan the trip on OddWay';
        btn.textContent = 'Roll again';
      })
      .catch(function () {
        f('cat').textContent = 'Road closed';
        f('name').textContent = 'The index didn’t answer';
        f('place').textContent = '';
        f('desc').textContent = 'OddWay couldn’t be reached just now. Try another roll, or browse every stop on the site itself.';
        var a = f('link');
        a.href = 'https://taketheoddway.com/explore';
        a.textContent = 'Explore OddWay';
      })
      .then(function () {
        btn.disabled = false;
        requestAnimationFrame(function () { card.classList.remove('is-dealing'); });
      });
  }

  btn.addEventListener('click', roll);
})();
