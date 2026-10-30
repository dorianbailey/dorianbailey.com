# dorianbailey.com

Personal portfolio and resume site for Dorian Bailey, and the front door to every brand:

| Section | Path | Links out to |
|---|---|---|
| Home (hero, work, highlights, about, contact) | `/` | |
| Resume | `/resume/` | |
| Bailey MetaZoo | `/metazoo/` | channel links (TBD) |
| Take The OddWay | `/oddway/` | taketheoddway.com, shoptheoddway.com |
| Better Selling With Bailey | `/better-selling/` | bettersellingwithbailey.com |
| Photography | `/photography/` | |

## Stack

Plain HTML, CSS and JavaScript. No build step: edit a file, commit, and GitHub Pages publishes it.

```
index.html            Home
resume/ metazoo/ oddway/ better-selling/ photography/   One folder per page
404.html              Not-found page
css/base.css          All styles. Colors, fonts and spacing are tokens at the top (:root)
js/main.js            Mobile menu + footer year
js/gallery.js         Photography grid + lightbox, driven by assets/photos/photos.json
assets/img/           Site images (headshot)
assets/photos/        Photography (see assets/photos/README.md)
CNAME                 Custom domain for GitHub Pages
```

The header and footer are repeated in each page. If you add a page, copy an existing one and add it to the nav in every page and to `sitemap.xml`.

## Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Hosting

GitHub Pages, deployed from the `main` branch root, with the custom domain `dorianbailey.com`.

DNS records at the domain registrar:

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | dorianbailey.github.io |

After DNS resolves, turn on **Enforce HTTPS** in Settings → Pages.
