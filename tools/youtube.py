"""Refreshes assets/data/youtube.json from the Bailey MetaZoo channel's public feed.
No API key needed. Run from the repo root: python3 tools/youtube.py
The GitHub Action in .github/workflows/youtube.yml runs this every six hours."""
import json, os, sys, time, urllib.request
import xml.etree.ElementTree as ET

CHANNEL = "UCeZ6kCNgkXWFRaLJTQVem8g"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "data", "youtube.json")
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

# YouTube's feed now and then answers 404 or 500 for a few minutes. Try a few times, and if it
# still won't answer, keep the current list and finish quietly; the next run will catch up.
req = urllib.request.Request(FEED, headers={"User-Agent": "dorianbailey.com feed refresh"})
root = None
for attempt in range(4):
    try:
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        break
    except Exception as err:
        print(f"Feed attempt {attempt + 1} failed: {err}")
        time.sleep(20 * (attempt + 1))
if root is None:
    print("The feed didn't answer; leaving the existing file alone until the next run.")
    sys.exit(0)
videos = []
for e in root.findall("a:entry", NS):
    videos.append({
        "id": e.find("yt:videoId", NS).text,
        "title": e.find("a:title", NS).text,
        "published": e.find("a:published", NS).text[:10],
        "url": e.find("a:link", NS).get("href"),
    })
if not videos:
    print("Feed returned no videos; leaving the existing file alone.")
    sys.exit(0)
data = {"channel": CHANNEL, "videos": videos}
with open(OUT, "w") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
print(len(videos), "videos")
