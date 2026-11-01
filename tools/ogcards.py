"""Share images (1200x630) for the venture pages and every journal post, scheduled ones included.
A photograph on the left, the title and the signature on the right; posts without a photograph get
a text card. Needs Playwright with Chromium. Run after site.py: python3 tools/ogcards.py ."""
import json, pathlib, subprocess, sys, tempfile
from PIL import Image

R = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SC = pathlib.Path(tempfile.mkdtemp())
sig = json.load(open(R / "tools/signature.json"))
m = json.load(open(R / "assets/photos/photos.json"))
C = {c["id"]: c for c in m["collections"]}
ph = lambda cid, n: str(R / "assets/photos" / C[cid]["photos"][n - 1]["file"])

# slug: (photo, focus, kicker, title, subtitle, style)
CARDS = {
    "photography": (ph("legends", 26), "center 30%", "Dorian Bailey", "Photography", "All types of photography offered.<br>Inquire for rates. Erie County, PA", ""),
    "better-selling": (str(R / "assets/img/dorian-bailey.jpg"), "center 20%", "Dorian Bailey", "Better Selling<br>With Bailey", "Estate sales across Erie County, PA", ""),
    "oddway": (ph("green-eyes", 7), "center 35%", "Dorian Bailey", "Take The OddWay", "A road-trip guide to the strange", ""),
    "metazoo": (ph("legends", 2), "center 40%", "Dorian Bailey", "Bailey MetaZoo", "Cryptids, folklore and trading cards", ""),
    "record": (str(R / "assets/img/dorian-bailey.jpg"), "center 20%", "The Record of", "Dorian Bailey", "Marketing and MIS, Penn State Behrend<br>Photographer and founder, North East, PA", ""),
}
for j in json.load(open(R / "tools/journal-cards.json")):
    img = str(R / "assets/photos" / j["image"]) if j["image"] else None
    CARDS["journal-" + j["slug"]] = (img, j["pos"], "Dorian Bailey &middot; Journal", j["title"].replace("’", "&rsquo;"), j["sub"], "j" if img else "t")

path = lambda d: f'<path fill-rule="evenodd" d="{d}"/>'
cards = []
for slug, (img, pos, pre, title, sub, style) in CARDS.items():
    photo = f'<div class="photo" style="background-image:url(\'file://{img}\');background-position:{pos}"></div>' if img else ""
    cards.append(f'''<div class="card {('card--' + style) if style else ''}" id="{slug}">{photo}
  <div class="text"><p class="pre">{pre}</p><h1>{title}</h1><div class="rule"></div><p class="sub">{sub}</p>
    <svg class="sig" viewBox="{sig['viewBox']}">{path(sig['refined_text'])}</svg></div>
  <div class="frame"></div>
</div>''')
(SC / "cards.html").write_text(f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "D"; src: url("file://{R}/assets/fonts/libre-caslon-display-latin-400-normal.woff2"); }}
@font-face {{ font-family: "T"; font-style: italic; src: url("file://{R}/assets/fonts/libre-caslon-text-latin-400-italic.woff2"); }}
body {{ margin: 0; background: #000; }}
.card {{ position: relative; width: 1200px; height: 630px; display: grid; grid-template-columns: 480px 1fr; background: #1c1b19; color: #e6e2d8; overflow: hidden; }}
.photo {{ background-size: cover; filter: saturate(.92) contrast(1.02); box-shadow: inset -60px 0 80px -40px rgba(0,0,0,.55); }}
.text {{ padding: 0 70px 0 64px; display: flex; flex-direction: column; justify-content: center; position: relative; }}
.pre {{ font-family: "T"; font-style: italic; font-size: 30px; color: #a39e92; margin: 0 0 12px; }}
h1 {{ font-family: "D"; font-weight: 400; font-size: 82px; line-height: 1.02; margin: 0; letter-spacing: .01em; }}
.rule {{ width: 130px; height: 5px; border-top: 1.5px solid #a08c64; border-bottom: 1.5px solid #a08c64; margin: 30px 0 24px; }}
.sub {{ font-family: "T"; font-style: italic; font-size: 27px; color: #a39e92; margin: 0; line-height: 1.4; }}
.sig {{ position: absolute; right: 56px; bottom: 44px; width: 150px; fill: #a08c64; opacity: .9; }}
.card--j h1 {{ font-size: 58px; line-height: 1.06; }} .card--j .pre {{ font-size: 26px; }} .card--j .sub {{ font-size: 25px; }}
.card--t {{ grid-template-columns: 1fr; }} .card--t .text {{ padding: 0 120px; }} .card--t h1 {{ font-size: 68px; line-height: 1.06; max-width: 900px; }}
.card--t .pre {{ font-size: 28px; }} .card--t .sig {{ width: 190px; right: 80px; bottom: 60px; }}
.frame {{ position: absolute; inset: 20px; border: 1px solid rgba(160,140,100,.38); pointer-events: none; }}
</style></head><body>{"".join(cards)}</body></html>''')
(SC / "shoot.js").write_text(f'''const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1200, height: 630 }} }});
  await p.goto('file://{SC}/cards.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  for (const id of {json.dumps(list(CARDS))}) await p.locator('#' + id).screenshot({{ path: '{SC}/' + id + '.png' }});
  await b.close(); }})();''')
subprocess.run(["node", str(SC / "shoot.js")], check=True)
for slug in CARDS:
    Image.open(SC / f"{slug}.png").convert("RGB").save(R / f"assets/img/og-{slug}.jpg", quality=86, optimize=True, progressive=True)
print(len(CARDS), "cards")
