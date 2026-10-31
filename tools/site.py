"""Generates the dorianbailey.com pages (plain HTML, committed to the repo).
Run: python3 site.py /path/to/repo
Shared head/header/footer live here so every page stays consistent."""
import json, pathlib, sys, html

ROOT = pathlib.Path(sys.argv[1])
SITE = "https://dorianbailey.com"
EMAIL = "dorianbailey814@gmail.com"
M = json.load(open(ROOT / "assets/photos/photos.json"))
COLL = {c["id"]: c for c in M["collections"]}
TOTAL = sum(len(c["photos"]) for c in M["collections"])
NUMWORD = ["Zero","One","Two","Three","Four","Five","Six","Seven","Eight"][len(M["collections"])]

NAV = [
    ("#services", "Services", "services"),
    ("photography/", "Photography", "photo"),
    ("better-selling/", "Better Selling", "selling"),
    ("oddway/", "OddWay", "oddway"),
    ("metazoo/", "MetaZoo", "metazoo"),
    ("record/", "Record", "record"),
    ("#correspondence", "Contact", "contact"),
]

LINKS = {
    "github": "https://github.com/dorianbailey",
    "yt": "https://www.youtube.com/@baileymetazoo",
    "ig": "https://www.instagram.com/baileymetazoo/",
    "bswb": "https://bettersellingwithbailey.com",
    "bswb_fb": "https://www.facebook.com/bettersellingwithbailey",
    "erie": "https://www.yourerie.com/news/local-news/star-wars-sale-draws-crowd-in-north-east/",
    "oddway": "https://taketheoddway.com",
    "shop": "https://shoptheoddway.com",
    "linkedin": "https://www.linkedin.com/in/dorian-bailey/",
    "vanta": "https://vantahouse.studio",
    "oddway_ads": "https://taketheoddway.com/advertise",
}
BSWB_EMAIL = "bettersellingwithbailey@gmail.com"     # estate sale inquiries and bookings go here
# FormSubmit form IDs for the booking requests (issued when each inbox activated its form)
FORM_ID = "511032ddbe1c69af5fe8d840dfea7b33"          # dorianbailey814@gmail.com
FORM_ID_ESTATE = "52c841a84d745bd972229883ba98b50b"   # bettersellingwithbailey@gmail.com


import hashlib
from urllib.parse import quote

# ---------------------------------------------------------------- Services and structured data
PHOTO_TYPES = [
    ("Events and festivals", "Conventions, tournaments, festivals and parties, covered from the doors opening to the last photo."),
    ("Portraits and headshots", "Headshots for work and profiles, and portraits for everything else."),
    ("Seniors and graduates", "Senior pictures and graduation portraits, on location around Erie County."),
    ("Couples and families", "Engagements, anniversaries and family sessions."),
    ("Sports and competitions", "Games, matches and card tournaments: the action and the people around it."),
    ("Products and small businesses", "Product photos, storefronts and social content for local businesses."),
    ("Real estate and interiors", "Listings, rentals and estate sale previews, bright and true to the room."),
    ("Landscapes and nature", "Scenic and nature photography, from the lakeshore to the gorge."),
]
MAILTO_PHOTO = ("mailto:" + EMAIL + "?subject=" + quote("Photography inquiry") + "&body=" +
                quote("Hi Dorian,\n\nType of photography:\nDate:\nLocation:\n\n"))
MAILTO_BSWB = ("mailto:" + BSWB_EMAIL + "?subject=" + quote("Estate sale inquiry"))
PERSON_ID = SITE + "/#dorian-bailey"
PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Dorian Bailey", "url": SITE + "/",
    "image": SITE + "/assets/img/dorian-bailey.jpg", "email": "mailto:" + EMAIL,
    "description": "Dorian Bailey is a photographer, marketer and founder from North East, Pennsylvania: Dorian Bailey Photography, "
                   "Better Selling With Bailey estate sales, Take The OddWay and Bailey MetaZoo.",
    "jobTitle": ["Photographer", "Marketing Assistant", "Founder"],
    "address": {"@type": "PostalAddress", "addressLocality": "North East", "addressRegion": "PA", "addressCountry": "US"},
    "homeLocation": {"@type": "Place", "name": "North East, Pennsylvania"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Penn State Behrend", "url": "https://behrend.psu.edu"},
    "worksFor": {"@type": "Organization", "name": "Vanta House", "url": LINKS["vanta"]},
    "knowsAbout": ["Photography", "Event photography", "Portrait photography", "Estate sales", "Digital marketing",
                   "Search engine optimization", "Social media marketing", "Web development", "MetaZoo"],
    "sameAs": [LINKS["linkedin"], LINKS["github"], LINKS["yt"], LINKS["ig"], LINKS["bswb"], LINKS["bswb_fb"], LINKS["oddway"]],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Dorian Bailey",
           "alternateName": "The Collection of Dorian Bailey", "inLanguage": "en-US", "publisher": {"@id": PERSON_ID}}
AREA = [{"@type": "AdministrativeArea", "name": "Erie County, Pennsylvania"}, {"@type": "City", "name": "North East, Pennsylvania"},
        {"@type": "City", "name": "Erie, Pennsylvania"}]
PHOTO_SERVICE = {
    "@type": "ProfessionalService", "@id": SITE + "/photography/#service", "name": "Dorian Bailey Photography",
    "url": SITE + "/photography/", "image": SITE + "/assets/img/og-photography.jpg", "email": EMAIL,
    "description": "All types of photography offered by Dorian Bailey in North East and Erie, Pennsylvania: events, portraits, "
                   "seniors, families, sports, products and real estate. Inquire for rates.",
    "founder": {"@id": PERSON_ID}, "areaServed": AREA,
    "address": {"@type": "PostalAddress", "addressLocality": "North East", "addressRegion": "PA", "addressCountry": "US"},
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Photography by Dorian Bailey", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in PHOTO_TYPES]},
}
ESTATE_SERVICE = {
    "@type": "Service", "@id": SITE + "/better-selling/#service", "name": "Estate sales by Better Selling With Bailey",
    "serviceType": "Estate sale management", "areaServed": AREA,
    "description": "Dorian Bailey prices, stages, promotes and runs estate sales in the client's home across Erie County, Pennsylvania, "
                   "and removes whatever is left at no charge.",
    "provider": {"@type": "LocalBusiness", "name": "Better Selling With Bailey", "url": LINKS["bswb"], "sameAs": [LINKS["bswb_fb"]], "email": BSWB_EMAIL,
                 "founder": {"@id": PERSON_ID}, "areaServed": AREA,
                 "address": {"@type": "PostalAddress", "addressLocality": "North East", "addressRegion": "PA", "addressCountry": "US"}},
    "offers": {"@type": "Offer", "description": "$995 flat fee plus 20% commission on total sales; leftover removal free"},
}


def v(rel):
    """Content fingerprint for cache-busting: base.css?v=abc123 changes whenever the file does."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


# The mark: Dorian's signature, traced from his drawing (tools/signature-source.png).
# tools/signature.json holds the path data: 'refined_display' as drawn, for the frontispiece;
# 'refined_text', a hair heavier so the fine tips hold up at header and footer sizes;
# 'refined_icon', much heavier, for the tab icons; and 'centre' lines for the signing animation.
SIG = json.load(open(ROOT / "tools/signature.json"))
SIG_VB = SIG["viewBox"]
_vb = [float(n) for n in SIG_VB.split()]
SIG_RATIO = _vb[2] / _vb[3]
# One copy of the small-size path per page; every mark on the page <use>s it.
SIG_SPRITE = (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
              f'<symbol id="sig" viewBox="{SIG_VB}"><path fill-rule="evenodd" d="{SIG["refined_text"]}"/></symbol></svg>')


def sig(height, cls="sig"):
    """The signature at a given height (width follows its proportions)."""
    return (f'<svg class="{cls}" width="{round(height * SIG_RATIO)}" height="{height}" aria-hidden="true" focusable="false">'
            f'<use href="#sig" width="100%" height="100%"/></svg>')


def sig_signing(cls="sig sig--hero"):
    """The large signature for the frontispiece. A mask of the pen's centre lines draws it on, stroke by stroke."""
    c = SIG["centre"]
    ink = lambda k, d: f'<path class="sig__ink sig__ink--{k}" d="{d}" pathLength="1" fill="none" stroke="#fff" stroke-width="64" stroke-linecap="round" stroke-linejoin="round"/>'
    return (f'<svg class="{cls}" width="{round(120 * SIG_RATIO)}" height="120" viewBox="{SIG_VB}" role="img" aria-label="Dorian Bailey&rsquo;s signature">'
            f'<mask id="sig-pen" maskUnits="userSpaceOnUse" x="{_vb[0]}" y="{_vb[1]}" width="{_vb[2]}" height="{_vb[3]}">'
            f'{ink("main", c["main"])}{ink("hook", c["hook"])}{ink("underline", c["underline"])}</mask>'
            f'<path fill-rule="evenodd" mask="url(#sig-pen)" d="{SIG["refined_display"]}"/></svg>')


def thumb_dims(p):
    w, h = p["w"], p["h"]
    s = 900 / max(w, h)
    return round(w * s), round(h * s)


# Cryptid Highway lives behind the Mothman eyes in the footer. The markup waits in an inert
# <template>; js/main.js clones it into a dialog and loads js/game.js on the first sighting clicked.
GAME_TEMPLATE = """    <template id="cryptid-highway">
      <div class="game-dialog__head">
        <p class="game-dialog__title" id="game-dialog-title">Cryptid Highway</p>
        <button class="game-dialog__close" type="button" data-game-close>Close</button>
      </div>
      <div class="game" data-game>
        <div class="game__screen">
          <canvas tabindex="0" role="img" aria-label="Cryptid Highway, a night drive past cryptids"></canvas>
          <div class="game__panel" data-game-start>
            <p class="game__kicker">You saw something</p>
            <h3>Cryptid Highway</h3>
            <p>Take the two-lane road out after it. Jump the potholes, cones and deer in your headlights, and photograph Mothman, Bigfoot and the Frogman before they slip back into the dark. You have twenty-four shots of film.</p>
            <button class="btn" type="button" data-game-go autofocus>Start the drive</button>
          </div>
          <div class="game__panel" data-game-over hidden>
            <p class="game__kicker" data-o="cause">Trip over.</p>
            <h3><span data-o="score">0</span> points</h3>
            <p data-o="detail"></p>
            <p class="game__stop" data-o="stop" hidden>Up the road, you&rsquo;d have passed <a href="https://taketheoddway.com" rel="noopener">a real stop</a>, <span data-o="place"></span>.</p>
            <button class="btn" type="button" data-game-go>Drive again</button>
          </div>
        </div>
        <div class="game__controls">
          <button type="button" class="game__btn" data-game-jump>Jump <span>Space</span></button>
          <button type="button" class="game__btn" data-game-snap>Photograph <span>S</span></button>
        </div>
      </div>
    </template>"""


CHANGED = {}


def page(path, key, title, desc, body, extra_js="", og_image="assets/img/og-card.jpg", ld=None, crumb=None, noindex=False,
         og_type="website", head_extra=""):
    depth = path.count("/")
    p = "/" if path == "404.html" else "../" * depth
    canonical = SITE + "/" + path.replace("index.html", "")
    # Structured data: whatever the page passes, plus a breadcrumb trail for inner pages
    graph = list(ld or [])
    if crumb:
        # a name for a page one level down, or a list of (name, url) pairs for deeper pages
        trail = [("Dorian Bailey", SITE + "/")] + (crumb if isinstance(crumb, list) else [(crumb, canonical)])
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(trail, 1)]})
    ld_html = ("\n  <script type=\"application/ld+json\">" + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
               .replace("</", "<\\/") + "</script>") if graph else ""
    seo = ('  <meta name="robots" content="noindex">' if noindex else f'  <link rel="canonical" href="{canonical}">')
    home = p or "./"
    nav = "\n".join(
        f'          <li><a href="{home if href.startswith("#") else p}{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
        for href, label, k in NAV)
    out = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="author" content="Dorian Bailey">
  <meta name="color-scheme" content="light dark">
{seo}
  <meta property="og:site_name" content="Dorian Bailey">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/{og_image}?v={v(og_image)}">
  <meta property="og:image:alt" content="{html.escape(title)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#1c1b19">
  <link rel="icon" href="{p}favicon.ico?v={v('favicon.ico')}" sizes="48x48">
  <link rel="icon" href="{p}favicon.svg?v={v('favicon.svg')}" type="image/svg+xml">
  <link rel="icon" href="{p}favicon-32.png?v={v('favicon-32.png')}" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{p}apple-touch-icon.png?v={v('apple-touch-icon.png')}">
  <link rel="manifest" href="{p}site.webmanifest">
  <link rel="preload" href="{p}assets/fonts/libre-caslon-display-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{p}assets/fonts/libre-caslon-text-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{p}css/base.css?v={v('css/base.css')}">{head_extra}{ld_html}
