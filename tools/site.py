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
    ("better-selling/", "Better Selling", "selling"),
    ("oddway/", "OddWay", "oddway"),
    ("metazoo/", "MetaZoo", "metazoo"),
    ("photography/", "Photography", "photo"),
    ("record/", "Record", "record"),
    ("index.html#correspondence", "Contact", "contact"),
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
}


def seal(size, cls="seal", foil=None):
    """The DB monogram seal. foil='<id>' paints it with a gold-foil gradient."""
    paint = f"url(#{foil})" if foil else "currentColor"
    defs = f"""
          <defs><linearGradient id="{foil}" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#8a6b32"/><stop offset=".28" stop-color="#e2cb8c"/>
            <stop offset=".5" stop-color="#a8894b"/><stop offset=".72" stop-color="#ead7a2"/>
            <stop offset="1" stop-color="#7d612c"/>
          </linearGradient></defs>""" if foil else ""
    return f"""<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 120 120" aria-hidden="true" focusable="false">{defs}
          <circle class="seal__ring" pathLength="1" cx="60" cy="60" r="57" fill="none" stroke="{paint}" stroke-width="1.6"/>
          <circle class="seal__ring seal__ring--inner" pathLength="1" cx="60" cy="60" r="50" fill="none" stroke="{paint}" stroke-width=".8"/>
          <g class="seal__dots" fill="{paint}"><circle cx="60" cy="6.5" r="1.8"/><circle cx="60" cy="113.5" r="1.8"/>
          <circle cx="6.5" cy="60" r="1.8"/><circle cx="113.5" cy="60" r="1.8"/></g>
          <text class="seal__mono" x="60" y="73" text-anchor="middle" font-family="'Libre Caslon Display', Georgia, serif" font-size="42" fill="{paint}">DB</text>
        </svg>"""


def thumb_dims(p):
    w, h = p["w"], p["h"]
    s = 900 / max(w, h)
    return round(w * s), round(h * s)


