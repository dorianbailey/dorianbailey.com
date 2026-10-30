// Cryptid Highway: a small game on the home page.
// Drive a two-lane road at dusk. Jump potholes, cones and deer; photograph
// Mothman, Bigfoot and the Frogman before they slip back into the dark.
// When the trip ends, OddWay deals a real cryptid stop you'd have passed.
(function () {
  var root = document.querySelector('[data-game]');
  if (!root) return;
  var canvas = root.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var panelStart = root.querySelector('[data-game-start]');
  var panelOver = root.querySelector('[data-game-over]');
  var btnStart = root.querySelectorAll('[data-game-go]');
  var btnSnap = root.querySelector('[data-game-snap]');
  var btnJump = root.querySelector('[data-game-jump]');

  var H = 360, W = 960;
  var ROAD_TOP = 268, BASE = 322, ROAD_BOTTOM = 352;   // BASE: where wheels and obstacles sit
  var CAR_X = 120, CAR_W = 124;
  var GRAV = 1900, JUMP_V = -660;
  var OSD = '"VT323", ui-monospace, monospace';
  var BEST_KEY = 'cryptid-highway-best';
  var best = 0;
  try { best = Number(localStorage.getItem(BEST_KEY)) || 0; } catch (e) { best = 0; }

  // Colours: matte dusk, same family as the site
  var C = {
    skyTop: '#16151a', skyMid: '#2a2428', horizon: '#5d4a3d', moon: '#e6e2d8',
    hills: '#262321', trees: '#191816', poles: '#121110', road: '#232120', shoulder: '#151413',
    line: '#cfc9bc', dash: '#a08c64', bone: '#e6e2d8', brass: '#a08c64', ink: '#0e0d0c'
  };

  // ---------- Scenery (seeded so it is the same every visit) ----------
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var HILL_TILE = 1400, TREE_TILE = 1100, POLE_GAP = 360;
  var hills = [], trees = [];
  for (var hx = 0; hx <= HILL_TILE; hx += 20) {
    hills.push(190 + Math.sin(hx / 160) * 14 + Math.sin(hx / 61 + 1.3) * 7 + Math.sin(hx / 347) * 18);
  }
  for (var tx = 0; tx < TREE_TILE; tx += 14 + rnd() * 22) {
    trees.push({ x: tx, h: 34 + rnd() * 46, w: 14 + rnd() * 12 });
  }

  // ---------- State ----------
  var S;
  function reset(mode) {
    S = {
      mode: mode, t: 0, speed: 300, dist: 0, sightings: 0, film: 24,
      car: { y: 0, vy: 0, air: false }, obs: [], cry: [],
      nextObs: 700, nextCry: 4 + Math.random() * 4, flash: 0, shake: 0, toasts: [],
      far: 0, mid: 0, near: 0, road: 0, beat: 0, score: 0
    };
  }
  reset('idle');

  // ---------- Size ----------
  var dpr = 1;
  function resize() {
    var r = canvas.getBoundingClientRect();
    if (!r.width) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(480, Math.round(H * r.width / r.height));
    canvas.width = Math.round(r.width * dpr);
    canvas.height = Math.round(r.height * dpr);
    ctx.setTransform(canvas.width / W, 0, 0, canvas.height / H, 0, 0);
    draw();
  }
  window.addEventListener('resize', resize);

  // ---------- Controls ----------
  function jump() {
    if (S.mode === 'idle' || S.mode === 'over') { start(); return; }
    if (S.mode === 'paused') { S.mode = 'run'; loop(); return; }
    if (!S.car.air) { S.car.vy = JUMP_V; S.car.air = true; }
  }
  function snap() {
    if (S.mode !== 'run') return;
    if (S.film <= 0) { toast('OUT OF FILM'); return; }
    S.film -= 1;
    S.flash = 0.16;
    var target = null;
    S.cry.forEach(function (c) {
      if (!c.shot && c.x > 20 && c.x < W - 20 && (!target || c.x < target.x)) target = c;
    });
    if (target) {
      target.shot = true;
      S.sightings += 1;
      toast(target.name + ' SIGHTED  +150');
    } else {
      toast('NOTHING THERE');
    }
  }
  function toast(text) { S.toasts.push({ text: text, life: 1.4 }); }

  var inView = false;
  window.addEventListener('keydown', function (e) {
    if (!inView) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;
    var k = e.key;
    if (S.mode === 'run' || S.mode === 'paused') {
      if (k === ' ' || k === 'ArrowUp' || k === 'w' || k === 'W') { e.preventDefault(); jump(); }
      else if (k === 's' || k === 'S' || k === 'x' || k === 'X') { e.preventDefault(); snap(); }
      else if (k === 'p' || k === 'P' || k === 'Escape') { pause(); }
    }
  });
  canvas.addEventListener('pointerdown', function (e) { e.preventDefault(); jump(); });
  btnJump.addEventListener('click', function () { jump(); canvas.focus({ preventScroll: true }); });
  btnSnap.addEventListener('click', function () { snap(); });
  btnStart.forEach(function (b) { b.addEventListener('click', start); });

  function start() {
    reset('run');
    panelStart.hidden = true;
    panelOver.hidden = true;
    root.classList.add('is-running');
    canvas.focus({ preventScroll: true });
    loop();
  }
  function pause() {
    if (S.mode === 'run') { S.mode = 'paused'; draw(); }
  }

  // ---------- Spawning ----------
  function spawnObstacle() {
    var r = Math.random();
    var deerChance = Math.min(0.32, 0.14 + S.t / 300);
    var o;
    if (r < deerChance) o = { kind: 'deer', w: 64, h: 58 };
    else if (r < deerChance + 0.33) o = { kind: 'cone', w: 20, h: 28 };
    else o = { kind: 'pothole', w: 54, h: 7 };
    o.x = W + 40;
    S.obs.push(o);
    S.nextObs = (0.9 + Math.random() * 1.2) * S.speed * 0.95 + 240;
  }
  function spawnCryptid() {
    var r = Math.random();
    var c;
    if (r < 0.4) c = { kind: 'mothman', name: 'MOTHMAN', p: 0.6 };
    else if (r < 0.72) c = { kind: 'bigfoot', name: 'BIGFOOT', p: 0.38 };
    else c = { kind: 'frogman', name: 'FROGMAN', p: 0.85 };
    c.x = W + 80;
    c.shot = false;
    S.cry.push(c);
    S.nextCry = 5 + Math.random() * 6;
  }

  // ---------- Update ----------
  function update(dt) {
    S.t += dt;
    S.beat += dt;
    var move = S.mode === 'run' ? 1 : 0.4;
    var speed = S.mode === 'run' ? Math.min(760, 300 + S.t * 9) : 120;
    S.speed = speed;
    var scroll = speed * dt;
    S.far = (S.far + scroll * 0.08) % HILL_TILE;
    S.mid = (S.mid + scroll * 0.25) % TREE_TILE;
    S.near = (S.near + scroll * 0.6) % POLE_GAP;
    S.road = (S.road + scroll) % 80;
    if (S.flash > 0) S.flash -= dt;
    if (S.shake > 0) S.shake -= dt;
    S.toasts.forEach(function (t) { t.life -= dt; });
    S.toasts = S.toasts.filter(function (t) { return t.life > 0; });
    if (S.mode !== 'run') return move;

    S.dist += scroll;
    var car = S.car;
    if (car.air) {
      car.vy += GRAV * dt;
      car.y += car.vy * dt;
      if (car.y >= 0) { car.y = 0; car.vy = 0; car.air = false; }
    }
    S.nextObs -= scroll;
    if (S.nextObs <= 0) spawnObstacle();
    S.nextCry -= dt;
    if (S.nextCry <= 0) spawnCryptid();
    S.obs.forEach(function (o) { o.x -= scroll; });
    S.obs = S.obs.filter(function (o) { return o.x > -120; });
    S.cry.forEach(function (c) { c.x -= scroll * c.p; });
    S.cry = S.cry.filter(function (c) { return c.x > -140; });

    // Collision: the car's body against each obstacle
    var left = CAR_X + 14, right = CAR_X + CAR_W - 10, bottom = BASE + car.y;
    for (var i = 0; i < S.obs.length; i++) {
      var o = S.obs[i];
      var ol = o.x + 6, or = o.x + o.w - 6;
      if (or < left || ol > right) continue;
      var top = BASE - o.h;
      if (o.kind === 'pothole' ? car.y > -4 : bottom > top + 4) { crash(o); break; }
    }
    S.score = Math.round(S.dist / 50) + S.sightings * 150;
    return move;
  }

  function crash(o) {
    S.mode = 'over';
    S.shake = 0.35;
    root.classList.remove('is-running');
    var miles = (S.dist / 5000).toFixed(1);
    var isBest = S.score > best;
    if (isBest) { best = S.score; try { localStorage.setItem(BEST_KEY, String(best)); } catch (e) { /* private mode */ } }
    var cause = o.kind === 'deer' ? 'A deer stepped into your headlights.' : o.kind === 'cone' ? 'You clipped a traffic cone.' : 'You hit a pothole.';
    setTimeout(function () {
      panelOver.querySelector('[data-o="cause"]').textContent = cause;
      panelOver.querySelector('[data-o="score"]').textContent = String(S.score);
      panelOver.querySelector('[data-o="detail"]').textContent =
        miles + ' miles, ' + S.sightings + (S.sightings === 1 ? ' sighting' : ' sightings') + (isBest ? '. A new best.' : '. Best: ' + best + '.');
      panelOver.hidden = false;
      passedStop();
    }, 650);
  }

  // A real cryptid stop from OddWay, dealt live
  function passedStop() {
    var slot = panelOver.querySelector('[data-o="stop"]');
    slot.hidden = true;
    var url = 'https://qnsomzxhnagzjwjhetzu.supabase.co/rest/v1/stops?select=name,slug,city,state' +
      '&category=eq.cryptids&public_access=in.(open,limited,roadside)&order=id&limit=1&offset=' + Math.floor(Math.random() * 82);
    fetch(url, { headers: { apikey: 'sb_publishable_Ao5UP0_OGS8-tz1E_d__iA_Ix0zFcaZ' } })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (rows) {
        var s = rows && rows[0];
        if (!s) return;
        var a = slot.querySelector('a');
        a.textContent = s.name;
        a.href = 'https://taketheoddway.com/stops/' + encodeURIComponent(s.slug);
        slot.querySelector('[data-o="place"]').textContent = [s.city, s.state].filter(Boolean).join(', ');
        slot.hidden = false;
      })
      .catch(function () { /* the panel works without it */ });
  }

  // ---------- Drawing ----------
  function draw() {
    ctx.save();
    if (S.shake > 0) ctx.translate((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 6);
    drawSky();
    drawHills();
    drawTrees();
    S.cry.forEach(function (c) { if (c.kind === 'bigfoot') drawBigfoot(c); });
    drawPoles();
    S.cry.forEach(function (c) { if (c.kind === 'mothman') drawMothman(c); });
    drawRoad();
    S.cry.forEach(function (c) { if (c.kind === 'frogman') drawFrogman(c); });
    S.obs.forEach(drawObstacle);
    drawCar();
    ctx.restore();
    drawHud();
    if (S.flash > 0) { ctx.fillStyle = 'rgba(240,236,226,' + (S.flash / 0.16) * 0.85 + ')'; ctx.fillRect(0, 0, W, H); }
  }

  function drawSky() {
    var g = ctx.createLinearGradient(0, 0, 0, ROAD_TOP);
    g.addColorStop(0, C.skyTop); g.addColorStop(0.55, C.skyMid); g.addColorStop(1, C.horizon);
    ctx.fillStyle = g; ctx.fillRect(-10, -10, W + 20, ROAD_TOP + 10);
    // moon with a soft halo
    var mx = W - 150, my = 62;
    var halo = ctx.createRadialGradient(mx, my, 10, mx, my, 70);
    halo.addColorStop(0, 'rgba(230,226,216,0.18)'); halo.addColorStop(1, 'rgba(230,226,216,0)');
    ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(mx, my, 70, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = C.moon; ctx.beginPath(); ctx.arc(mx, my, 17, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = C.skyMid; ctx.beginPath(); ctx.arc(mx + 7, my - 4, 15, 0, Math.PI * 2); ctx.fill();
  }

  function drawHills() {
    ctx.fillStyle = C.hills;
    ctx.beginPath(); ctx.moveTo(-10, ROAD_TOP);
    for (var x = -20; x <= W + 20; x += 20) {
      var i = Math.floor(((x + S.far) % HILL_TILE) / 20);
      ctx.lineTo(x, hills[i] || 190);
    }
    ctx.lineTo(W + 10, ROAD_TOP); ctx.closePath(); ctx.fill();
  }

  function drawTrees() {
    ctx.fillStyle = C.trees;
    ctx.fillRect(-10, 248, W + 20, ROAD_TOP - 248);
    for (var rep = 0; rep * TREE_TILE < W + TREE_TILE; rep++) {
      for (var i = 0; i < trees.length; i++) {
        var t = trees[i];
        var x = t.x + rep * TREE_TILE - S.mid;
        if (x < -40 || x > W + 40) continue;
        ctx.beginPath();
        ctx.moveTo(x - t.w / 2, 252); ctx.lineTo(x, 252 - t.h); ctx.lineTo(x + t.w / 2, 252);
        ctx.fill();
      }
    }
  }

  function drawPoles() {
    ctx.strokeStyle = C.poles; ctx.fillStyle = C.poles; ctx.lineWidth = 2;
    var first = -S.near;
    var xs = [];
    for (var x = first; x < W + POLE_GAP; x += POLE_GAP) xs.push(x);
    ctx.beginPath();
    for (var i = 0; i < xs.length - 1; i++) {
      for (var w = 0; w < 2; w++) {
        var y = 132 + w * 10;
        ctx.moveTo(xs[i], y);
        ctx.quadraticCurveTo((xs[i] + xs[i + 1]) / 2, y + 26, xs[i + 1], y);
      }
    }
    ctx.stroke();
    xs.forEach(function (x) {
      ctx.fillRect(x - 3, 124, 6, ROAD_TOP - 124);
      ctx.fillRect(x - 18, 130, 36, 4);
    });
  }

  function eyes(x, y, gap, r, color) {
    ctx.save();
    ctx.shadowColor = color; ctx.shadowBlur = 10; ctx.fillStyle = color;
    ctx.beginPath(); ctx.ellipse(x, y, r, r * 0.7, 0, 0, Math.PI * 2); ctx.ellipse(x + gap, y, r, r * 0.7, 0, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  function drawMothman(c) {
    var x = c.x, y = 124;
    ctx.fillStyle = C.poles;
    ctx.fillRect(x - 3, y, 6, ROAD_TOP - y);           // its own pole
    ctx.fillStyle = '#0b0a0a';
    var flap = Math.sin(S.beat * 3) * 6;
    ctx.beginPath();                                     // wings
    ctx.moveTo(x, y - 30);
    ctx.lineTo(x - 46, y - 52 - flap); ctx.lineTo(x - 30, y - 10); ctx.lineTo(x - 12, y - 4);
    ctx.lineTo(x + 12, y - 4); ctx.lineTo(x + 30, y - 10); ctx.lineTo(x + 46, y - 52 - flap);
    ctx.closePath(); ctx.fill();
    ctx.fillRect(x - 9, y - 44, 18, 44);                 // body
    ctx.beginPath(); ctx.arc(x, y - 46, 9, 0, Math.PI * 2); ctx.fill();
    if (!c.shot || Math.sin(S.beat * 9) > 0) eyes(x - 5, y - 47, 10, 3.2, '#c0392b');
  }

  function drawBigfoot(c) {
    var x = c.x, b = 262, s = Math.sin(S.beat * 4);
    ctx.fillStyle = '#3a2d24';
    ctx.beginPath();
    ctx.ellipse(x, b - 40, 15, 25, 0.08, 0, Math.PI * 2); ctx.fill();          // torso
    ctx.beginPath(); ctx.arc(x + 4, b - 70, 9, 0, Math.PI * 2); ctx.fill();    // head
    ctx.save(); ctx.lineCap = 'round'; ctx.strokeStyle = '#3a2d24';
    ctx.lineWidth = 8;
    ctx.beginPath(); ctx.moveTo(x - 4, b - 18); ctx.lineTo(x - 8 + s * 7, b); ctx.moveTo(x + 5, b - 18); ctx.lineTo(x + 8 - s * 7, b); ctx.stroke(); // legs
    ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(x - 10, b - 56); ctx.lineTo(x - 16 - s * 6, b - 28); ctx.moveTo(x + 12, b - 56); ctx.lineTo(x + 16 + s * 6, b - 28); ctx.stroke(); // arms
    ctx.restore();
  }

  function drawFrogman(c) {
    var x = c.x, b = ROAD_TOP + 2;
    ctx.fillStyle = '#4b5a3e';
    ctx.beginPath(); ctx.ellipse(x, b - 18, 12, 18, 0, 0, Math.PI * 2); ctx.fill();   // body
    ctx.beginPath(); ctx.ellipse(x + 1, b - 40, 11, 8, 0, 0, Math.PI * 2); ctx.fill(); // head
    ctx.fillRect(x - 10, b - 4, 7, 4); ctx.fillRect(x + 3, b - 4, 7, 4);               // feet
    eyes(x - 5, b - 43, 11, 2.6, '#d8d0a0');
  }

  function drawRoad() {
    ctx.fillStyle = C.shoulder; ctx.fillRect(-10, ROAD_TOP, W + 20, H - ROAD_TOP + 10);
    ctx.fillStyle = C.road; ctx.fillRect(-10, ROAD_TOP + 6, W + 20, ROAD_BOTTOM - ROAD_TOP - 6);
    ctx.fillStyle = C.line; ctx.globalAlpha = 0.55;
    ctx.fillRect(-10, ROAD_TOP + 6, W + 20, 2); ctx.fillRect(-10, ROAD_BOTTOM - 3, W + 20, 2);
    ctx.globalAlpha = 1;
    ctx.fillStyle = C.dash;
    for (var x = -S.road; x < W + 80; x += 80) ctx.fillRect(x, 292, 40, 3);
  }

  function drawObstacle(o) {
    var x = o.x;
    if (o.kind === 'pothole') {
      ctx.fillStyle = '#0d0c0b'; ctx.beginPath(); ctx.ellipse(x + o.w / 2, BASE + 2, o.w / 2, 6, 0, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(207,201,188,0.18)'; ctx.lineWidth = 1.5; ctx.stroke();
    } else if (o.kind === 'cone') {
      ctx.fillStyle = '#b4613a';
      ctx.beginPath(); ctx.moveTo(x, BASE); ctx.lineTo(x + o.w / 2, BASE - o.h); ctx.lineTo(x + o.w, BASE); ctx.closePath(); ctx.fill();
      ctx.fillStyle = C.bone; ctx.fillRect(x + 5, BASE - 15, o.w - 10, 4);
      ctx.fillStyle = '#8c4a2c'; ctx.fillRect(x - 4, BASE - 2, o.w + 8, 3);
    } else {
      // a deer, standing broadside, eyes catching the headlights
      ctx.fillStyle = '#4a3a2e'; ctx.strokeStyle = '#4a3a2e'; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.ellipse(x + 34, BASE - 34, 24, 11, 0, 0, Math.PI * 2); ctx.fill();   // body
      ctx.lineWidth = 4;
      ctx.beginPath();
      [16, 24, 44, 52].forEach(function (lx) { ctx.moveTo(x + lx, BASE - 28); ctx.lineTo(x + lx, BASE); });
      ctx.moveTo(x + 14, BASE - 38); ctx.lineTo(x + 6, BASE - 52);                                  // neck
      ctx.stroke();
      ctx.beginPath(); ctx.ellipse(x + 4, BASE - 54, 7, 5, -0.4, 0, Math.PI * 2); ctx.fill();         // head
      ctx.lineWidth = 2; ctx.strokeStyle = '#6b5a48';
      ctx.beginPath(); ctx.moveTo(x + 6, BASE - 58); ctx.lineTo(x + 10, BASE - 70); ctx.moveTo(x + 8, BASE - 64); ctx.lineTo(x + 14, BASE - 66); ctx.stroke();
      eyes(x + 1, BASE - 55, 0.01, 1.8, '#f2ecd8');
    }
  }

  function drawCar() {
    var x = CAR_X, b = BASE + S.car.y;
    var bob = S.car.air ? 0 : Math.sin(S.beat * 22) * 0.6;
    // headlight beam
    var beam = ctx.createLinearGradient(x + CAR_W, 0, x + CAR_W + 300, 0);
    beam.addColorStop(0, 'rgba(236,228,200,0.22)'); beam.addColorStop(1, 'rgba(236,228,200,0)');
    ctx.fillStyle = beam;
    ctx.beginPath(); ctx.moveTo(x + CAR_W - 4, b - 22); ctx.lineTo(x + CAR_W + 300, b - 46); ctx.lineTo(x + CAR_W + 300, b + 18); ctx.lineTo(x + CAR_W - 4, b - 14); ctx.closePath(); ctx.fill();
    // body: a boxy old station wagon, facing right
    ctx.fillStyle = '#c9c2b2';
    ctx.beginPath();
    ctx.moveTo(x + 4, b - 12 + bob); ctx.lineTo(x + 4, b - 34 + bob); ctx.lineTo(x + 20, b - 36 + bob);
    ctx.lineTo(x + 26, b - 56 + bob); ctx.lineTo(x + 84, b - 56 + bob); ctx.lineTo(x + 98, b - 36 + bob);
    ctx.lineTo(x + CAR_W - 2, b - 32 + bob); ctx.lineTo(x + CAR_W, b - 12 + bob); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#7a6748'; ctx.fillRect(x + 6, b - 26 + bob, CAR_W - 10, 5);   // wood-grain stripe
    ctx.fillStyle = '#2b2a2e';                                                      // windows
    ctx.beginPath(); ctx.moveTo(x + 30, b - 52 + bob); ctx.lineTo(x + 54, b - 52 + bob); ctx.lineTo(x + 54, b - 38 + bob); ctx.lineTo(x + 26, b - 38 + bob); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x + 58, b - 52 + bob); ctx.lineTo(x + 82, b - 52 + bob); ctx.lineTo(x + 92, b - 38 + bob); ctx.lineTo(x + 58, b - 38 + bob); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#efe6c4'; ctx.fillRect(x + CAR_W - 5, b - 30 + bob, 5, 6);     // headlight
    ctx.fillStyle = '#8c3a2e'; ctx.fillRect(x + 4, b - 30 + bob, 4, 6);             // tail light
    // wheels
    [x + 28, x + CAR_W - 26].forEach(function (wx) {
      ctx.fillStyle = '#0f0e0d'; ctx.beginPath(); ctx.arc(wx, b - 6, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#8f8a80'; ctx.beginPath(); ctx.arc(wx, b - 6, 4, 0, Math.PI * 2); ctx.fill();
    });
  }

  function drawHud() {
    ctx.font = '26px ' + OSD;
    ctx.textBaseline = 'top';
    ctx.fillStyle = 'rgba(0,0,0,0.55)';
    var line = 'MI ' + (S.dist / 5000).toFixed(1) + '   SIGHTINGS ' + S.sightings + '   FILM ' + S.film;
    var right = 'BEST ' + best;
    ctx.fillText(line, 22, 20); ctx.fillText(right, W - 20 - ctx.measureText(right).width + 2, 20);
    ctx.fillStyle = C.bone;
    ctx.fillText(line, 20, 18);
    ctx.fillText(right, W - 20 - ctx.measureText(right).width, 18);
    if (S.mode === 'run' || S.mode === 'paused') {
      ctx.fillStyle = C.bone; ctx.fillText(S.mode === 'paused' ? 'PAUSE ❚❚' : 'SCORE ' + S.score, 20, 46);
    }
    S.toasts.forEach(function (t, i) {
      ctx.globalAlpha = Math.min(1, t.life / 0.4);
      ctx.font = '30px ' + OSD;
      ctx.fillStyle = '#e6d9b0';
      var w = ctx.measureText(t.text).width;
      ctx.fillText(t.text, (W - w) / 2, 84 - (1.4 - t.life) * 18 + i * 32);
      ctx.globalAlpha = 1;
    });
  }

  // ---------- Loop ----------
  var raf = 0, last = 0;
  function frame(now) {
    raf = 0;
    var dt = Math.min(0.033, (now - (last || now)) / 1000);
    last = now;
    update(dt);
    draw();
    var keepGoing = (S.mode === 'run' || S.mode === 'idle' || S.shake > 0 || S.toasts.length) && inView && !document.hidden;
    if (keepGoing) raf = requestAnimationFrame(frame); else last = 0;
  }
  function loop() { if (!raf) { last = 0; raf = requestAnimationFrame(frame); } }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) {
      inView = e[0].isIntersecting;
      if (!inView) pause(); else { resize(); loop(); }
    }, { threshold: 0.25 }).observe(root);
  } else { inView = true; loop(); }
  document.addEventListener('visibilitychange', function () { if (document.hidden) pause(); else if (inView) loop(); });

  // Wait for the VHS font so the dashboard draws in it from the first frame
  (document.fonts && document.fonts.load ? document.fonts.load('26px VT323') : Promise.resolve()).then(resize, resize);
  resize();
})();
