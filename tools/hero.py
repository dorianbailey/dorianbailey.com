"""Builds the small images for the moving collage behind the home title.
Reads the web-sized photos already in assets/photos and writes
assets/photos/hero/*.jpg (320px tall) plus assets/photos/hero.json.
Run from the repo root: python3 tools/hero.py"""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PH = os.path.join(ROOT, "assets", "photos")
OUT = os.path.join(PH, "hero")
H = 320

# (collection, plate number) — a mix from every collection
PICKS = {
    "legends": [1, 2, 5, 9, 11, 16, 23, 25, 26],
    "mothman": [1, 3, 6, 10, 13, 16],
    "green-eyes": [1, 4, 7, 13, 14, 15],
    "letchworth": [2, 4, 6, 7, 9],
    "north-east": [1, 2, 5, 6, 7, 9],
    "creatures": [1, 3, 4, 8, 10, 12],
    "studies": [4, 6, 7, 9],
}

m = json.load(open(os.path.join(PH, "photos.json")))
coll = {c["id"]: c for c in m["collections"]}

# Interleave collections so each row mixes events, landscapes and animals
queues = [[(cid, n) for n in nums] for cid, nums in PICKS.items()]
order = []
while any(queues):
    for q in queues:
        if q:
            order.append(q.pop(0))

os.makedirs(OUT, exist_ok=True)
items = []
for i, (cid, n) in enumerate(order, 1):
    ph = coll[cid]["photos"][n - 1]
    im = Image.open(os.path.join(PH, ph["file"])).convert("RGB")
    w = round(im.width * H / im.height)
    im = im.resize((w, H), Image.LANCZOS)
    name = f"h-{i:02d}.jpg"
    im.save(os.path.join(OUT, name), "JPEG", quality=72, optimize=True, progressive=True)
    items.append({"file": f"hero/{name}", "w": w, "h": H, "from": cid})

json.dump(items, open(os.path.join(PH, "hero.json"), "w"), indent=1)
print(len(items), "hero images")
