"""Refreshes assets/data/youtube.json from the Bailey MetaZoo channel's public feed.
No API key needed. Run from the repo root: python3 tools/youtube.py
The GitHub Action in .github/workflows/youtube.yml runs this every six hours."""
import json, os, urllib.request
import xml.etree.ElementTree as ET

CHANNEL = "UCeZ6kCNgkXWFRaLJTQVem8g"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "youtube.json")
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

req = urllib.request.Request(FEED, headers={"User-Agent": "dorianbailey.com feed refresh"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
videos = []
for e in root.findall("a:entry", NS):
    videos.append({
        "id": e.find("yt:videoId", NS).text,
        "title": e.find("a:title", NS).text,
        "published": e.find("a:published", NS).text[:10],
        "url": e.find("a:link", NS).get("href"),
    })
if not videos:
    raise SystemExit("Feed returned no videos; leaving the existing file alone.")
data = {"channel": CHANNEL, "videos": videos}
with open(OUT, "w") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
print(len(videos), "videos")