</head>
<body>
  {SIG_SPRITE}
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap site-header__inner">
      <a class="site-mark" href="{home}">
        {sig(28)}
        <span>Dorian Bailey</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <button class="mothman" type="button" tabindex="-1" aria-hidden="true" data-game-src="{p}js/game.js?v={v('js/game.js')}"><i></i><i></i></button>
{GAME_TEMPLATE}
    <div class="wrap site-footer__inner">
      <div class="site-footer__mark">
        {sig(44, "sig sig--deboss")}
        <p>The Collection of Dorian Bailey<br><em>North East, Pennsylvania</em></p>
      </div>
      <ul class="site-footer__links">
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{LINKS['linkedin']}" rel="noopener">LinkedIn</a></li>
        <li><a href="{LINKS['ig']}" rel="noopener">Instagram <em>@baileymetazoo</em></a></li>
        <li><a href="{LINKS['yt']}" rel="noopener">YouTube <em>@baileymetazoo</em></a></li>
        <li><a href="{LINKS['github']}" rel="noopener">GitHub</a></li>
        <li><a href="{p}journal/"{" aria-current=\"page\"" if key == "journal" else ""}>Journal</a></li>
      </ul>
      <p class="site-footer__fine">&copy; <span data-year>2026</span> Dorian Bailey. Photographs are the author&rsquo;s own. <a href="{p}privacy/">Privacy</a></p>
    </div>
  </footer>

  <script src="{p}js/main.js?v={v('js/main.js')}" defer></script>
  <script src="{p}js/book.js?v={v('js/book.js')}" data-to="{EMAIL}" data-to-estate="{BSWB_EMAIL}" data-form="{FORM_ID}" data-form-estate="{FORM_ID_ESTATE}" data-privacy="{p}privacy/" data-photo-types="{html.escape('|'.join(t for t, _ in PHOTO_TYPES))}" defer></script>
{extra_js}</body>
</html>
"""
    f = ROOT / path
    CHANGED[path] = not f.exists() or f.read_text() != out    # for honest sitemap dates
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(out)
    print("wrote", path)


def srcset(ph, prefix="", full=False):
    """The sizes of a photo, smallest first: small (520px long side), thumbnail (900px), optionally full.
    With a sizes attribute, the browser downloads only the smallest one that will look sharp."""
    def wide(long):
        return round(ph["w"] * min(1, long / max(ph["w"], ph["h"])))
    base = prefix + "assets/photos/"
    out = [f'{base}{ph["thumb"].replace("/t-", "/s-")} {wide(520)}w', f'{base}{ph["thumb"]} {wide(900)}w']
    if full:
        out.append(f'{base}{ph["file"]} {ph["w"]}w')
    return ", ".join(out)


PORTRAIT_SET = "{p}assets/img/s-dorian-bailey.jpg 390w, {p}assets/img/dorian-bailey.jpg 900w"
SIZES_PLATE = "(max-width: 640px) 46vw, 330px"


def plate(src_thumb, alt, w, h, caption, href=None, prefix="", ph=None, sizes=SIZES_PLATE):
    ss = f' srcset="{srcset(ph, prefix)}" sizes="{sizes}"' if ph else ""
    img = f'<img src="{prefix}{src_thumb}"{ss} alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    inner = f'<a href="{href}">{img}</a>' if href else img
    return f"""<figure class="plate">
            <div class="frame">{inner}</div>
            <figcaption>{caption}</figcaption>
          </figure>"""


def photo(cid, n):
    ph = COLL[cid]["photos"][n - 1]
    w, h = thumb_dims(ph)
    return ph, w, h


# ---------------------------------------------------------------- Home collage
HERO = json.load(open(ROOT / "assets/photos/hero.json"))
ROWS, ROW_H, GAP, SPEED = 5, 190, 12, 40   # row height in px at desktop, px/second


def collage():
    rows = [HERO[i::ROWS] for i in range(ROWS)]
    out = []
    for r, items in enumerate(rows):
        # Each set is repeated so it is wider than any screen; the track holds two sets and slides by one.
        one = items * 2
        set_w = sum(round(it["w"] * ROW_H / it["h"]) + GAP for it in one)
        dur = round(set_w / SPEED)
        imgs = "".join(f'<img src="assets/photos/{it["file"]}" alt="" width="{it["w"]}" height="{it["h"]}" decoding="async">' for it in one)
        rev = " collage__row--rev" if r % 2 else ""
        out.append(f'          <div class="collage__row{rev}" style="--dur: {dur}s"><div class="collage__track">{imgs}{imgs}</div></div>')
    return "\n".join(out)


# ===================================================================== Home
ENTRIES = [
    ("I", "better-selling/", "Better Selling With Bailey", "Estate sales in Erie County"),
    ("II", "oddway/", "Take The OddWay", "A road-trip guide to the strange"),
    ("III", "metazoo/", "Bailey MetaZoo", "Cryptids and trading cards"),
    ("IV", "photography/", "Photography", "Commissions and collections"),
    ("V", "record/", "The Record", "Education, positions and ventures"),
]

contents = "\n".join(f"""          <li>
            <a href="{href}">
              <span class="contents__num">{num}</span>
              <span class="contents__title">{title}</span>
              <span class="contents__leader" aria-hidden="true"></span>
              <span class="contents__desc">{desc}</span>
            </a>
          </li>""" for num, href, title, desc in ENTRIES)

selected = []
for cid, n, cap in [("letchworth", 7, "Letchworth"), ("creatures", 4, "Creatures"),
                    ("north-east", 5, "North East"), ("studies", 6, "Studies")]:
    ph, w, h = photo(cid, n)
    selected.append(plate("assets/photos/" + ph["thumb"], ph["alt"], w, h,
                          f"<em>{cap}</em>", href=f"photography/#{cid}", ph=ph, sizes="(max-width: 640px) 46vw, 250px"))
selected = "\n          ".join(selected)

FEAT = COLL["legends"]["photos"][25]

EVENTS = [("legends", "Legends Expo", "MetaZoo $10,000 cash tournament, Monroeville, Pennsylvania, August 2026"),
          ("mothman", "Mothman Festival", "Point Pleasant, West Virginia, September 2026"),
          ("green-eyes", "Green Eyes Festival", "Chickamauga, Georgia, October 2026")]


def events_list(prefix):
    return "\n".join(f'            <li><a href="{prefix}#{cid}">{t}</a> <em>{m}</em></li>' for cid, t, m in EVENTS)


NOW = [
    ("Studying", "Marketing and Management Information Systems at Penn State Behrend, class of 2027."),
    ("Working", f'Marketing assistant at <a href="{LINKS["vanta"]}" rel="noopener">Vanta House</a>: content strategy, social campaigns and SEO for client brands.'),
    ("Running", '<a href="better-selling/">Better Selling With Bailey</a>, booking estate sales across Erie County.'),
    ("Building", '<a href="oddway/">Take The OddWay</a>, with an events listing for cryptid festivals next on the roadmap.'),
    ("Photographing", '<a href="photography/">Events for MetaZoo TCG</a>, three so far this year.'),
    ("Filming", '<a href="metazoo/">Bailey MetaZoo</a>: short films on cryptid lore and the cards behind it.'),
]
now_rows = "\n".join(f"""          <div class="ledger__row">
            <dt>{k}</dt>
            <dd><p>{v}</p></dd>
          </div>""" for k, v in NOW)

SERVICES = f"""
    <section class="section services" id="services" aria-labelledby="services-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="services-title">Services</h2>
          <p class="section-head__note">Choose a date and Dorian Bailey will confirm by email</p>
        </div>
        <div class="services__grid">
          <article class="service">
            <p class="service__kicker">Photography</p>
            <h3><a href="photography/">Dorian Bailey Photography</a></h3>
            <p class="service__status">Bookings available now</p>
            <p>All types of photography offered, from events and festivals to portraits, seniors, families, products and real estate. Inquire for rates.</p>
            <details class="service__more">
              <summary>Photography offered <span>{len(PHOTO_TYPES)}</span></summary>
              <ul class="service__list">
{chr(10).join(f"                <li>{t}</li>" for t, _ in PHOTO_TYPES)}
              </ul>
            </details>
            <div class="btn-row"><button class="btn" type="button" data-book="photo">Book now</button><a class="btn" href="{html.escape(MAILTO_PHOTO)}">Inquire for rates</a></div>
          </article>
          <article class="service">
            <p class="service__kicker">Estate sales</p>
            <h3><a href="better-selling/">Better Selling With Bailey</a></h3>
            <p class="service__status">Bookings available now</p>
            <p>Estate sales across Erie County, priced, staged, promoted and run by Dorian Bailey in your own home, with whatever is left removed free. A $995 flat fee plus 20% of sales.</p>
            <details class="service__more">
              <summary>Services offered <span>5</span></summary>
              <ul class="service__list">
                <li>Walkthrough and pricing</li>
                <li>Staging</li>
                <li>Promotion</li>
                <li>Running the sale days</li>
                <li>Cleanup and removal</li>
              </ul>
            </details>
            <div class="btn-row"><button class="btn" type="button" data-book="estate">Book now</button><a class="btn" href="{html.escape(MAILTO_BSWB)}">Email me</a></div>
          </article>
          <article class="service">
            <p class="service__kicker">Advertising</p>
            <h3><a href="oddway/#advertise">Advertise on Take The OddWay</a></h3>
            <p class="service__status">Bookings available now</p>
            <p>Banner and featured map placements on OddWay for brands that fit the road it maps: roadside attractions, small museums, diners and motels, festivals and haunted tours, and makers of strange things.</p>
            <details class="service__more">
              <summary>Placements offered <span>2</span></summary>
              <ul class="service__list">
                <li>Banner on the home and stop pages</li>
                <li>Featured marker on the map</li>
              </ul>
              <p class="service__fine">Seen by people planning a detour. Listings themselves are never for sale.</p>
            </details>
            <div class="btn-row"><button class="btn" type="button" data-book="ads">Book a call</button><a class="btn" href="{LINKS['oddway_ads']}" rel="noopener">Advertising options</a></div>
          </article>
        </div>
      </div>
    </section>