def page(path, key, title, desc, body, extra_js="", og_image="assets/img/og-card.jpg"):
    depth = path.count("/")
    p = "/" if path == "404.html" else "../" * depth
    canonical = SITE + "/" + path.replace("index.html", "")
    nav = "\n".join(
        f'          <li><a href="{p}{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
        for href, label, k in NAV)
    out = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="color-scheme" content="light dark">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#1c1b19">
  <link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{p}assets/fonts/libre-caslon-display-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{p}assets/fonts/libre-caslon-text-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{p}css/base.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap site-header__inner">
      <a class="site-mark" href="{p}index.html">
        {seal(34)}
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
    <div class="wrap site-footer__inner">
      <div class="site-footer__mark">
        {seal(56, "seal seal--deboss")}
        <p>The Collection of Dorian Bailey<br><em>North East, Pennsylvania</em></p>
      </div>
      <ul class="site-footer__links">
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{LINKS['linkedin']}" rel="noopener">LinkedIn</a></li>
        <li><a href="{LINKS['ig']}" rel="noopener">Instagram</a></li>
        <li><a href="{LINKS['yt']}" rel="noopener">YouTube</a></li>
        <li><a href="{LINKS['github']}" rel="noopener">GitHub</a></li>
      </ul>
      <p class="site-footer__fine">&copy; <span data-year>2026</span> Dorian Bailey. Photographs are the author&rsquo;s own.</p>
    </div>
  </footer>

  <script src="{p}js/main.js" defer></script>
{extra_js}</body>
</html>
"""
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(out)
    print("wrote", path)


def plate(src_thumb, alt, w, h, caption, href=None, prefix=""):
    img = f'<img src="{prefix}{src_thumb}" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
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
                          f"<em>{cap}</em>", href=f"photography/#{cid}"))
selected = "\n          ".join(selected)

FEAT = COLL["legends"]["photos"][25]

EVENTS = [("legends", "Legends", "Two-day tournament, August 2026"),
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

page("index.html", "home",
     "Dorian Bailey",
     "The collection of Dorian Bailey: Better Selling With Bailey, Take The OddWay, Bailey MetaZoo and photography for MetaZoo TCG, from North East, Pennsylvania.",
     f"""    <section class="frontispiece">
      <div class="collage" aria-hidden="true">
        <div class="collage__wall">
{collage()}
        </div>
      </div>
      <div class="wrap frontispiece__inner">
        {seal(112, "seal seal--large seal--deboss")}
        <p class="frontispiece__pre">The Collection of</p>
        <h1>Dorian Bailey</h1>
        <p class="frontispiece__sub">Ventures, pursuits and photographs<br>from North East, Pennsylvania</p>
      </div>
    </section>

    <section class="section" aria-labelledby="contents-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="contents-title">Contents</h2>
        <ol class="contents">
{contents}
        </ol>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="feature-title">
      <div class="wrap feature">
        <figure class="feature__media">
          <a class="frame" href="photography/#legends"><img src="assets/photos/{FEAT['file']}" alt="{html.escape(FEAT['alt'])}" width="{FEAT['w']}" height="{FEAT['h']}" loading="lazy" decoding="async"></a>
        </figure>
        <div class="feature__card">
          <p class="feature__kicker">Featured commission</p>
          <h2 id="feature-title">MetaZoo TCG, 2026</h2>
          <p>Three events in three months for MetaZoo TCG: a two-day tournament, the Mothman Festival and the Green Eyes Festival. Players at the tables, prize cards on their easels, costumed cryptids, and the crowds that came to see them.</p>
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
          <div class="frame"><img src="assets/img/dorian-bailey.jpg" alt="Portrait of Dorian Bailey" width="900" height="1200" loading="lazy"></div>
        </figure>
        <div class="foreword__text">
          <h2 class="section-title" id="foreword-title">Foreword</h2>
          <p class="lede">Born and raised in North East, Pennsylvania, I study Marketing and Management Information Systems at Penn State Behrend.</p>
          <p>Long before I started a business, I spent years buying, selling, researching and pricing things of every kind. That became Better Selling With Bailey. A taste for the strange side of the map became Take The OddWay, and a love of cryptid lore and collecting became Bailey MetaZoo. Somewhere along the way I picked up a camera, and now photograph events for MetaZoo TCG.</p>
          <p>By day I&rsquo;m a marketing assistant at <a href="{LINKS['vanta']}" rel="noopener">Vanta House</a>, a video-first content studio here in North East. This site gathers the rest: the work I&rsquo;m paid for and the work I&rsquo;d do anyway.</p>
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

    <section class="correspondence band--raised" id="correspondence" aria-labelledby="corr-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="corr-title">Correspondence</h2>
        <p>For work, commissions, collaborations or an estate sale, write to me directly.</p>
        <p class="correspondence__email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p class="correspondence__more">Also on <a href="{LINKS['linkedin']}" rel="noopener">LinkedIn</a>. Estate sale bookings are handled at <a href="{LINKS['bswb']}" rel="noopener">bettersellingwithbailey.com</a>.</p>
      </div>
    </section>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Dorian Bailey",
      "url": "https://dorianbailey.com",
      "email": "mailto:{EMAIL}",
      "image": "https://dorianbailey.com/assets/img/dorian-bailey.jpg",
      "homeLocation": "North East, Pennsylvania",
      "alumniOf": "Penn State Behrend",
      "jobTitle": "Marketing Assistant",
      "worksFor": {{"@type": "Organization", "name": "Vanta House", "url": "{LINKS['vanta']}"}},
      "sameAs": ["{LINKS['linkedin']}", "{LINKS['github']}", "{LINKS['bswb']}", "{LINKS['oddway']}", "{LINKS['yt']}", "{LINKS['ig']}"]
    }}
    </script>""")


# ===================================================================== Entries (venture pages)
ORDER = [("better-selling", "I", "Better Selling With Bailey"),
         ("oddway", "II", "Take The OddWay"),
         ("metazoo", "III", "Bailey MetaZoo"),
         ("photography", "IV", "Photography")]


def entry(slug, key, title, desc, standfirst, prose, particulars, plates, links, head_print=None, extra=""):
    idx = [o[0] for o in ORDER].index(slug)
    num = ORDER[idx][1]
    prev_ = ORDER[idx - 1] if idx > 0 else None
    next_ = ORDER[idx + 1]
    parts = "\n".join(f"            <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in particulars)
    lk = "\n".join(f'          <a class="btn" href="{h}" rel="noopener">{t}</a>' for t, h in links)
    nav = []
    if prev_:
        nav.append(f'<a class="entry-nav__prev" href="../{prev_[0]}/"><em>Previous</em> {prev_[1]}. {prev_[2]}</a>')
    else:
        nav.append('<a class="entry-nav__prev" href="../index.html"><em>Back to</em> Contents</a>')
    nav.append(f'<a class="entry-nav__next" href="../{next_[0]}/"><em>Next</em> {next_[1]}. {next_[2]}</a>')

    if head_print:
        src, alt, w, h = head_print
        head = f"""    <header class="entry-head entry-head--figure">
      <div class="wrap">
        <div class="entry-head__text">
          <p class="entry-head__num">No. {num}</p>
          <h1>{title}</h1>
          <p class="entry-head__standfirst">{standfirst}</p>
        </div>
        <figure class="entry-head__print">
          <div class="frame"><img src="{src}" alt="{html.escape(alt)}" width="{w}" height="{h}" fetchpriority="high" decoding="async"></div>
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

    page(f"{slug}/index.html", key, f"{title} | Dorian Bailey", desc, f"""{head}

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
                 href=f"../photography/#{cid}" if link else None, prefix="../")


def HP(cid, n):
    ph = COLL[cid]["photos"][n - 1]
    return ("../assets/photos/" + ph["file"], ph["alt"], ph["w"], ph["h"])


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

bswb_extra = f"""
    <section class="section section--rule" aria-labelledby="process-title">
      <div class="wrap">
        <h2 class="section-title" id="process-title">How a sale works</h2>
        <p class="section-intro">Every sale is hosted at the client&rsquo;s home in Erie County and handled start to finish.</p>
        <ol class="steps">
{steps(BSWB_STEPS)}
        </ol>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="clients-title">
      <div class="wrap split">
        <div>
          <h2 class="section-title" id="clients-title">From clients</h2>
          <div class="quotes quotes--stack">
            <blockquote class="quote">
              <p>Everything was done for me. Great turnout for the sale. Was better than I hoped for.</p>
              <cite>Google review</cite>
            </blockquote>
            <blockquote class="quote">
              <p>Great advertising and phenomenal work setting things up and execution of the sale.</p>
              <cite>Google review</cite>
            </blockquote>
          </div>
        </div>
        <div>
          <h2 class="section-title">What sells</h2>
          <p class="section-intro">The categories that consistently draw buyers at Erie County sales.</p>
          <ul class="events cols-2">
{chr(10).join(f"            <li>{s}</li>" for s in SELLS)}
          </ul>
          <h3 class="subhead">In the press</h3>
          <p><a href="{LINKS['erie']}" rel="noopener">YourErie.com, May 2026.</a> A Star Wars collector&rsquo;s sale in North East drew an eager crowd through heavy rain and wind, for a collection of action figures, books and sealed LEGO sets.</p>
        </div>
      </div>
    </section>
"""

entry("better-selling", "selling", "Better Selling With Bailey",
      "Better Selling With Bailey is Dorian Bailey's estate sale company in Erie County, Pennsylvania.",
      "Estate sales in Erie County, run start to finish by one person, so the people selling keep the proceeds.",
      """          <p>Better Selling With Bailey prices, stages, promotes and runs estate sales in the client&rsquo;s own home, then clears whatever is left at no charge. Many clients treat it as a cleanout of a garage, basement or collection that happens to pay.</p>
          <p>Every client works with me directly, from the first walkthrough to the last sale of the day. Some like to be involved in every pricing decision; others would rather hand the whole thing over. Either works.</p>""",
      [("Established", "May 2026, North East, Pennsylvania"),
       ("Region", "Erie County"),
       ("Role", "Founder and owner"),
       ("Client sales", "More than $35,000"),
       ("Top events", "More than $16,000 and $8,000, each in a single weekend"),
       ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
       ("Press", f'<a href="{LINKS["erie"]}" rel="noopener">YourErie.com, May 2026</a>')],
      [],
      [("Visit bettersellingwithbailey.com", LINKS["bswb"]), ("Facebook", LINKS["bswb_fb"])],
      head_print=("../assets/img/dorian-bailey.jpg", "Dorian Bailey in a Better Selling With Bailey polo", 900, 1200),
      extra=bswb_extra)

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
       ("Also", f'<a href="{LINKS["shop"]}" rel="noopener">The OddWay shop</a>')],
      [P("green-eyes", 5, "<em>Bigfoot, from Green Eyes</em>"),
       P("letchworth", 7, "<em>The gorge, from Letchworth</em>"),
       P("north-east", 2, "<em>Halloween, from North East</em>")],
      [("Visit taketheoddway.com", LINKS["oddway"]), ("Shop the OddWay", LINKS["shop"])],
      head_print=HP("green-eyes", 7),
      extra=odd_extra)

# ---------------------------------------------------------------- III. Bailey MetaZoo
FILMS = ["The Squonk Might Be the Saddest Cryptid Ever", "Old Scratch Is Back in MetaZoo",
         "Ohio Has a Frogman Problem: the Loveland Frogman", "What Cryptid Haunts Your State?",
         "Escape Polybius: a ten-pack giveaway", "Salem Nights, a new limited release"]
VHS = [
    ("The tape", "Hands slide a cassette into a VCR, shot moody and close, with the deck&rsquo;s clunk on the beat."),
    ("Warm-up", "An old CRT clicks on and warms to snow as the camera pushes toward the glass."),
    ("The logo", "A white flash, then the MetaZoo logo rolls down into place through fading static."),
    ("The flashes", "Five cards flash through the snow, each a little faster than the last."),
    ("The hero", "Tracking drops, a beat of dead air, then the hero card slams in with its own sound."),
    ("Switch-off", "The picture squeezes to a line, then a dot, and loops back to the start."),
]
mz_extra = f"""
    <section class="section section--rule" aria-labelledby="vhs-title">
      <div class="wrap">
        <h2 class="section-title" id="vhs-title">The VHS reveal</h2>
        <p class="section-intro">The signature format: an eighteen-second vertical film built to loop, shot on real tape-deck and television footage.</p>
        <ol class="steps">
{steps(VHS)}
        </ol>
      </div>
    </section>

    <section class="section band--raised section--rule" aria-labelledby="films-title">
      <div class="wrap split">
        <div>
          <h2 class="section-title" id="films-title">Recent films</h2>
          <ul class="events">
{chr(10).join(f'            <li><a href="{LINKS["yt"]}" rel="noopener">{f}</a></li>' for f in FILMS)}
          </ul>
        </div>
        <div>
          <h2 class="section-title">On assignment</h2>
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
      extra=mz_extra)

