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
  <meta name="theme-color" content="#1e3a2b">
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
        {seal(56, foil="foil-foot")}
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


# ===================================================================== Home
ENTRIES = [
    ("I", "better-selling/", "Better Selling With Bailey", "Estate sales in Erie County"),
    ("II", "oddway/", "Take The OddWay", "A road-trip guide to the strange"),
    ("III", "metazoo/", "Bailey MetaZoo", "Cryptids and trading cards"),
    ("IV", "photography/", "Photography", "Commissions and collections"),
    ("V", "record/", "The Record", "Education, ventures and proficiencies"),
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

page("index.html", "home",
     "Dorian Bailey",
     "The collection of Dorian Bailey: Better Selling With Bailey, Take The OddWay, Bailey MetaZoo and photographs, from North East, Pennsylvania.",
     f"""    <section class="frontispiece">
      <div class="wrap frontispiece__inner">
        {seal(112, "seal seal--large", foil="foil-hero")}
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

    <section class="section section--rule" aria-labelledby="foreword-title">
      <div class="wrap foreword">
        <figure class="plate foreword__portrait">
          <div class="frame"><img src="assets/img/dorian-bailey.jpg" alt="Portrait of Dorian Bailey" width="900" height="1200"></div>
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

    <section class="section section--rule" aria-labelledby="plates-title">
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

    <section class="correspondence" id="correspondence" aria-labelledby="corr-title">
      <div class="wrap wrap--narrow">
        <h2 class="section-title" id="corr-title">Correspondence</h2>
        <p>For work, collaborations or an estate sale, write to me directly.</p>
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


# ===================================================================== Entries (brand pages)
ORDER = [("better-selling", "I", "Better Selling With Bailey"),
         ("oddway", "II", "Take The OddWay"),
         ("metazoo", "III", "Bailey MetaZoo"),
         ("photography", "IV", "Photography")]


def entry(slug, key, title, desc, standfirst, prose, particulars, plates, links):
    idx = [o[0] for o in ORDER].index(slug)
    num = ORDER[idx][1]
    prev_ = ORDER[idx - 1] if idx > 0 else None
    next_ = ORDER[idx + 1]
    parts = "\n".join(f"            <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in particulars)
    lk = "\n".join(f'          <a class="btn" href="{h}" rel="noopener">{t}</a>' for t, h in links)
    pl = "\n          ".join(plates)
    nav = []
    if prev_:
        nav.append(f'<a class="entry-nav__prev" href="../{prev_[0]}/"><em>Previous</em> {prev_[1]}. {prev_[2]}</a>')
    else:
        nav.append('<a class="entry-nav__prev" href="../index.html"><em>Back to</em> Contents</a>')
    nav.append(f'<a class="entry-nav__next" href="../{next_[0]}/"><em>Next</em> {next_[1]}. {next_[2]}</a>')
    page(f"{slug}/index.html", key, f"{title} | Dorian Bailey", desc, f"""    <header class="entry-head">
      <div class="wrap">
        <p class="entry-head__num">No. {num}</p>
        <h1>{title}</h1>
        <p class="entry-head__standfirst">{standfirst}</p>
      </div>
    </header>

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

    <section class="section section--rule" aria-label="Plates">
      <div class="wrap">
        <div class="plate-row plate-row--{len(plates)}">
          {pl}
        </div>
      </div>
    </section>

    <nav class="wrap entry-nav" aria-label="Collection">
      {nav[0]}
      {nav[1]}
    </nav>""")


def P(cid, n, cap, link=True):
    ph, w, h = photo(cid, n)
    return plate("assets/photos/" + ph["thumb"], ph["alt"], w, h, cap,
                 href=f"../photography/#{cid}" if link else None, prefix="../")


entry("better-selling", "selling", "Better Selling With Bailey",
      "Better Selling With Bailey is Dorian Bailey's estate sale company in Erie County, Pennsylvania.",
      "Estate sales in Erie County, run start to finish by one person, so the people selling keep the proceeds.",
      """          <p>Better Selling With Bailey prices, stages, promotes and runs estate sales in the client&rsquo;s own home, then clears whatever is left at no charge. Many clients treat it as a cleanout of a garage, basement or collection that happens to pay.</p>
          <p>Every client works with me directly, from the first walkthrough to the last sale of the day. I set the prices, arrange the rooms, write the listings, run the floor and handle the teardown.</p>
          <p>A Star Wars collector&rsquo;s sale in North East drew a crowd through heavy rain and wind in May 2026, and was covered by YourErie.com.</p>""",
      [("Established", "May 2026, North East, Pennsylvania"),
       ("Region", "Erie County"),
       ("Role", "Founder and owner"),
       ("Returned to sellers", "More than $35,000"),
       ("Top events", "More than $16,000 and $8,000, each in a single weekend"),
       ("Terms", "$995 flat fee plus 20% commission; leftover removal free"),
       ("Press", f'<a href="{LINKS["erie"]}" rel="noopener">YourErie.com, May 2026</a>')],
      [plate("../assets/img/dorian-bailey.jpg", "Dorian Bailey in a Better Selling With Bailey polo", 900, 1200,
             "<em>The proprietor, in the house colors</em>")],
      [("Visit bettersellingwithbailey.com", LINKS["bswb"]), ("Facebook", LINKS["bswb_fb"])])

entry("oddway", "oddway", "Take The OddWay",
      "Take The OddWay is a road-trip discovery platform by Dorian Bailey for finding cryptids, folklore, haunted places and roadside oddities.",
      "A road-trip guide to the strange: cryptids, folklore, haunted places and roadside oddities along your route.",
      """          <p>Give OddWay a route and it finds the detours worth taking: Bigfoot sightings, local legends, haunted hotels, UFO landmarks, odd little museums and giant roadside statues.</p>
          <p>I designed and built it end to end, from the brand and the research behind every stop to the web app itself, written in Next.js and TypeScript on Supabase. Stops are sorted into seven categories: cryptids, folklore, haunted, UFOs, weird history, museums and roadside oddities.</p>""",
      [("Founded by", "Dorian Bailey"),
       ("Subject", "Cryptids, folklore and roadside Americana"),
       ("Categories", "Seven"),
       ("Built with", "Next.js, React, TypeScript, Tailwind CSS, Supabase"),
       ("Also", f'<a href="{LINKS["shop"]}" rel="noopener">The OddWay shop</a>')],
      [P("green-eyes", 7, "<em>Mothman and Bigfoot, from Green Eyes</em>"),
       P("green-eyes", 5, "<em>Bigfoot, from Green Eyes</em>"),
       P("letchworth", 7, "<em>The gorge, from Letchworth</em>")],
      [("Visit taketheoddway.com", LINKS["oddway"]), ("Shop the OddWay", LINKS["shop"])])

entry("metazoo", "metazoo", "Bailey MetaZoo",
      "Bailey MetaZoo is Dorian Bailey's YouTube and Instagram channel on MetaZoo, the cryptid trading card game, and the folklore behind it.",
      "Short films on MetaZoo, the cryptid trading card game, and the folklore behind its cards.",
      """          <p>MetaZoo is a trading card game built from cryptids, folklore and the paranormal. Bailey MetaZoo covers the game and the legends it draws on: the Squonk, the Loveland Frogman, Old Scratch, and which cryptid haunts your state.</p>
          <p>Alongside the lore there are new set releases, pack openings, giveaways, and a signature format: the VHS reveal, where a tape goes into the deck, the old set flickers on, and the cards flash through static before the best one lands.</p>
          <p>Off camera, I photograph events for MetaZoo TCG itself, including the Green Eyes Festival, the Mothman Festival and Legends. The plates below are from <a href="../photography/#green-eyes">Green Eyes</a>.</p>""",
      [("Platforms", f'<a href="{LINKS["yt"]}" rel="noopener">YouTube</a> and <a href="{LINKS["ig"]}" rel="noopener">Instagram</a>'),
       ("Handle", "@baileymetazoo"),
       ("Subject", "MetaZoo and cryptid folklore"),
       ("Format", "Short vertical video"),
       ("Role", "Creator, host and editor"),
       ("Also", '<a href="../photography/">Event photographer for MetaZoo TCG</a>')],
      [P("green-eyes", 14, "<em>A MetaZoo card, from Green Eyes</em>"),
       P("green-eyes", 13, "<em>A MetaZoo cap, from Green Eyes</em>"),
       P("green-eyes", 3, "<em>The binder, from Green Eyes</em>")],
      [("Watch on YouTube", LINKS["yt"]), ("Follow on Instagram", LINKS["ig"])])

# ===================================================================== Photographs
index_items, sections = [], []
running = 0
for c in M["collections"]:
    cov = next(p for p in c["photos"] if p["thumb"] == c["cover"])
    w, h = thumb_dims(cov)
    n = len(c["photos"])
    index_items.append(f"""          <li>
            <a href="#{c['id']}">
              <span class="frame"><img src="../assets/photos/{c['cover']}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async"></span>
              <span class="coll-index__num">{c['numeral']}</span>
              <span class="coll-index__title">{c['title']}</span>
              <span class="coll-index__meta">{('Commissioned by ' + c['commission'] + '<br>') if c.get('commission') else ''}{c['place']}<br>{n} plates</span>
            </a>
          </li>""")
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
      <img src="../assets/photos/{BANNER['file']}" alt="{html.escape(BANNER['alt'])}" width="{BANNER['w']}" height="{BANNER['h']}" fetchpriority="high" decoding="async">
      <figcaption class="wrap"><em>Letchworth State Park, New York, October 2026</em></figcaption>
    </figure>

    <section class="section" aria-labelledby="commissions-title">
      <div class="wrap">
        <h2 class="section-title" id="commissions-title">Commissions</h2>
        <dl class="ledger">
          <div class="ledger__row">
            <dt>Event photographer</dt>
            <dd>
              <h3>MetaZoo TCG</h3>
              <p>Professional coverage of MetaZoo TCG at cryptid festivals: players at the tables, the cards they pull, costumed cryptids, and the crowds that come to see them.</p>
              <ul class="events">
                <li><a href="#green-eyes">Green Eyes Festival</a> <em>Chickamauga, Georgia, October 2026</em></li>
                <li>Mothman Festival <em>Point Pleasant, West Virginia, September 2026</em></li>
                <li>Legends</li>
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

    <section class="section section--rule" aria-labelledby="collections-title">
      <div class="wrap">
        <div class="section-head">
          <h2 class="section-title" id="collections-title">Collections</h2>
          <p class="section-head__note">{TOTAL} plates in {NUMWORD.lower()} collections</p>
        </div>
        <ol class="coll-index">
{chr(10).join(index_items)}
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
              <p><em>Event photographer.</em> Commissioned coverage at the Green Eyes Festival, the Mothman Festival and Legends.</p>
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