"""

page("index.html", "home",
     "Dorian Bailey | Photography and Estate Sales in Erie, PA",
     "Dorian Bailey offers all types of photography and runs estate sales across Erie County, PA, and builds Take The OddWay and Bailey MetaZoo. Inquire for rates.",
     f"""    <section class="frontispiece">
      <div class="collage" aria-hidden="true">
        <div class="collage__wall">
{collage()}
        </div>
      </div>
      <div class="wrap frontispiece__inner">
        {sig_signing()}
        <p class="frontispiece__pre">The Collection of</p>
        <h1>Dorian Bailey</h1>
        <p class="frontispiece__sub">Photography, estate sales and ventures<br>from North East, Pennsylvania</p>
      </div>
    </section>
{SERVICES}
    <section class="section" aria-labelledby="feature-title">
      <div class="wrap feature">
        <figure class="feature__media">
          <a class="frame" href="photography/#legends"><img src="assets/photos/{FEAT['file']}" srcset="{srcset(FEAT, full=True)}" sizes="(max-width: 900px) 92vw, 620px" alt="{html.escape(FEAT['alt'])}" width="{FEAT['w']}" height="{FEAT['h']}" decoding="async"></a>
        </figure>
        <div class="feature__card">
          <p class="feature__kicker">Featured commission</p>
          <h2 id="feature-title">MetaZoo TCG, 2026</h2>
          <p>Dorian Bailey photographed three events in three months for MetaZoo TCG: the $10,000 cash tournament at the Legends Expo Card Show in Monroeville, the Mothman Festival and the Green Eyes Festival. Players at the tables, prize cards on their easels, costumed cryptids, and the crowds that came to see them.</p>
          <ul class="events">
{events_list("photography/")}
          </ul>
          <div class="btn-row"><a class="btn" href="photography/">See the commissions</a></div>
        </div>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="foreword-title">
      <div class="wrap foreword">
        <figure class="plate foreword__portrait">
          <div class="frame"><img src="assets/img/dorian-bailey.jpg" srcset="{PORTRAIT_SET.format(p='')}" sizes="(max-width: 900px) 92vw, 340px" alt="Portrait of Dorian Bailey" width="900" height="1200" loading="lazy" decoding="async"></div>
        </figure>
        <div class="foreword__text">
          <h2 class="section-title" id="foreword-title">Foreword</h2>
          <p class="lede">Born and raised in North East, Pennsylvania, I study Marketing and Management Information Systems at Penn State Behrend.</p>
          <p>Long before I started a business, I spent years buying, selling, researching and pricing things of every kind. That became Better Selling With Bailey. A taste for the strange side of the map became Take The OddWay, and a love of cryptid lore and collecting became Bailey MetaZoo. Somewhere along the way I picked up a camera, and now photograph events for MetaZoo TCG.</p>
          <p>By day I&rsquo;m a marketing assistant at <a href="{LINKS['vanta']}" rel="noopener">Vanta House</a>, a video-first content studio here in North East. This site gathers the rest: the work I&rsquo;m paid for and the work I&rsquo;d do anyway.</p>
          <p class="foreword__sign">{sig(40)}<span>Dorian Bailey</span></p>
          <p><a class="text-link" href="record/">Read the record</a></p>
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="now-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="now-title">Now</h2>
          <p class="section-head__note">What fills the week, as of October 2026</p>
        </div>
        <dl class="ledger ledger--wide">
{now_rows}
        </dl>
      </div>
    </section>

    <section class="section band--dark" aria-labelledby="plates-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="plates-title">Selected plates</h2>
          <a class="text-link" href="photography/">All {TOTAL} photographs</a>
        </div>
        <div class="plate-row">
          {selected}
        </div>
      </div>
    </section>

    <section class="section" id="index" aria-labelledby="index-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="index-title">Index</h2>
        <ol class="contents">
{contents}
        </ol>
      </div>
    </section>

    <section class="correspondence band--raised" id="correspondence" aria-labelledby="corr-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="corr-title">Correspondence</h2>
        <p>For photography, an estate sale, advertising on OddWay or a collaboration, write to me directly, or book a date.</p>
        <p class="correspondence__email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <div class="btn-row"><button class="btn" type="button" data-book="photo">Book a photo shoot</button><button class="btn" type="button" data-book="estate">Request an estate sale</button><button class="btn" type="button" data-book="ads">Advertise on OddWay</button></div>
        <p class="correspondence__more">Also on <a href="{LINKS['linkedin']}" rel="noopener">LinkedIn</a>. More on the estate sales at <a href="{LINKS['bswb']}" rel="noopener">bettersellingwithbailey.com</a>.</p>
      </div>
    </section>""", ld=[WEBSITE, PERSON, PHOTO_SERVICE])


# ===================================================================== Entries (venture pages)
ORDER = [("better-selling", "I", "Better Selling With Bailey"),
         ("oddway", "II", "Take The OddWay"),
         ("metazoo", "III", "Bailey MetaZoo"),
         ("photography", "IV", "Photography")]


def entry(slug, key, title, desc, standfirst, prose, particulars, plates, links, head_print=None, extra="", js=None,
          seo_title=None, ld=None):
    idx = [o[0] for o in ORDER].index(slug)
    num = ORDER[idx][1]
    prev_ = ORDER[idx - 1] if idx > 0 else None
    next_ = ORDER[idx + 1]
    parts = "\n".join(f"            <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in particulars)
    lk = "\n".join(f'          <button class="btn" type="button" data-book="{h[5:]}">{t}</button>' if h.startswith("book:")
                   else f'          <a class="btn" href="{h}" rel="noopener">{t}</a>' for t, h in links)
    nav = []
    if prev_:
        nav.append(f'<a class="entry-nav__prev" href="../{prev_[0]}/"><em>Previous</em> {prev_[1]}. {prev_[2]}</a>')
    else:
        nav.append('<a class="entry-nav__prev" href="../#index"><em>Back to</em> the index</a>')
    nav.append(f'<a class="entry-nav__next" href="../{next_[0]}/"><em>Next</em> {next_[1]}. {next_[2]}</a>')

    if head_print:
        src, alt, w, h, ss = head_print
        head = f"""    <header class="entry-head entry-head--figure">
      <div class="wrap">
        <div class="entry-head__text">
          <p class="entry-head__num">No. {num}</p>
          <h1>{title}</h1>
          <p class="entry-head__standfirst">{standfirst}</p>
        </div>
        <figure class="entry-head__print">
          <div class="frame"><img src="{src}" srcset="{ss}" sizes="(max-width: 900px) 320px, 420px" alt="{html.escape(alt)}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div>
        </figure>
      </div>
    </header>"""
    else:
        head = f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. {num}</p>
        <h1>{title}</h1>
        <p class="entry-head__standfirst">{standfirst}</p>
      </div>
    </header>"""

    plates_html = ""
    if plates:
        pl = "\n          ".join(plates)
        plates_html = f"""
    <section class="section band--dark" aria-label="Plates">
      <div class="wrap">
        <div class="plate-row plate-row--{len(plates)}">
          {pl}
        </div>
      </div>
    </section>
"""

    page(f"{slug}/index.html", key, seo_title or f"{title} | Dorian Bailey", desc, ld=[PERSON] + (ld or []), crumb=title,
         og_image=f"assets/img/og-{slug}.jpg", extra_js=(f'  <script src="../js/{js}?v={v("js/" + js)}" defer></script>\n' if js else ""), body=f"""{head}

    <section class="section">
      <div class="wrap entry">
        <div class="entry__prose">
{prose}
          <div class="btn-row">
{lk}
          </div>
        </div>
        <aside class="particulars" aria-labelledby="particulars-title">
          <h2 id="particulars-title">Particulars</h2>
          <dl>
{parts}
          </dl>
        </aside>
      </div>
    </section>
{extra}{plates_html}
    <nav class="wrap entry-nav" aria-label="Collection">
      {nav[0]}
      {nav[1]}
    </nav>""")


def P(cid, n, cap, link=True):
    ph, w, h = photo(cid, n)
    return plate("assets/photos/" + ph["thumb"], ph["alt"], w, h, cap,
                 href=f"../photography/#{cid}" if link else None, prefix="../", ph=ph)


def HP(cid, n):
    ph = COLL[cid]["photos"][n - 1]
    return ("../assets/photos/" + ph["file"], ph["alt"], ph["w"], ph["h"], srcset(ph, "../", full=True))


def steps(items):
    return "\n".join(f"""          <li>
            <h3>{t}</h3>
            <p>{d}</p>
          </li>""" for t, d in items)


# ---------------------------------------------------------------- I. Better Selling With Bailey
BSWB_STEPS = [
    ("Walkthrough and pricing", "I assess everything in the home and price it to sell, with you as involved in the decisions as you like."),
    ("Staging", "Rooms are organized and merchandise is laid out so buyers can browse easily and find what they came for."),
    ("Promotion", "Listings, Facebook events and local outreach bring the right buyers to the door, whatever the weather."),
    ("Sale days", "I run the floor: every customer, every sale and every question. You don&rsquo;t need to be there unless you want to be."),
    ("Cleanup", "Teardown at the end of the sale, and free removal of whatever is left if you want it gone."),
    ("Proceeds", "The earnings go to you, minus the flat fee and commission agreed before the sale began."),
]
SELLS = ["Clothing collections", "Toys and LEGO", "Video games and electronics", "Antiques and vintage",
         "Sports cards and collectibles", "Trading card collections", "Household goods", "Tools and equipment"]

ES = json.load(open(ROOT / "assets/photos/estate-sales.json"))
ES_CAPS = ["A collector&rsquo;s garage, staged", "Tables down the side of the house", "The line before opening, in the rain",
           "The local news, filming the sale", "Boxed figures by the hundred", "A wet day, and still a crowd"]
es_plates = "\n          ".join(plate("assets/photos/" + ph["thumb"], ph["alt"], *thumb_dims(ph), f"<em>{cap}</em>", prefix="../", ph=ph,
                                     sizes="(max-width: 640px) 46vw, 360px")
                               for ph, cap in zip(ES["photos"], ES_CAPS))

bswb_extra = f"""
    <section class="section band--dark" aria-labelledby="sales-photos-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="sales-photos-title">From the sales</h2>
          <p class="section-head__note">A Better Selling With Bailey collector&rsquo;s sale in North East. Photographs by clients Ben and Andy Nagle, from their Google reviews.</p>
        </div>
        <div class="plate-row plate-row--3 plate-row--sales">
          {es_plates}
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="process-title">
      <div class="wrap">
        <h2 class="section-title" id="process-title">How a sale works</h2>
        <p class="section-intro">Every sale is hosted at the client&rsquo;s home in Erie County and handled start to finish. The journal has <a href="../journal/how-estate-sales-work-erie-county/">the whole process, with the fees worked out</a>.</p>
        <ol class="steps">
{steps(BSWB_STEPS)}
        </ol>
      </div>
    </section>

    <section class="section band--dark" aria-labelledby="calc-title">
      <div class="wrap split calc" data-calc data-fee="995" data-rate="0.2">
        <div>
          <h2 class="section-title" id="calc-title">What would I keep?</h2>
          <p class="section-intro">Slide to what you think your sale might bring in. The math uses the standard terms: a $995 flat fee and 20% of total sales.</p>
          <label class="calc__label" for="calc-total">Estimated total sales</label>
          <div class="calc__input">
            <span aria-hidden="true">$</span>
            <input id="calc-total" type="text" inputmode="numeric" autocomplete="off" value="10,000">
          </div>
          <input class="calc__range" type="range" min="2000" max="40000" step="250" value="10000" aria-label="Estimated total sales" data-calc-range>
          <div class="calc__presets">
            <button type="button" data-calc-preset="8000">$8,000 <em>a past weekend</em></button>
            <button type="button" data-calc-preset="16000">$16,000 <em>the best weekend so far</em></button>
          </div>
        </div>
        <div class="calc__result" aria-live="polite">
          <p class="calc__kicker">You would keep</p>
          <p class="calc__big" data-calc-out="keep">$7,005</p>
          <dl class="calc__lines">
            <div><dt>Total sales</dt><dd data-calc-out="total">$10,000</dd></div>
            <div><dt>Commission, 20%</dt><dd data-calc-out="commission">&minus;$2,000</dd></div>
            <div><dt>Flat fee</dt><dd>&minus;$995</dd></div>
          </dl>
          <p class="calc__note" data-calc-out="note">An estimate, not a quote. Removal of whatever is left is free either way.</p>
          <div class="btn-row"><button class="btn" type="button" data-book="estate">Book now</button></div>
        </div>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="clients-title">
      <div class="wrap split">
        <div>
          <h2 class="section-title" id="clients-title">From clients</h2>
          <div class="quotes quotes--stack">
            <blockquote class="quote">
              <p>Everything was done for me. Great turnout for the sale. Was better than I hoped for. The local TV station even came out and did a story on the sale.</p>
              <cite>Andy N., Google review</cite>
            </blockquote>
            <blockquote class="quote">
              <p>Ran a giant garage sale for me and it went off without a hitch. Great advertising and phenomenal work setting things up and execution of the sale.</p>
              <cite>Ben N., Google review</cite>
            </blockquote>
            <blockquote class="quote">
              <p>Hands down the best! The weekend sale was such a success. Will be using them again for my future sale events.</p>
              <cite>Juan G., Google review</cite>
            </blockquote>
            <blockquote class="quote">
              <p>Dorian&rsquo;s great. He&rsquo;s very understanding and knowledgeable about whatever he is selling.</p>
              <cite>Zane S., Google review</cite>
            </blockquote>
          </div>
          <p class="quotes__more"><a href="https://www.google.com/search?q=Better%20Selling%20With%20Bailey%20reviews" rel="noopener">Rated 5.0 from six reviews on Google</a></p>
        </div>
        <div>
          <h2 class="section-title">What sells</h2>
          <p class="section-intro">The categories that consistently draw buyers at Erie County sales.</p>
          <ul class="events cols-2">
{chr(10).join(f"            <li>{s}</li>" for s in SELLS)}
          </ul>
          <h3 class="subhead">In the press</h3>
          <p><a href="{LINKS['erie']}" rel="noopener">YourErie.com, May 2026.</a> A Star Wars collector&rsquo;s sale in North East drew an eager crowd through heavy rain and wind, for a collection of action figures, books and sealed LEGO sets. <a href="../journal/star-wars-collectors-sale-north-east/">More on the sale</a>.</p>
        </div>
      </div>
    </section>
"""