# ===================================================================== Photographs
index_items, sections = [], []
running = 0
for c in M["collections"]:
    cov = next(p for p in c["photos"] if p["thumb"] == c["cover"])
    w, h = thumb_dims(cov)
    n = len(c["photos"])
    index_items.append((bool(c.get("commission")), f"""          <li>
            <a href="#{c['id']}">
              <span class="frame"><img src="../assets/photos/{c['cover']}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
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
              <img src="../assets/photos/{ph['thumb']}" alt="{html.escape(ph['alt'])}" width="{tw}" height="{th}" loading="lazy" decoding="async">
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
          </div>
        </header>
        <div class="gallery" data-collection>
{chr(10).join(figs)}
        </div>
      </div>
    </section>""")

BANNER = COLL["letchworth"]["photos"][1]

page("photography/index.html", "photo", "Photography | Dorian Bailey",
     f"Photography by Dorian Bailey: event coverage for MetaZoo TCG, work with Vanta House, and {NUMWORD.lower()} collections of portrait, event, landscape and close-up photographs.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. IV</p>
        <h1>Photography</h1>
        <p class="entry-head__standfirst">Event, portrait and landscape photography, from commissioned coverage for MetaZoo TCG to quiet studies close to home. Made on a Canon EOS R50.</p>
      </div>
    </header>

    <figure class="banner">
      <div class="banner__clip"><img src="../assets/photos/{BANNER['file']}" alt="{html.escape(BANNER['alt'])}" width="{BANNER['w']}" height="{BANNER['h']}" fetchpriority="high" decoding="async"></div>
      <figcaption class="wrap"><em>Letchworth State Park, New York, October 2026</em></figcaption>
    </figure>

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
                <li><a href="#legends">Legends</a> <em>MetaZoo TCG tournament, August 2026</em></li>
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

    <section class="section" aria-labelledby="kit-title">
      <div class="wrap split">
        <div class="measure">
          <h2 class="section-title" id="kit-title">Approach</h2>
          <p class="lede">Most of this is event work: long days on a festival street or a tournament floor, close to the people and the cards.</p>
          <p>The kit is small on purpose. Two fast primes for faces and details, a zoom for when the crowd closes in, and everything edited in Lightroom. The personal collections are where the slower pictures live: a gorge in October, a cat in window light, fungi on a fallen log.</p>
        </div>
        <aside class="particulars" aria-labelledby="kit-list-title">
          <h2 id="kit-list-title">The kit</h2>
          <dl>
            <div><dt>Body</dt><dd>Canon EOS R50</dd></div>
            <div><dt>Primes</dt><dd>RF 35mm f/1.8 Macro IS STM<br>RF 50mm f/1.8 STM</dd></div>
            <div><dt>Zooms</dt><dd>EF 24&ndash;105mm f/4L IS USM<br>RF-S 55&ndash;210mm<br>RF-S 18&ndash;45mm</dd></div>
            <div><dt>Editing</dt><dd>Adobe Lightroom and Photoshop</dd></div>
          </dl>
        </aside>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="collections-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="collections-title">Collections</h2>
          <p class="section-head__note">{TOTAL} plates in {NUMWORD.lower()} collections</p>
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
     extra_js='  <script src="../js/gallery.js" defer></script>\n')

# ===================================================================== Record
page("record/index.html", "record", "The Record | Dorian Bailey",
     "The record of Dorian Bailey: Penn State Behrend, Better Selling With Bailey, Take The OddWay, Bailey MetaZoo and photography.",
     f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. V</p>
        <h1>The Record</h1>
        <p class="entry-head__standfirst">Education, positions, ventures and proficiencies, for anyone who would like it all on one page.</p>
        <div class="btn-row"><a class="btn" href="../assets/dorian-bailey-record.pdf" download>Download the record (PDF)</a></div>
      </div>
    </header>

    <section class="section">
      <div class="wrap">
        <div class="print-head" aria-hidden="true">
          {seal(64, "seal print-head__seal")}
          <div>
            <p class="print-head__name">Dorian Bailey</p>
            <p class="print-head__meta">North East, Pennsylvania &nbsp;&middot;&nbsp; {EMAIL} &nbsp;&middot;&nbsp; dorianbailey.com &nbsp;&middot;&nbsp; linkedin.com/in/dorian-bailey</p>
          </div>
        </div>
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
              <p><em>Event photographer.</em> Commissioned coverage at the Legends tournament, the Mothman Festival and the Green Eyes Festival.</p>
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
              <p><em>Photographer.</em> Event, portrait, landscape and close-up work, collected in {NUMWORD.lower()} series of {TOTAL} plates.</p>
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
      <a class="entry-nav__next" href="../index.html"><em>Back to</em> Contents</a>
    </nav>""")

# ===================================================================== 404
page("404.html", "", "Not found | Dorian Bailey", "This page is not in the collection.",
     """    <header class="entry-head entry-head--center">
      <div class="wrap">
        <p class="entry-head__num">Not catalogued</p>
        <h1>This page isn&rsquo;t in the collection</h1>
        <p class="entry-head__standfirst">It may have moved, or the address may be mistyped.</p>
        <div class="btn-row btn-row--center"><a class="btn" href="/">Return to the contents</a></div>
      </div>
    </header>""")