entry("better-selling", "selling", "Better Selling With Bailey",
      "Better Selling With Bailey is Dorian Bailey's estate sale company in Erie County, PA: pricing, staging, promotion and the sale itself, for a $995 flat fee plus 20%.",
      "Estate sales in Erie County, run start to finish by Dorian Bailey, so the people selling keep the proceeds. Bookings available now.",
      """          <p>Better Selling With Bailey prices, stages, promotes and runs estate sales in the client&rsquo;s own home, then clears whatever is left at no charge. Many clients treat it as a cleanout of a garage, basement or collection that happens to pay.</p>
          <p>Every client works with me directly, from the first walkthrough to the last sale of the day. Some like to be involved in every pricing decision; others would rather hand the whole thing over. Either works.</p>""",
      [("Established", "May 2026, North East, Pennsylvania"),
       ("Region", "Erie County"),
       ("Role", "Founder and owner"),
       ("Client sales", "More than $35,000"),
       ("Top events", "More than $16,000 and $8,000, each in a single weekend"),
       ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
       ("Email", f'<a href="mailto:{BSWB_EMAIL}">{BSWB_EMAIL}</a>'),
       ("Bookings", "Available now"),
       ("Press", f'<a href="{LINKS["erie"]}" rel="noopener">YourErie.com, May 2026</a>')],
      [],
      [("Book now", "book:estate"), ("Email me", MAILTO_BSWB), ("Facebook", LINKS["bswb_fb"])],
      head_print=("../assets/img/dorian-bailey.jpg", "Dorian Bailey in a Better Selling With Bailey polo", 900, 1200, PORTRAIT_SET.format(p="../")),
      extra=bswb_extra, js="calc.js",
      seo_title="Erie Estate Sales by Dorian Bailey | Better Selling With Bailey", ld=[ESTATE_SERVICE])

# ---------------------------------------------------------------- II. Take The OddWay
ODD_STEPS = [
    ("Pick your route", "Give it a start and a finish. OddWay takes care of everything in between, including the two-lane roads you would never have chosen yourself."),
    ("Find strange stops", "Filter by what you actually want to see, then check how far each stop pulls you off course before you commit to it."),
    ("Take the OddWay", "Add the good ones to your trip, take the directions with you, and go stand in front of the thing."),
]
ODD_CATS = [
    ("Cryptids", "Creatures people keep reporting and nobody has caught."),
    ("Folklore", "Stories a place tells about itself, passed down and still repeated."),
    ("Haunted", "Hotels, theatres, prisons and back roads with a reputation."),
    ("UFOs", "Sighting sites, crash lore and the towns that kept the file open."),
    ("Weird history", "Real events too strange to have made the textbook."),
    ("Museums", "Small, specific collections run by people who care far too much."),
    ("Roadside oddities", "Giant objects, odd monuments and things built for no clear reason."),
]
odd_extra = f"""
    <section class="section section--rule" aria-labelledby="how-title">
      <div class="wrap">
        <h2 class="section-title" id="how-title">How it works</h2>
        <ol class="steps">
{steps(ODD_STEPS)}
        </ol>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="cats-title">
      <div class="wrap">
        <h2 class="section-title" id="cats-title">Seven kinds of strange</h2>
        <p class="section-intro">Every stop is filed under one of seven categories, so a trip can be all haunted hotels or all giant statues.</p>
        <dl class="glossary">
{chr(10).join(f"          <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in ODD_CATS)}
        </dl>
      </div>
    </section>

    <section class="section band--dark" aria-labelledby="detour-title">
      <div class="wrap detour" data-detour>
        <div class="detour__controls">
          <h2 class="section-title" id="detour-title">Roll a detour</h2>
          <p class="section-intro">One stop at a time, dealt live from OddWay&rsquo;s index of nearly 7,000 places. Pick a kind of strange, or leave it to chance.</p>
          <div class="chips" role="group" aria-label="Kind of stop">
            <button type="button" class="chip" data-cat="" aria-pressed="true">Any</button>
            <button type="button" class="chip" data-cat="cryptids" aria-pressed="false">Cryptids</button>
            <button type="button" class="chip" data-cat="folklore" aria-pressed="false">Folklore</button>
            <button type="button" class="chip" data-cat="haunted" aria-pressed="false">Haunted</button>
            <button type="button" class="chip" data-cat="ufos" aria-pressed="false">UFOs</button>
            <button type="button" class="chip" data-cat="weird-history" aria-pressed="false">Weird history</button>
            <button type="button" class="chip" data-cat="museums" aria-pressed="false">Museums</button>
            <button type="button" class="chip" data-cat="roadside-oddities" aria-pressed="false">Roadside oddities</button>
          </div>
          <div class="btn-row"><button type="button" class="btn" data-detour-roll>Roll a detour</button></div>
        </div>
        <article class="atlas" aria-live="polite" data-detour-card>
          <p class="atlas__cat" data-f="cat">Stop no. &mdash;</p>
          <h3 class="atlas__name" data-f="name">Somewhere strange</h3>
          <p class="atlas__place" data-f="place">Anywhere in the United States</p>
          <p class="atlas__desc" data-f="desc">Press the button and OddWay will deal you a real stop: a cryptid museum, a haunted inn, a ship parked on a bluff.</p>
          <p class="atlas__go"><a data-f="link" href="https://taketheoddway.com" rel="noopener">Open OddWay</a></p>
        </article>
      </div>
    </section>

    <section class="section band--raised section--rule" id="advertise" aria-labelledby="ads-title">
      <div class="wrap split">
        <div>
          <h2 class="section-title" id="ads-title">Advertise on OddWay</h2>
          <p class="section-intro">OddWay offers advertising for brands that fit the road it maps: roadside attractions, small museums, diners and motels, festivals and haunted tours, and makers of strange things. The people who see it are planning a detour and deciding which stops are worth the trip.</p>
          <p class="service__status">Bookings available now</p>
          <div class="btn-row"><button class="btn" type="button" data-book="ads">Book a call</button><a class="btn" href="{LINKS['oddway_ads']}" rel="noopener">See advertising options</a></div>
        </div>
        <dl class="glossary glossary--single">
          <div><dt>Banner placement</dt><dd>A banner on the home page and stop pages, with a link to your site and a line of text.</dd></div>
          <div><dt>Featured map placement</dt><dd>A marker on the OddWay map with your name, logo and description.</dd></div>
          <div><dt>Listings are never for sale</dt><dd>Advertising buys a placement, not a place in the index. Ads that don&rsquo;t fit the road are turned down.</dd></div>
        </dl>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="next-title">
      <div class="wrap split">
        <h2 class="section-title" id="next-title">Next on the road</h2>
        <div class="measure">
          <p>An events listing: cryptid festivals, haunted houses and seasonal mazes, sortable by distance from wherever you are.</p>
          <p>The hard part is the calendar. Most of these events follow a pattern, like the third weekend in September, rather than a fixed date, so each year&rsquo;s dates will be confirmed by hand. An event listed on the wrong weekend is worse than one not listed at all; nobody should drive four hours to an empty field.</p>
        </div>
      </div>
    </section>
"""

entry("oddway", "oddway", "Take The OddWay",
      "Take The OddWay is a road-trip discovery platform by Dorian Bailey for finding cryptids, folklore, haunted places and roadside oddities.",
      "A road-trip guide to the strange: cryptids, folklore, haunted places and roadside oddities along your route.",
      """          <p>Give OddWay a route and it finds the detours worth taking: Bigfoot sightings, local legends, haunted hotels, UFO landmarks, odd little museums and giant roadside statues.</p>
          <p>I designed and built it end to end, from the brand and the research behind every stop to the web app itself, written in Next.js and TypeScript on Supabase.</p>""",
      [("Founded by", "Dorian Bailey"),
       ("Subject", "Cryptids, folklore and roadside Americana"),
       ("Categories", "Seven"),
       ("Built with", "Next.js, React, TypeScript, Tailwind CSS, Supabase"),
       ("Advertising", f'<a href="{LINKS["oddway_ads"]}" rel="noopener">For brands that fit the road</a>'),
       ("Also", f'<a href="{LINKS["shop"]}" rel="noopener">The OddWay shop</a>')],
      [P("green-eyes", 5, "<em>Bigfoot, from Green Eyes</em>"),
       P("letchworth", 7, "<em>The gorge, from Letchworth</em>"),
       P("north-east", 2, "<em>Halloween, from North East</em>")],
      [("Visit taketheoddway.com", LINKS["oddway"]), ("Advertise on OddWay", LINKS["oddway_ads"]), ("Shop the OddWay", LINKS["shop"])],
      head_print=HP("green-eyes", 7),
      extra=odd_extra, js="detour.js",
      seo_title="Take The OddWay | A Road-Trip App by Dorian Bailey",
      ld=[{"@type": "WebApplication", "name": "Take The OddWay", "url": LINKS["oddway"], "applicationCategory": "TravelApplication",
           "operatingSystem": "Web", "description": "A road-trip guide to cryptids, folklore, haunted places and roadside oddities along your route.",
           "creator": {"@id": PERSON_ID}, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}])

# ---------------------------------------------------------------- III. Bailey MetaZoo
VHS = [
    ("The tape", "Hands slide a cassette into a VCR, shot moody and close, with the deck&rsquo;s clunk on the beat."),
    ("Warm-up", "An old CRT clicks on and warms to snow as the camera pushes toward the glass."),
    ("The logo", "A white flash, then the MetaZoo logo rolls down into place through fading static."),
    ("The flashes", "Five cards flash through the snow, each a little faster than the last."),
    ("The hero", "Tracking drops, a beat of dead air, then the hero card slams in with its own sound."),
    ("Switch-off", "The picture squeezes to a line, then a dot, and loops back to the start."),
]
YT = json.load(open(ROOT / "assets/data/youtube.json"))["videos"]
MON = ["JAN.", "FEB.", "MAR.", "APR.", "MAY", "JUNE", "JULY", "AUG.", "SEPT.", "OCT.", "NOV.", "DEC."]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def osd_date(d):
    y, m, dd = d.split("-")
    return f"{MON[int(m) - 1]} {int(dd)} {y}"


def long_date(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m) - 1]} {y}"


_SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", "of", "on", "or", "the", "to", "vs"}
_BRANDS = {"METAZOO": "MetaZoo", "TCG": "TCG", "UFO": "UFO", "UFOS": "UFOs", "VHS": "VHS"}


def tidy_title(t):
    """YouTube titles shout; the catalogue doesn't. All-caps titles become title case and all-caps
    words (SADDEST, GIVEAWAY) become capitalised, keeping brands and acronyms as they should be."""
    letters = [c for c in t if c.isalpha()]
    shouting = bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.6
    out = []
    for i, w in enumerate(t.split(" ")):
        core = "".join(c for c in w if c.isalpha())
        if core.isupper() and core in _BRANDS:
            out.append(w.replace(core, _BRANDS[core]))
        elif core.isupper() and (shouting or len(core) >= 4):
            low = w.lower()
            if shouting and i > 0 and core.lower() in _SMALL:
                out.append(low)
            else:
                k = next(j for j, c in enumerate(low) if c.isalpha())
                out.append(low[:k] + low[k].upper() + low[k + 1:])
        else:
            out.append(w)
    return " ".join(out)


for _v in YT:
    _v["title"] = tidy_title(_v["title"])

tapes = "\n".join(f"""            <li><button type="button" class="tape" data-id="{v['id']}" data-title="{html.escape(v['title'])}" data-date="{osd_date(v['published'])}" aria-pressed="{'true' if i == 0 else 'false'}">
              <span class="tape__title">{html.escape(v['title'])}</span>
              <span class="tape__date">{long_date(v['published'])}</span>
            </button></li>""" for i, v in enumerate(YT[:8]))
latest = YT[0]

mz_extra = f"""
    <section class="section band--dark" aria-labelledby="tv-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="tv-title">Now playing</h2>
          <a class="text-link" href="{LINKS['yt']}" rel="noopener">The channel on YouTube</a>
        </div>
        <div class="tv-set">
          <div class="tv" data-tv>
            <div class="tv__cabinet">
              <div class="tv__screen">
                <canvas class="tv__static" width="160" height="120" aria-hidden="true"></canvas>
                <div class="tv__player" data-tv-player></div>
                <div class="tv__osd" aria-hidden="true"><span class="tv__osd-tl" data-tv-state>STOP &#9632;</span><span class="tv__osd-bl" data-tv-date>{osd_date(latest['published'])}</span></div>
                <button class="tv__insert" type="button" data-tv-insert>Insert tape</button>
              </div>
              <div class="tv__panel" aria-hidden="true"><span class="tv__knob"></span><span class="tv__knob tv__knob--small"></span><span class="tv__grille"></span></div>
            </div>
            <p class="tv__now"><em>On the tape</em> <span data-tv-title>{html.escape(latest['title'])}</span></p>
            <p class="tv__note">Plays from YouTube, which may set cookies once a tape is playing. <a href="../privacy/">Privacy</a></p>
          </div>
          <div class="tv-guide">
            <p class="tv-guide__head">Tapes, newest first</p>
            <ol class="tapes">
{tapes}
            </ol>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="vhs-title">
      <div class="wrap">
        <h2 class="section-title" id="vhs-title">The VHS reveal</h2>
        <p class="section-intro">The signature format: an eighteen-second vertical film built to loop, shot on real tape-deck and television footage.</p>
        <ol class="steps">
{steps(VHS)}
        </ol>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="assign-title">
      <div class="wrap split">
        <h2 class="section-title" id="assign-title">On assignment</h2>
        <div>
          <p class="section-intro">Event photography for MetaZoo TCG itself.</p>
          <ul class="events">
{events_list("../photography/")}
          </ul>
        </div>
      </div>
    </section>
"""

entry("metazoo", "metazoo", "Bailey MetaZoo",
      "Bailey MetaZoo is Dorian Bailey's YouTube and Instagram channel on MetaZoo, the cryptid trading card game, and the folklore behind it.",
      "Short films on MetaZoo, the cryptid trading card game, and the folklore behind its cards.",
      """          <p>MetaZoo is a trading card game built from cryptids, folklore and the paranormal. Bailey MetaZoo covers the game and the legends it draws on: the Squonk, the Loveland Frogman, Old Scratch, and which cryptid haunts your state.</p>
          <p>Alongside the lore there are new set releases, pack openings and giveaways. Off camera, I photograph events for MetaZoo TCG itself.</p>""",
      [("Platforms", f'<a href="{LINKS["yt"]}" rel="noopener">YouTube</a> and <a href="{LINKS["ig"]}" rel="noopener">Instagram</a>'),
       ("Handle", "@baileymetazoo"),
       ("Subject", "MetaZoo and cryptid folklore"),
       ("Format", "Short vertical video"),
       ("Role", "Creator, host and editor"),
       ("Also", '<a href="../photography/">Event photographer for MetaZoo TCG</a>')],
      [P("mothman", 3, "<em>A signed print, from Mothman Festival</em>"),
       P("legends", 25, "<em>The Loveland Frogman, from Legends</em>"),
       P("green-eyes", 14, "<em>A MetaZoo card, from Green Eyes</em>")],
      [("Watch on YouTube", LINKS["yt"]), ("Follow on Instagram", LINKS["ig"])],
      head_print=HP("legends", 2),
      extra=mz_extra, js="tv.js",
      seo_title="Bailey MetaZoo | MetaZoo TCG Videos by Dorian Bailey",
      ld=[{"@type": "CreativeWorkSeries", "name": "Bailey MetaZoo", "url": LINKS["yt"], "sameAs": [LINKS["yt"], LINKS["ig"]],
           "about": "MetaZoo, the cryptid trading card game, and the folklore behind its cards", "creator": {"@id": PERSON_ID}}])

# ===================================================================== Photographs
index_items, sections = [], []
running = 0
for c in M["collections"]:
    cov = next(p for p in c["photos"] if p["thumb"] == c["cover"])
    w, h = thumb_dims(cov)
    n = len(c["photos"])
    index_items.append((bool(c.get("commission")), f"""          <li>
            <a href="#{c['id']}">
              <span class="frame"><img src="../assets/photos/{c['cover']}" srcset="{srcset(cov, '../')}" sizes="(max-width: 640px) 44vw, 240px" alt="" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
              <span class="coll-index__num">{c['numeral']}</span>
              <span class="coll-index__title">{c['title']}</span>
              <span class="coll-index__meta">{c['place']}<br>{c['date']}, {n} plates</span>
            </a>
          </li>"""))
    figs = []
    for i, ph in enumerate(c["photos"], 1):
        tw, th = thumb_dims(ph)
        figs.append(f"""          <figure class="plate">
            <button class="frame" type="button" data-full="../assets/photos/{ph['file']}" data-caption="{c['title']}, plate {i} of {n}">
              <img src="../assets/photos/{ph['thumb']}" srcset="{srcset(ph, '../')}" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 30vw, 340px" alt="{html.escape(ph['alt'])}" width="{tw}" height="{th}" loading="lazy" decoding="async">
            </button>
          </figure>""")
    sections.append(f"""    <section class="collection section--rule" id="{c['id']}" aria-labelledby="{c['id']}-title">
      <div class="wrap">
        <header class="collection__head">
          <p class="collection__num">{c['numeral']}</p>
          <div>
            <h2 id="{c['id']}-title">{c['title']}</h2>
            <p class="collection__meta">{('Commissioned by ' + c['commission'] + '. ') if c.get('commission') else ''}{c['place']}, {c['date']}. {n} plates.</p>
            <p class="collection__note">{c['note']}</p>
            <p class="collection__up"><a href="#collections-title">All collections</a></p>
          </div>
        </header>
        <div class="gallery" data-collection>
{chr(10).join(figs)}
        </div>
      </div>
    </section>""")

BANNER = COLL["letchworth"]["photos"][1]

page("photography/index.html", "photo", "Dorian Bailey Photography | Photographer in Erie, PA",
     "Dorian Bailey Photography: all types of photography in Erie County, PA, from events and portraits to seniors, families, products and real estate. Inquire for rates.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. IV</p>
        <h1>Dorian Bailey Photography</h1>
        <p class="entry-head__standfirst">All types of photography offered, from events and festivals to portraits, families, products and real estate. Based in North East, Pennsylvania. Inquire for rates.</p>
        <p class="service__status">Bookings available now</p>
        <div class="btn-row"><button class="btn" type="button" data-book="photo">Book now</button><a class="btn" href="{html.escape(MAILTO_PHOTO)}">Inquire for rates</a><a class="btn" href="#types">What I photograph</a></div>
      </div>
    </header>

    <figure class="banner">
      <div class="banner__clip"><img src="../assets/photos/{BANNER['file']}" srcset="{srcset(BANNER, '../', full=True)}" sizes="100vw" alt="{html.escape(BANNER['alt'])}" width="{BANNER['w']}" height="{BANNER['h']}" fetchpriority="high" decoding="async"></div>
      <figcaption class="wrap"><em>Letchworth State Park, New York, October 2026. Photograph by Dorian Bailey.</em></figcaption>
    </figure>

    <section class="section" id="types" aria-labelledby="types-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="types-title">All types of photography</h2>
          <p class="section-head__note">Inquire for rates</p>
        </div>
        <dl class="glossary">
{chr(10).join(f"          <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in PHOTO_TYPES)}
        </dl>
        <div class="btn-row"><button class="btn" type="button" data-book="photo">Book now</button><a class="btn" href="{html.escape(MAILTO_PHOTO)}">Inquire for rates</a></div>
        <p class="services__note">Dorian Bailey is based in North East, Pennsylvania, photographs across Erie County, and travels for events.</p>
      </div>
    </section>

    <section class="section band--dark" aria-labelledby="commissions-title">
      <div class="wrap">
        <h2 class="section-title" id="commissions-title">Commissions</h2>
        <dl class="ledger">
          <div class="ledger__row">
            <dt>Event photographer</dt>
            <dd>
              <h3>MetaZoo TCG</h3>
              <p>Professional coverage of MetaZoo TCG at tournaments and cryptid festivals: players at the tables, the cards they pull, costumed cryptids, and the crowds that come to see them.</p>
              <ul class="events">
                <li><a href="#legends">Legends Expo</a> <em>MetaZoo $10,000 cash tournament, Monroeville, Pennsylvania, August 2026</em></li>
                <li><a href="#mothman">Mothman Festival</a> <em>Point Pleasant, West Virginia, September 2026</em></li>
                <li><a href="#green-eyes">Green Eyes Festival</a> <em>Chickamauga, Georgia, October 2026</em></li>
              </ul>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Marketing assistant <em>since June 2026</em></dt>
            <dd>
              <h3><a href="{LINKS['vanta']}" rel="noopener">Vanta House</a></h3>
              <p>A video-first content studio in North East, Pennsylvania, that turns one long-form film a month into a full system of content for its clients. I support content strategy, social campaigns and SEO across client accounts, and work alongside the team on shoots and video production.</p>
            </dd>
          </div>
        </dl>
      </div>
    </section>

    <section class="section" aria-labelledby="approach-title">
      <div class="wrap">
        <div class="measure">
          <h2 class="section-title" id="approach-title">Approach</h2>
          <p class="lede">Most of this is event work: long days on a festival street or a tournament floor, close to the people and the cards.</p>
          <p>The personal collections are where the slower pictures live: a gorge in October, a cat in window light, fungi on a fallen log.</p>
          <p>From the journal: <a href="../journal/legends-expo-metazoo-tournament/">photographing the MetaZoo $10,000 tournament</a>, and <a href="../journal/senior-pictures-erie-county/">where to take senior pictures in Erie County</a>.</p>
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="collections-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="collections-title">Collections</h2>
          <p class="section-head__note">{TOTAL} photographs by Dorian Bailey in {NUMWORD.lower()} collections</p>
        </div>
        <h3 class="coll-group">Commissioned by MetaZoo TCG</h3>
        <ol class="coll-index">
{chr(10).join(item for comm, item in index_items if comm)}
        </ol>
        <h3 class="coll-group">Personal</h3>
        <ol class="coll-index" start="{sum(1 for comm, _ in index_items if comm) + 1}">
{chr(10).join(item for comm, item in index_items if not comm)}
        </ol>
      </div>
    </section>

{chr(10).join(sections)}

    <section class="correspondence band--raised" aria-labelledby="hire-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="hire-title">Book Dorian Bailey</h2>
        <p>Events, portraits, seniors, families, sports, products, real estate or something else entirely: all types of photography offered, and bookings are available now. Pick a date and I&rsquo;ll reply to confirm, with rates.</p>
        <div class="btn-row"><button class="btn" type="button" data-book="photo">Book now</button><a class="btn" href="{html.escape(MAILTO_PHOTO)}">Inquire for rates</a></div>
        <p class="correspondence__more">Based in North East, Pennsylvania. Photographing across Erie County and travelling for events.</p>
      </div>
    </section>

    <nav class="wrap entry-nav" aria-label="Collection">
      <a class="entry-nav__prev" href="../metazoo/"><em>Previous</em> III. Bailey MetaZoo</a>
      <a class="entry-nav__next" href="../record/"><em>Next</em> V. The Record</a>
    </nav>

    <dialog class="lightbox" id="lightbox" aria-label="Photograph viewer">
      <figure>
        <img src="" alt="" decoding="async">
        <figcaption aria-live="polite"></figcaption>
      </figure>
      <button class="lightbox__btn lightbox__close" type="button" aria-label="Close">&times;</button>
      <button class="lightbox__btn lightbox__prev" type="button" aria-label="Previous photograph">&lsaquo;</button>
      <button class="lightbox__btn lightbox__next" type="button" aria-label="Next photograph">&rsaquo;</button>
    </dialog>""",
     extra_js=f'  <script src="../js/gallery.js?v={v("js/gallery.js")}" defer></script>\n',
     og_image="assets/img/og-photography.jpg", crumb="Dorian Bailey Photography", ld=[PERSON, PHOTO_SERVICE])

# ===================================================================== Record
page("record/index.html", "record", "The Record of Dorian Bailey | Resume",
     "The resume of Dorian Bailey: Marketing and MIS at Penn State Behrend, Vanta House, Better Selling With Bailey, Take The OddWay, Bailey MetaZoo and photography.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. V</p>
        <h1>The Record</h1>
        <p class="entry-head__standfirst">Dorian Bailey&rsquo;s education, positions, ventures and proficiencies, for anyone who would like it all on one page.</p>
        <div class="btn-row"><a class="btn" href="../assets/dorian-bailey-record.pdf" download="Dorian-Bailey-Resume.pdf">Download the résumé (PDF)</a></div>
      </div>
    </header>

    <section class="section">
      <div class="wrap">
        <div class="print-head" aria-hidden="true">
          {sig(40, "sig print-head__sig")}
          <div>
            <p class="print-head__name">Dorian Bailey</p>
            <p class="print-head__meta">North East, Pennsylvania &nbsp;&middot;&nbsp; <a href="mailto:{EMAIL}">{EMAIL}</a> &nbsp;&middot;&nbsp; <a href="{SITE}/">dorianbailey.com</a> &nbsp;&middot;&nbsp; <a href="{LINKS['linkedin']}">linkedin.com/in/dorian-bailey</a></p>
          </div>
        </div>
        <h2 class="sr-only">The record of Dorian Bailey</h2>
        <dl class="ledger">
          <div class="ledger__row">
            <dt>Education</dt>
            <dd>
              <h3>Penn State Behrend</h3>
              <p>Bachelor of Science, Marketing and Management Information Systems. <em>Expected 2027.</em></p>
              <p>Study across digital marketing, data analytics, information systems and the digital humanities.</p>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Positions</dt>
            <dd>
              <h3><a href="{LINKS['vanta']}" rel="noopener">Vanta House</a></h3>
              <p><em>Marketing assistant, June 2026 to present.</em> A video-first content studio in North East. Content strategy and social campaigns across client accounts, SEO and digital campaigns, campaign analysis, and support on shoots and video production.</p>
              <h3><a href="../photography/">MetaZoo TCG</a></h3>
              <p><em>Event photographer.</em> Commissioned coverage of the MetaZoo $10,000 cash tournament at the Legends Expo Card Show in Monroeville, the Mothman Festival and the Green Eyes Festival.</p>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Ventures</dt>
            <dd>
              <h3><a href="../better-selling/">Better Selling With Bailey</a></h3>
              <p><em>Founder and owner, May 2026 to present.</em> Estate sale management across Erie County. More than $35,000 in client sales, including events of more than $16,000 and $8,000 in a single weekend. Valuation, pricing, promotion, day-of sales and cleanup, all handled personally.</p>
              <h3><a href="../oddway/">Take The OddWay</a></h3>
              <p><em>Founder and builder.</em> A road-trip discovery platform for cryptids, folklore, haunted places and roadside oddities, designed and built end to end in Next.js, TypeScript and Supabase, with its own shop.</p>
              <h3><a href="../metazoo/">Bailey MetaZoo</a></h3>
              <p><em>Creator.</em> Short-form video on MetaZoo and cryptid folklore for YouTube and Instagram, including the VHS card-reveal series.</p>
              <h3><a href="../photography/">Photography</a></h3>
              <p><em>Photographer.</em> Event, portrait, landscape and close-up work, {TOTAL} photographs in {NUMWORD.lower()} collections.</p>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Recognition</dt>
            <dd>
              <p><a href="{LINKS['erie']}" rel="noopener">YourErie.com, May 2026.</a> A Better Selling With Bailey collector&rsquo;s sale in North East drew a crowd through heavy rain and wind.</p>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Proficiencies</dt>
            <dd>
              <p>Marketing strategy, SEO, social media and content, sales and pricing, data analysis, event management, customer relations.</p>
              <p>Photography and Adobe Lightroom and Photoshop; short-form video and video production.</p>
              <p>HTML and CSS, Next.js and React, TypeScript, Supabase, Git and GitHub, and AI tools.</p>
            </dd>
          </div>
          <div class="ledger__row ledger__row--screen">
            <dt>Correspondence</dt>
            <dd><p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{LINKS['linkedin']}" rel="noopener">linkedin.com/in/dorian-bailey</a></p></dd>
          </div>
        </dl>
      </div>
    </section>

    <nav class="wrap entry-nav" aria-label="Collection">
      <a class="entry-nav__prev" href="../photography/"><em>Previous</em> IV. Photography</a>
      <a class="entry-nav__next" href="../#index"><em>Back to</em> the index</a>
    </nav>""", crumb="The Record", og_image="assets/img/og-record.jpg",
     ld=[PERSON, {"@type": "ProfilePage", "url": SITE + "/record/", "name": "The Record of Dorian Bailey", "mainEntity": {"@id": PERSON_ID}}])

# ===================================================================== Privacy
PRIVACY_DATE = "October 31, 2026"
page("privacy/index.html", "privacy", "Privacy | Dorian Bailey",
     "What dorianbailey.com collects, which is almost nothing: no cookies, no tracking, no analytics.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">Privacy</p>
        <h1>What this site keeps</h1>
        <p class="entry-head__standfirst">Very little. No cookies, no tracking and no analytics. The only personal information the site asks for is in a booking request, and that goes straight to Dorian Bailey.</p>
      </div>
    </header>

    <section class="section">
      <div class="wrap">
        <h2 class="sr-only">What dorianbailey.com collects</h2>
        <dl class="ledger">
          <div class="ledger__row">
            <dt>Cookies</dt>
            <dd><p>This site doesn&rsquo;t set any. There are no analytics, advertising or social-media tracking scripts, and every font is served from this site rather than from Google Fonts or another font service.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>In your browser</dt>
            <dd><p>If you play Cryptid Highway, your best score is saved in your browser&rsquo;s local storage so it&rsquo;s there next time. It never leaves your device, and clearing this site&rsquo;s data in your browser removes it.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Hosting</dt>
            <dd><p>The site is hosted by GitHub Pages. Like any web host, GitHub logs visitors&rsquo; IP addresses for security purposes, under the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub General Privacy Statement</a>.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Outside services<em>Only when you use them</em></dt>
            <dd>
              <h3>YouTube</h3>
              <p>The television on the <a href="../metazoo/">Bailey MetaZoo</a> page uses YouTube&rsquo;s privacy-enhanced player, and nothing loads from YouTube until you insert a tape. Once a video plays, YouTube may set cookies and store data in your browser under <a href="https://policies.google.com/privacy" rel="noopener">Google&rsquo;s Privacy Policy</a>.</p>
              <h3>Take The OddWay</h3>
              <p>&ldquo;Roll a detour&rdquo; on the <a href="../oddway/">Take The OddWay</a> page, and the end of a Cryptid Highway drive, fetch a real stop from Take The OddWay&rsquo;s database. Nothing about you is sent with the request, though like any web request it reaches the server with your IP address.</p>
            </dd>
          </div>
          <div class="ledger__row">
            <dt>Booking requests</dt>
            <dd><p>When you book a date, your name, email, phone (if you give it), the date and your message are emailed to Dorian Bailey (estate sale requests to the Better Selling With Bailey inbox) through <a href="https://formsubmit.co" rel="noopener">FormSubmit</a>, a form-to-email service, and used only to reply to you. If that service can&rsquo;t be reached, your own email app opens with the request written out instead.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Correspondence</dt>
            <dd><p>If you email me, I&rsquo;ll use your address and what you write only to reply. I don&rsquo;t share or sell it, or add it to any list.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Other sites</dt>
            <dd><p>Links to Instagram, YouTube, LinkedIn, Facebook, GitHub and my other ventures lead to sites with their own privacy policies.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Changes</dt>
            <dd><p>If this site ever adds analytics or anything else that collects information, this page will say so first, with a new date.</p></dd>
          </div>
          <div class="ledger__row">
            <dt>Questions<em>Effective {PRIVACY_DATE}</em></dt>
            <dd><p>Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></dd>
          </div>
        </dl>
      </div>
    </section>

    <nav class="wrap entry-nav" aria-label="Collection">
      <a class="entry-nav__prev" href="../record/"><em>See also</em> The Record</a>
      <a class="entry-nav__next" href="../#index"><em>Back to</em> the index</a>
    </nav>""", crumb="Privacy")

# ===================================================================== 404
page("404.html", "", "Not found | Dorian Bailey", "This page is not in the collection.",
     """    <header class="entry-head entry-head--center">
      <div class="wrap">
        <p class="entry-head__num">Not catalogued</p>
        <h1>This page isn&rsquo;t in the collection</h1>
        <p class="entry-head__standfirst">It may have moved, or the address may be mistyped.</p>
        <div class="btn-row btn-row--center"><a class="btn" href="/">Return to the index</a></div>
      </div>
    </header>""", noindex=True)

# ===================================================================== Journal
# Written pieces about the work: an index at /journal/ and one page per article.
# Every fact in these pieces comes from the work itself, the clients' published reviews,
# the press coverage, or the parks' own published information.
J_DATE, J_DATE_LONG = "2026-10-31", "October 31, 2026"
J = "../../"                                     # article pages sit two folders deep


def jph(src, n=None):
    """A photograph record from a collection ('legends', 26) or from the estate sale set (index)."""
    return COLL[src]["photos"][n - 1] if n else ES["photos"][src]


def jfig(ph, caption, cls="", sizes="(max-width: 820px) 92vw, 600px"):
    w, h = thumb_dims(ph)
    return f"""          <figure class="plate article__fig{(' ' + cls) if cls else ''}">
            <div class="frame"><img src="{J}assets/photos/{ph['thumb']}" srcset="{srcset(ph, J, full=True)}" sizes="{sizes}" alt="{html.escape(ph['alt'])}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
            <figcaption>{caption}</figcaption>
          </figure>"""


def jpair(a, b):
    small = "(max-width: 820px) 45vw, 290px"
    return (f'          <div class="article__pair">\n{jfig(a[0], a[1], sizes=small)}\n{jfig(b[0], b[1], sizes=small)}\n          </div>')


def cta(title, text, buttons):
    return f"""          <aside class="article__cta" aria-labelledby="cta-title">
            <p class="service__status">Bookings available now</p>
            <h2 id="cta-title">{title}</h2>
            <p>{text}</p>
            <div class="btn-row">{''.join(buttons)}</div>
          </aside>"""


BOOK_PHOTO = '<button class="btn" type="button" data-book="photo">Book now</button>'
BOOK_SENIOR = '<button class="btn" type="button" data-book="photo" data-book-type="Seniors and graduates">Book now</button>'
BOOK_ESTATE = '<button class="btn" type="button" data-book="estate">Book now</button>'
RATES = f'<a class="btn" href="{html.escape(MAILTO_PHOTO)}">Inquire for rates</a>'
EMAIL_BSWB = f'<a class="btn" href="{html.escape(MAILTO_BSWB)}">Email me</a>'

JOURNAL = []

# ---------------------------------------------------------------- 1. Legends
JOURNAL.append(dict(
    slug="legends-expo-metazoo-tournament", section="Event photography",
    title="Photographing the MetaZoo $10,000 Tournament at the Legends Expo",
    seo="Photographing the MetaZoo $10,000 Tournament | Dorian Bailey",
    desc="Event photographer Dorian Bailey on covering the MetaZoo $10,000 cash tournament at the Legends Expo Card Show in Monroeville, Pennsylvania, for MetaZoo TCG.",
    standfirst="Two days of play at the Legends Expo Card Show in Monroeville, Pennsylvania, photographed for MetaZoo TCG.",
    dek="Two days of play in Monroeville, photographed for MetaZoo TCG: the prizes, the players, the broadcast and the last photograph of the weekend.",
    head=jph("legends", 26), card_pos="center 30%",
    about=["Event photography", "MetaZoo", "Trading card game tournaments"],
    body=f"""          <p class="article__lede">In August 2026, MetaZoo TCG commissioned me to photograph its $10,000 cash tournament at the Legends Expo Card Show in Monroeville, Pennsylvania. It was two days of play under convention-hall lights, and the job was to come away with everything the company would need afterward: the prizes, the booth, the players, the broadcast, and one photograph of everyone together at the end.</p>

          <h2>Before the first round</h2>
          <p>The quiet minutes before play starts are when the details get photographed. The first-, second- and third-place prize cards stood on their easels, the MetaZoo booth was set, and an inflatable winged cryptid towered over the hall on its MetaZoo base.</p>
          <p>Those pictures are easy to skip and hard to replace. They&rsquo;re what a brand reaches for when it announces the next event, and once the hall fills up they&rsquo;re much harder to take cleanly.</p>
{jpair((jph("legends", 2), "The first-place prize card"), (jph("legends", 5), "The MetaZoo Trading Card Game booth"))}

          <h2>At the tables</h2>
          <p>A card tournament is a quiet kind of sport. There&rsquo;s no ball to follow, so the story is in hands and faces: a player fanning a hand of cards, another weighing his next move, a reaction across the table when a play lands.</p>
          <p>I worked along the rows through the day, close enough to read the moment and far enough back to stay out of the way. Players are concentrating, and the photographs only work if they forget you&rsquo;re there.</p>
{jpair((jph("legends", 13), "Weighing the next move"), (jph("legends", 17), "A reaction across the table"))}

          <h2>The broadcast</h2>
          <p>Part of the coverage was the production itself: the commentary desk in front of the MetaZoo backdrop, and matches at the feature table played beneath the stream camera. For a brand, those pictures say the event reached people well beyond the hall.</p>
{jpair((jph("legends", 11), "The commentary desk"), (jph("legends", 22), "A match beneath the stream camera"))}

          <h2>The cards themselves</h2>
          <p>It&rsquo;s a trading card game, so the cards get photographs of their own: rows of Old Green Eyes, a Mothman Festival edition card in its sleeve, a Loveland Frogman, and cards being signed at the table.</p>
{jfig(jph("legends", 24), "A Mothman Festival edition card", cls="article__fig--narrow", sizes="(max-width: 820px) 70vw, 400px")}

          <h2>The last photograph</h2>
          <p>When play was done, the whole field gathered beneath the inflatable cryptid for one last photograph. It&rsquo;s the picture that sums up an event, so it&rsquo;s worth getting everyone in place for it before anyone heads for the door.</p>

          <h2>Covering your event</h2>
          <p>Legends was the first of three events I photographed for MetaZoo TCG in three months, followed by the <a href="{J}photography/#mothman">Mothman Festival</a> in Point Pleasant, West Virginia, and the <a href="{J}photography/#green-eyes">Green Eyes Festival</a> in Chickamauga, Georgia. <a href="{J}photography/#legends">The full Legends collection</a> is on the photography page.</p>
          <p>If you&rsquo;re running a tournament, convention, festival or other event, in Erie County or farther afield, I travel for event work.</p>
{cta("Book event photography", "Pick a date and I&rsquo;ll reply to confirm, with rates. Tournaments, conventions, festivals and parties.", [BOOK_PHOTO, RATES])}""",
    particulars=[("Event", "MetaZoo $10,000 cash tournament"), ("Where", "Legends Expo Card Show, Monroeville, Pennsylvania"),
                 ("When", "August 2026"), ("Commissioned by", "MetaZoo TCG"), ("Photographs", "Dorian Bailey"),
                 ("See also", f'<a href="{J}photography/#legends">The Legends collection</a>, <a href="{J}metazoo/">Bailey MetaZoo</a>')],
    images=[jph("legends", n) for n in (26, 2, 5, 13, 17, 11, 22, 24)],
))

# ---------------------------------------------------------------- 2. Senior pictures
JOURNAL.append(dict(
    slug="senior-pictures-erie-county", section="Senior pictures",
    title="Where to Take Senior Pictures in Erie County",
    seo="Where to Take Senior Pictures in Erie County, PA | Dorian Bailey",
    desc="Senior picture locations around Erie, PA, from Presque Isle sunsets and the Erie Land Lighthouse to Wintergreen Gorge, suggested by Dorian Bailey, a photographer in North East.",
    standfirst="Beaches, lighthouses, bluffs and woods around Erie and North East, Pennsylvania, and how to get the best light at each.",
    dek="Presque Isle at sunset, the lighthouses, the bluffs over the bay, the gorges and the vineyards: the places I&rsquo;d suggest, and when to go.",
    head=jph("north-east", 8), card_pos="center 50%",
    about=["Senior pictures", "Portrait photography", "Erie, Pennsylvania", "Presque Isle State Park"],
    body=f"""          <p class="article__lede">Erie County packs a lot into a short drive: a sand peninsula on Lake Erie, lighthouses, bluffs over the bay, wooded gorges and vineyards. These are the places I&rsquo;d suggest for senior pictures, from the classics to the quieter spots, with a note on light and timing.</p>

          <h2>Presque Isle State Park</h2>
          <p>Presque Isle is the obvious choice for a reason. The peninsula is Pennsylvania&rsquo;s only &ldquo;seashore&rdquo;: sand beaches and open water, joined to the mainland about four miles west of downtown Erie, with a road looping roughly thirteen miles around it. For senior pictures, a few spots stand out:</p>
          <ul>
            <li><strong>Sunset Point</strong>, between Beaches 9 and 10, is known for exactly what the name promises. Plan the session to end as the sun drops toward the lake.</li>
            <li><strong>Presque Isle Lighthouse</strong>, for a classic lighthouse portrait.</li>
            <li><strong>The North Pier Light</strong>, which marks the channel, for a pier and open water behind you.</li>
            <li><strong>The beaches themselves</strong>, for sand, water and nothing but sky.</li>
          </ul>
          <p>The park opens at 5 a.m. and its day-use areas close at dusk, so a sunset session needs to finish on time. It&rsquo;s a state park, so check with the park office (<a href="tel:+18148337424">814-833-7424</a>) about current guidelines for photo sessions before you settle on a date.</p>

          <h2>Lighthouses and the bayfront</h2>
          <ul>
            <li><strong>Erie Land Lighthouse</strong>, in east Erie, looks out over the city and Presque Isle.</li>
            <li><strong>The ERIE sign</strong> on the west bluffs of Bayview Park overlooks Presque Isle Bay: a senior photo that says exactly where it was taken.</li>
            <li><strong>Bicentennial Tower</strong> has two observation decks, the higher one 138 feet up, with views over the bay.</li>
            <li><strong>Tom Ridge Environmental Center</strong> has a 75-foot observation tower above the peninsula.</li>
            <li><strong>Downtown murals.</strong> Erie&rsquo;s murals can be seen on a self-guided tour, and a bright wall makes a bold background for a senior who wants something less traditional.</li>
          </ul>

          <h2>Woods, waterfalls and trails</h2>
          <p><strong>Wintergreen Gorge</strong>, east of Erie, has greenery, waterfalls and rock formations; wear real shoes for the walk in and carry the photo shoes in a bag. <strong>Asbury Woods</strong> has trails through the trees, which soften the light on a bright day.</p>

          <h2>Closer to North East</h2>
          <p>North East is grape country, and the rows of vines in late summer and early fall make a backdrop that says Lake Erie wine country. Vineyards are private property, so always ask the owner first. The town itself is worth a look in October, when the trees along its streets and park turn.</p>
{jfig(jph("north-east", 7), "Red maples in North East, Pennsylvania, October 2026")}

          <h2>When to go</h2>
          <ul>
            <li><strong>Golden hour.</strong> The hour or so before sunset gives warm, soft light that flatters everyone. On the lake, it&rsquo;s the best light of the day.</li>
            <li><strong>Overcast days</strong> are underrated: even light, no squinting, and colors that stay true.</li>
            <li><strong>October</strong> is when fall color in Erie County tends to peak, and it books up for that reason.</li>
            <li><strong>Two locations, not five.</strong> Driving between spots eats the light. Pick two that are close together and spend the time on photographs.</li>
            <li><strong>Bring a jacket for the lake.</strong> It&rsquo;s windier by the water, so plan hair and layers for it.</li>
          </ul>

          <h2>Booking senior pictures</h2>
          <p>I photograph seniors and graduates on location around Erie County. Tell me the places you have in mind, or let me suggest a pair that work well together, and I&rsquo;ll reply with rates.</p>
{cta("Book senior pictures", "Pick a date and I&rsquo;ll reply to confirm, with rates. Sessions on location around Erie and North East.", [BOOK_SENIOR, RATES])}""",
    particulars=[("Area", "Erie County, Pennsylvania"),
                 ("Places", "Presque Isle State Park, Erie Land Lighthouse, Bayview Park, Bicentennial Tower, Tom Ridge Environmental Center, Wintergreen Gorge, Asbury Woods and North East"),
                 ("Photographs", "North East in October, by Dorian Bailey"),
                 ("Service", f'<a href="{J}photography/#types">Seniors and graduates</a>')],
    images=[jph("north-east", 8), jph("north-east", 7)],
))

# ---------------------------------------------------------------- 3. How an estate sale works
_rows = "".join(f"<tr><td>${t:,}</td><td>&minus;${round(t * 0.2):,}</td><td>&minus;$995</td><td>${t - round(t * 0.2) - 995:,}</td></tr>" for t in (10000, 16000))
JOURNAL.append(dict(
    slug="how-estate-sales-work-erie-county", section="Estate sales",
    title="How an Estate Sale Works in Erie County",
    seo="How an Estate Sale Works in Erie County, PA | Dorian Bailey",
    desc="How Better Selling With Bailey runs an estate sale in Erie County, PA: walkthrough and pricing, staging, promotion, sale days, cleanup and what you keep, explained by Dorian Bailey.",
    standfirst="From the first walkthrough to the last box out the door: what happens, what it costs, and what you keep.",
    dek="Walkthrough, pricing, staging, promotion, sale days and cleanup, with the fees worked out: an estate sale with Better Selling With Bailey, start to finish.",
    head=jph(5), card_pos="center 40%",
    about=["Estate sales", "Erie County, Pennsylvania", "Better Selling With Bailey"],
    body=f"""          <p class="article__lede">An estate sale is a sale of a home&rsquo;s contents, held in the home itself. It isn&rsquo;t only for after a loss: people hold them when they move or downsize, and many of my clients treat a sale as a cleanout of a garage, basement or collection that happens to pay. Here is how a sale works with Better Selling With Bailey, start to finish.</p>

          <h2>Six steps</h2>
          <ol class="article__steps">
            <li><strong>Walkthrough and pricing.</strong> I walk through the home with you, assess everything to be sold and price it to sell. You can be involved in every pricing decision or none of them. Before the walkthrough, set aside anything you&rsquo;re keeping: family photographs, papers, and anything with sentimental value.</li>
            <li><strong>Staging.</strong> Rooms are organized and merchandise is laid out so buyers can browse easily and find what they came for. When a sale outgrows the house, tables go outside under a canopy.</li>
            <li><strong>Promotion.</strong> Listings, Facebook events and local outreach bring the right buyers to the door, whatever the weather.</li>
            <li><strong>Sale days.</strong> I run the floor: every customer, every sale and every question.</li>
            <li><strong>Cleanup.</strong> Teardown at the end of the sale, and free removal of whatever is left if you want it gone.</li>
            <li><strong>Proceeds.</strong> The earnings go to you, minus the flat fee and commission agreed before the sale began.</li>
          </ol>

          <h2>What it costs</h2>
          <p>The terms are simple: a $995 flat fee plus 20% of total sales, agreed before the sale begins. Removing whatever is left afterward is free. Here is the math on two sale totals:</p>
          <div class="article__table">
            <table>
              <thead><tr><th scope="col">Total sales</th><th scope="col">Commission, 20%</th><th scope="col">Flat fee</th><th scope="col">You keep</th></tr></thead>
              <tbody>{_rows}</tbody>
            </table>
          </div>
          <p>The best weekend so far brought in more than $16,000. To try your own number, use <a href="{J}better-selling/#calc-title">the calculator on the Better Selling With Bailey page</a>.</p>

          <h2>What sells</h2>
          <p>These are the categories that consistently draw buyers at Erie County sales:</p>
          <ul class="article__cols">
{chr(10).join(f"            <li>{x}</li>" for x in SELLS)}
          </ul>
          <p>Collections do especially well when they&rsquo;re promoted to the people who collect them, as at <a href="../star-wars-collectors-sale-north-east/">a Star Wars collector&rsquo;s sale in North East</a> in May 2026.</p>

          <h2>Do you need to be there?</h2>
          <p>No. Some clients like to be on hand for every minute; others would rather hand everything over and come back when it&rsquo;s done. Either works.</p>

          <h2>Where</h2>
          <p>Better Selling With Bailey is based in North East and runs sales in clients&rsquo; homes across Erie County, including Erie.</p>
{cta("Book an estate sale", "Pick a date and I&rsquo;ll reply to set up a walkthrough.", [BOOK_ESTATE, EMAIL_BSWB])}""",
    particulars=[("Company", f'<a href="{J}better-selling/">Better Selling With Bailey</a>'), ("Region", "Erie County, Pennsylvania"),
                 ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
                 ("Email", f'<a href="mailto:{BSWB_EMAIL}">{BSWB_EMAIL}</a>'), ("Photograph", "Ben and Andy Nagle")],
    images=[jph(5)],
))

# ---------------------------------------------------------------- 4. The Star Wars sale
JOURNAL.append(dict(
    slug="star-wars-collectors-sale-north-east", section="Estate sales",
    title="A Star Wars Collector’s Sale in North East",
    seo="Star Wars Collector’s Sale in North East, PA | Better Selling With Bailey",
    desc="A Better Selling With Bailey sale in North East, Pennsylvania: a Star Wars collection of action figures, books and sealed LEGO sets that drew a crowd through the rain and the local news.",
    standfirst="In May 2026, a collection of action figures, books and sealed LEGO sets drew a line of buyers through heavy rain and wind, and the local news came out to film it.",
    dek="Action figures, books and sealed LEGO sets, a line of buyers in the rain, and a story on the local news.",
    head=jph(2), card_pos="center 35%",
    about=["Estate sales", "Star Wars collectibles", "North East, Pennsylvania"],
    body=f"""          <p class="article__lede">Some sales sell themselves once the right people hear about them. This one was a Star Wars collection in North East: boxed action figures by the hundred, books and sealed LEGO sets, staged across a garage and down the side of the house.</p>

          <h2>The setup</h2>
          <p>The garage was staged wall to wall, with boxed figures on racks and LEGO sets stacked where buyers could see the boxes. More tables ran down the side of the house under a canopy, which mattered once the rain came in.</p>
{jfig(jph(0), "The garage, staged")}
{jpair((jph(1), "Tables down the side of the house"), (jph(4), "Racks of boxed figures"))}

          <h2>Rain, and a crowd anyway</h2>
          <p><a href="{LINKS['erie']}" rel="noopener">YourErie.com reported</a> an eager crowd through heavy rain and wind. Buyers lined up on the wet sale morning and browsed the tables under the canopy.</p>
{jpair((jph(5), "Under the canopy"), (jph(3), "The local news, filming the sale"))}

          <h2>On the news</h2>
          <p>The local TV news came out to film the sale, and YourErie.com ran the story in May 2026.</p>

          <h2>What the clients said</h2>
          <blockquote class="quote">
            <p>Everything was done for me. Great turnout for the sale. Was better than I hoped for. The local TV station even came out and did a story on the sale.</p>
            <cite>Andy N., Google review</cite>
          </blockquote>
          <blockquote class="quote">
            <p>Ran a giant garage sale for me and it went off without a hitch. Great advertising and phenomenal work setting things up and execution of the sale.</p>
            <cite>Ben N., Google review</cite>
          </blockquote>

          <h2>Why it worked</h2>
          <p>A collection sells when it&rsquo;s laid out so buyers can take it in at a glance, and promoted to the people who collect it. Staging, promotion and running the floor are the whole job; <a href="../how-estate-sales-work-erie-county/">here is how a sale works</a>, step by step.</p>
          <p class="article__credit">Photographs of the sale by clients Ben and Andy Nagle, from their Google reviews.</p>
{cta("Book an estate sale", "Have a collection, a garage or a whole house to sell? Pick a date and I&rsquo;ll reply to set up a walkthrough.", [BOOK_ESTATE, EMAIL_BSWB])}""",
    particulars=[("Where", "North East, Pennsylvania"), ("When", "May 2026"),
                 ("Collection", "Star Wars action figures, books and sealed LEGO sets"),
                 ("Press", f'<a href="{LINKS["erie"]}" rel="noopener">YourErie.com, May 2026</a>'),
                 ("Company", f'<a href="{J}better-selling/">Better Selling With Bailey</a>'),
                 ("Photographs", "Ben and Andy Nagle")],
    images=[jph(i) for i in (2, 0, 1, 4, 5, 3)],
))


def words(s):
    return len(_re.sub(r"<[^>]+>|&[a-z]+;", " ", s).split())


import re as _re
BLOG_ID = SITE + "/journal/#journal"
for i, a in enumerate(JOURNAL):
    url = f"{SITE}/journal/{a['slug']}/"
    a["url"] = url
    a["mins"] = max(1, round(words(a["body"]) / 230))
    hd = a["head"]
    prev_ = JOURNAL[i - 1] if i > 0 else None
    next_ = JOURNAL[i + 1] if i + 1 < len(JOURNAL) else None
    nav_prev = (f'<a class="entry-nav__prev" href="../{prev_["slug"]}/"><em>Previous</em> {html.escape(prev_["title"])}</a>' if prev_
                else '<a class="entry-nav__prev" href="../"><em>Back to</em> the Journal</a>')
    nav_next = (f'<a class="entry-nav__next" href="../{next_["slug"]}/"><em>Next</em> {html.escape(next_["title"])}</a>' if next_
                else '<a class="entry-nav__next" href="../"><em>Back to</em> the Journal</a>')
    parts = [("Published", f'<time datetime="{J_DATE}">{J_DATE_LONG}</time>'),
             ("Written by", f'<a href="{J}" rel="author">Dorian Bailey</a>, North East, Pennsylvania')] + a["particulars"]
    dl = "\n".join(f"            <div><dt>{k}</dt><dd>{v_}</dd></div>" for k, v_ in parts)
    post = {"@type": "BlogPosting", "@id": url + "#article", "headline": a["title"], "description": a["desc"],
            "url": url, "mainEntityOfPage": url, "datePublished": J_DATE, "dateModified": J_DATE, "inLanguage": "en-US",
            "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID}, "isPartOf": {"@id": BLOG_ID},
            "image": [f"{SITE}/assets/photos/{ph['file']}" for ph in a["images"][:3]],
            "articleSection": a["section"], "keywords": a["about"], "wordCount": words(a["body"])}
    page(f"journal/{a['slug']}/index.html", "journal-post", a["seo"], html.escape(a["desc"]),
         og_image=f"assets/img/og-journal-{a['slug']}.jpg", og_type="article",
         head_extra=(f'\n  <link rel="preload" href="{J}assets/fonts/libre-caslon-text-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>'
                     f'\n  <meta property="article:published_time" content="{J_DATE}">'
                     f'\n  <meta property="article:author" content="{SITE}/">'
                     f'\n  <meta property="article:section" content="{a["section"]}">'),
         ld=[PERSON, post], crumb=[("Journal", SITE + "/journal/"), (a["title"], url)], body=f"""    <article>
    <header class="entry-head entry-head--figure entry-head--article">
      <div class="wrap">
        <div class="entry-head__text">
          <p class="entry-head__num"><a href="../">Journal</a> <span aria-hidden="true">&middot;</span> {a['section']}</p>
          <h1>{html.escape(a['title'])}</h1>
          <p class="entry-head__standfirst">{a['standfirst']}</p>
          <p class="article__byline">By <a href="{J}" rel="author">Dorian Bailey</a> <span aria-hidden="true">&middot;</span> <time datetime="{J_DATE}">{J_DATE_LONG}</time> <span aria-hidden="true">&middot;</span> <span class="nowrap">{a['mins']} minute read</span></p>
        </div>
        <figure class="entry-head__print">
          <div class="frame"><img src="{J}assets/photos/{hd['file']}" srcset="{srcset(hd, J, full=True)}" sizes="(max-width: 900px) 320px, 420px" alt="{html.escape(hd['alt'])}" width="{hd['w']}" height="{hd['h']}" style="object-position:{a['card_pos']}" fetchpriority="high" decoding="async"></div>
        </figure>
      </div>
    </header>

    <section class="section">
      <div class="wrap entry">
        <div class="entry__prose article">
{a['body']}
        </div>
        <aside class="particulars" aria-labelledby="particulars-title">
          <h2 id="particulars-title">Particulars</h2>
          <dl>
{dl}
          </dl>
        </aside>
      </div>
    </section>
    </article>

    <nav class="wrap entry-nav" aria-label="Journal">
      {nav_prev}
      {nav_next}
    </nav>""")

# ---------------------------------------------------------------- Journal index
def j_item(a):
    ph = a["head"]
    return f"""          <li>
            <a href="{a['slug']}/">
              <div class="frame"><img src="../assets/photos/{ph['thumb']}" srcset="{srcset(ph, '../')}" sizes="(max-width: 640px) 120px, 220px" alt="" width="{thumb_dims(ph)[0]}" height="{thumb_dims(ph)[1]}" style="object-position:{a['card_pos']}" loading="lazy" decoding="async"></div>
              <div class="journal-list__text">
                <p class="journal-list__kicker">{a['section']} <span aria-hidden="true">&middot;</span> <time datetime="{J_DATE}">{J_DATE_LONG}</time></p>
                <h2 class="journal-list__title">{html.escape(a['title'])}</h2>
                <p class="journal-list__dek">{a['dek']}</p>
              </div>
            </a>
          </li>"""


BLOG = {"@type": "Blog", "@id": BLOG_ID, "url": SITE + "/journal/", "name": "The Journal of Dorian Bailey", "inLanguage": "en-US",
        "description": "Notes from Dorian Bailey's work in photography and estate sales around Erie County, Pennsylvania.",
        "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
        "blogPost": [{"@type": "BlogPosting", "@id": a["url"] + "#article", "headline": a["title"], "url": a["url"], "datePublished": J_DATE}
                     for a in JOURNAL]}
page("journal/index.html", "journal", "Journal | Dorian Bailey, Photographer and Estate Sales in Erie, PA",
     "The journal of Dorian Bailey: notes on event photography, senior pictures and estate sales around Erie County and North East, Pennsylvania.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">Journal</p>
        <h1>The Journal</h1>
        <p class="entry-head__standfirst">Notes from the work of Dorian Bailey: events photographed, estate sales run, and places around Erie County worth knowing.</p>
      </div>
    </header>

    <section class="section">
      <div class="wrap">
        <ol class="journal-list">
{chr(10).join(j_item(a) for a in JOURNAL)}
        </ol>
      </div>
    </section>

    <nav class="wrap entry-nav" aria-label="Collection">
      <a class="entry-nav__prev" href="../#index"><em>Back to</em> the index</a>
      <a class="entry-nav__next" href="../photography/"><em>See also</em> Dorian Bailey Photography</a>
    </nav>""", ld=[PERSON, BLOG], crumb="Journal")


# ===================================================================== Sitemap
# Every public page with today's date, and the photographs on each page, so search engines
# can find them for image search. (The 404 page is left out on purpose.)
import datetime
import re as _re
TODAY = datetime.date.today().isoformat()
# Keep each page's previous date unless its HTML actually changed in this build
_old = (ROOT / "sitemap.xml").read_text() if (ROOT / "sitemap.xml").exists() else ""
PREV = dict(_re.findall(r"<loc>" + _re.escape(SITE) + r"/([^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", _old))
PAGE_IMAGES = {
    "": ["assets/img/dorian-bailey.jpg", "assets/photos/" + FEAT["file"]],
    "better-selling/": ["assets/img/dorian-bailey.jpg"] + ["assets/photos/" + ph["file"] for ph in ES["photos"]],
    "oddway/": ["assets/photos/" + COLL["green-eyes"]["photos"][6]["file"]],
    "metazoo/": ["assets/photos/" + COLL["legends"]["photos"][1]["file"]],
    "photography/": ["assets/photos/" + ph["file"] for c in M["collections"] for ph in c["photos"]],
    "record/": ["assets/img/dorian-bailey.jpg"],
    "privacy/": [],
    "journal/": ["assets/photos/" + a["head"]["file"] for a in JOURNAL],
}
for a in JOURNAL:
    PAGE_IMAGES[f"journal/{a['slug']}/"] = ["assets/photos/" + ph["file"] for ph in a["images"]]
urls = []
for path, imgs in PAGE_IMAGES.items():
    im = "".join(f"\n    <image:image><image:loc>{SITE}/{i}</image:loc></image:image>" for i in imgs)
    page_file = (path or "") + "index.html"
    lastmod = TODAY if CHANGED.get(page_file, True) or path not in PREV else PREV[path]
    urls.append(f"  <url>\n    <loc>{SITE}/{path}</loc>\n    <lastmod>{lastmod}</lastmod>{im}\n  </url>")
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                  'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")
print("wrote sitemap.xml")
