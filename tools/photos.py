"""Builds web images + photos.json for the Photography collections."""
import json, os, io, sys
from PIL import Image, ImageOps, ImageCms, ImageChops

SRC = "/mnt/user-data/uploads/Photography"
OUT = "/home/claude/dorianbailey.com/assets/photos"
SRGB = ImageCms.createProfile("sRGB")

C = [
 dict(id="legends", numeral="I", title="Legends", place="Two-day tournament", date="August 2026",
      commission="MetaZoo TCG", root="/mnt/user-data/uploads/Dropbox/Legends Edits (Photo)/Legends Edits",
      note="Tournament play under convention-hall lights: the prize cards on their easels, players at the tables, the commentary desk, and the whole field together for one last photograph.",
      cover="IMG_0208", photos=[
  ("IMG_0123","An inflatable winged cryptid on a MetaZoo base"),
  ("IMG_0128","The first-place prize card on an easel"),
  ("IMG_0130","The second-place prize card on an easel"),
  ("IMG_0131","The third-place prize card on an easel"),
  ("IMG_0192","The MetaZoo Trading Card Game booth"),
  ("IMG_0193","A match underway"),
  ("IMG_0197","Players studying their hands"),
  ("IMG_0199","Concentration at the tournament tables"),
  ("IMG_0201","A player fanning his cards"),
  ("IMG_0202","Holding a hand of cards across the table"),
  ("IMG_0208","The commentary desk in front of a MetaZoo backdrop"),
  ("IMG_0226","Signing cards at the table"),
  ("IMG_0234","A player weighing his next move"),
  ("IMG_0238","A player in a MetaZoo cap mid-match"),
  ("IMG_0248","A player beside the inflatable cryptid"),
  ("IMG_0267","A match at the feature table"),
  ("IMG_0268","A reaction across the table"),
  ("IMG_0278","A player in glasses mid-game"),
  ("IMG_0279","Players at the tables"),
  ("IMG_0289","A match on the clock"),
  ("IMG_0300","Two players deep in a match"),
  ("IMG_0304","A match beneath the stream camera"),
  ("IMG_0312","Rows of Old Green Eyes cards"),
  ("IMG_0314","A Mothman Festival edition card in its sleeve"),
  ("IMG_0315","A Loveland Frogman card"),
  ("IMG_0325","The players together beneath the inflatable cryptid"),
 ]),
 dict(id="mothman", numeral="II", title="Mothman Festival", place="Point Pleasant, West Virginia", date="September 2026",
      commission="MetaZoo TCG", root="/mnt/user-data/uploads/Dropbox/Mothman Edited/Mothman Edited",
      note="MetaZoo TCG\u2019s booth on the festival street: players, pulls and playmats, and a few people dressed for the occasion.",
      cover="IMG_0988", photos=[
  ("IMG_0849","A couple posing before an inflatable Mothman at the MetaZoo booth"),
  ("IMG_0854","Crowds filling the festival street between brick storefronts"),
  ("IMG_0861","A signed MetaZoo Mothman print on an easel"),
  ("IMG_0862","A player checking his cards"),
  ("IMG_0889","Players gathered at the booth table"),
  ("IMG_0900","Festival-goers in feathered ears, and a dachshund in a sling"),
  ("IMG_0902","Browsing cards under the booth tent"),
  ("IMG_0907","Comparing pulls at the booth"),
  ("IMG_0916","Trading across the booth table"),
  ("IMG_0926","A festival-goer in red glasses and feathered ears"),
  ("IMG_0933","A young fan pointing out cards at the booth"),
  ("IMG_0936","A laughing player under the tent"),
  ("IMG_0952","Players shopping the booth display"),
  ("IMG_0958","Opening packs with a friend"),
  ("IMG_0985","Hands sorting cards over a playmat"),
  ("IMG_0988","Two fans holding up a MetaZoo playmat"),
 ]),
 dict(id="green-eyes", numeral="III", title="Green Eyes", place="Green Eyes Festival, Chickamauga, Georgia", date="October 2026",
      commission="MetaZoo TCG",
      note="A day of cryptids, costumes and card tables at a festival named for the battlefield legend of Ole’ Green Eyes.",
      cover="IMG_2147", photos=[
  ("Green Eyes Edited/IMG_2063","A small cryptid plush hanging from a vendor tent"),
  ("Green Eyes Edited/IMG_2093","Card players at a folding table in the street"),
  ("Green Eyes Edited/IMG_2098","Browsing a binder of trading cards"),
  ("Green Eyes Edited/IMG_2147","A Bigfoot costume waving beside a festival-goer"),
  ("Green Eyes Edited/IMG_2153","Bigfoot mid-stride, in black and white"),
  ("Green Eyes Edited/IMG_2166","Bigfoot waving as a child laughs"),
  ("Green Eyes Edited/IMG_2210","Mothman and Bigfoot side by side"),
  ("Green Eyes Edited/IMG_2254","Smiling over a card pull"),
  ("Green Eyes Edited/IMG_2264","A card match at a street table"),
  ("Green Eyes Edited/IMG_2267","A father and son sorting cards, a Stormtrooper behind"),
  ("Green Eyes Edited/IMG_2290","Costumed characters on the festival stage"),
  ("Green Eyes Edited/IMG_2306","A chicken costume on stage"),
  ("Green Eyes Edited/IMG_2337","A photographer in a MetaZoo cap behind a vintage camera"),
  ("Green Eyes Edited/IMG_2364","A MetaZoo card in a binder sleeve"),
  ("Green Eyes Edited/IMG_2381","A Jigsaw puppet on a tricycle with a smiling fan"),
 ]),
 dict(id="letchworth", numeral="IV", title="Letchworth", place="Letchworth State Park, New York", date="October 2026",
      note="The Genesee River gorge in early autumn: high falls, a railroad bridge, a passing rainbow, and the friends on the trail.",
      cover="IMG_1811", photos=[
  ("Letchworth Edited/IMG_1699","On a fallen log in the forest"),
  ("Letchworth Edited/IMG_1707","The gorge and a distant waterfall framed by autumn leaves"),
  ("Letchworth Edited/IMG_1734","A hiker with trekking poles above the river"),
  ("Letchworth Edited/IMG_1737","A thumbs-up above the rushing river"),
  ("Letchworth Edited/IMG_1742","Falls pouring into the gorge"),
  ("Letchworth Edited/IMG_1791","A rainbow across the gorge wall"),
  ("Letchworth Edited/IMG_1811","Mist rising beneath the railroad bridge"),
  ("Letchworth Edited/IMG_1816","Arms crossed at the overlook below the bridge"),
  ("Letchworth Edited/IMG_1822","A hiker in red at the stone railing below the bridge"),
 ]),
 dict(id="north-east", numeral="V", title="North East", place="North East, Pennsylvania", date="September–October 2026",
      note="Home: Halloween porches after dark, the park in full color, and the Wine Fest run through town.",
      cover="Ne-Night5", photos=[
  ("NE Night + Random/Ne-Night1","Street signs at the corner of Gibson and North Mill at night"),
  ("NE Night + Random/Ne-Night2","Giant skeletons and a skeleton dog on a lawn"),
  ("NE Night + Random/Ne-Night3","A porch glowing with Halloween lights"),
  ("NE Night + Random/Ne-night4","A skeleton lounging in magenta light"),
  ("NE Night + Random/Ne-Night5","A lit fountain statue at night"),
  ("NE Night + Random/Ne-Night6","Witch figures around a cauldron in violet light"),
  ("Park (October)/IMG_2468","A white statue and a pink ribbon flag among red maples"),
  ("Park (October)/IMG_2491","The park path under autumn trees"),
  ("Winefest Run Edited/WineFest1","Runners on a residential street"),
  ("Winefest Run Edited/WineFest2","A runner and a young racer mid-stride"),
  ("Winefest Run Edited/WineFest3","Walking the course with a setter"),
  ("Winefest Run Edited/WineFest4","A shaggy black dog on the course"),
 ]),
 dict(id="creatures", numeral="VI", title="Creatures", place="Pennsylvania", date="September–October 2026",
      note="Cats in window light, a poodle at the water bowl, horses, goats, and one woolly bear crossing the leaves.",
      cover="IMG_1048", photos=[
  ("Cats-Edited/IMG_1008","A cream cat resting on a leather chair"),
  ("Cats-Edited/IMG_1020","A cream cat, eyes half closed"),
  ("Cats-Edited/IMG_1029","A Siamese stepping toward the camera"),
  ("Cats-Edited/IMG_1048","A Siamese with blue eyes, head tilted on a table"),
  ("Cats-Edited/IMG_1054","A Siamese in profile"),
  ("Cats Random/IMG_1997","A Siamese mid-yawn on the floor"),
  ("Cats Random/IMG_2021","A cream cat curled on a windowsill"),
  ("Cats Random/IMG_2028","A cream cat beside a lion mask in the window"),
  ("Lorenzo Bday Edited/IMG_1951","A Siamese portrait"),
  ("Lorenzo Bday Edited/IMG_1912","A poodle in a bandana drinking from a bowl"),
  ("Lorenzo Bday Edited/IMG_1881","A woolly bear caterpillar among fallen leaves"),
  ("NE Night + Random/Random1","Two dark horses in harness"),
  ("NE Night + Random/Random2","A brown goat at the fence"),
  ("NE Night + Random/Random3","A black goat in dappled light"),
 ]),
 dict(id="studies", numeral="VII", title="Studies", place="Penn State Behrend and elsewhere", date="September–October 2026",
      note="Close looks at small things: fungi on fallen wood, asters, a weed in shale, and an eye.",
      cover="IMG_1551", photos=[
  ("Behrend Edited/IMG_1468","Ferns and fallen logs in the woods"),
  ("Behrend Edited/IMG_1472","A graffiti-covered trail sign in the woods"),
  ("Behrend Edited/IMG_1477","A small flowering plant growing from shale"),
  ("Behrend Edited/IMG_1516","White asters with a ladybug"),
  ("Behrend Edited/IMG_1542","Pale bracket fungus on a dark stump"),
  ("Behrend Edited/IMG_1551","Orange chicken-of-the-woods on a stump"),
  ("Behrend Edited/IMG_1559","Orange fungus spreading across a log"),
  ("Lorenzo Bday Edited/IMG_1886","A photographer at work among yellow leaves"),
  ("NE Night + Random/Random4","A close study of a green-blue eye"),
 ]),
]

def trim_border(im):
    """Remove a baked-in white mat (some Photoshop exports have one). Detects on a small copy."""
    small = im.copy(); small.thumbnail((600, 600))
    k = im.width / small.width
    diff = ImageChops.difference(small, Image.new("RGB", small.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 18 else 0)
    bb = diff.getbbox()
    if not bb: return im
    l, t, r, b = bb
    if min(l, t, small.width - r, small.height - b) > 0.015 * min(small.size):
        inset = 2
        return im.crop((round((l + inset) * k), round((t + inset) * k), round((r - inset) * k), round((b - inset) * k)))
    return im

def save(im, path, long_edge, q):
    im = im.copy(); im.thumbnail((long_edge, long_edge), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)  # no exif/icc -> metadata stripped
    return im.size

manifest = {"collections": []}
for c in C:
    d = os.path.join(OUT, c["id"]); os.makedirs(d, exist_ok=True)
    entries = []
    for i, (src, alt) in enumerate(c["photos"], 1):
        im = Image.open(os.path.join(c.get("root", SRC), src + ".jpg"))
        im = ImageOps.exif_transpose(im)
        icc = im.info.get("icc_profile")
        if icc:
            try:
                im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)), SRGB, outputMode="RGB")
            except Exception as e:
                print("icc fail", src, e)
        im = im.convert("RGB")
        im = trim_border(im)
        name = f"{c['id']}-{i:02d}.jpg"
        w, h = save(im, os.path.join(d, name), 2000, 82)
        save(im, os.path.join(d, "t-" + name), 900, 76)
        im.close() if hasattr(im, "close") else None
        e = {"file": f"{c['id']}/{name}", "thumb": f"{c['id']}/t-{name}", "alt": alt, "w": w, "h": h}
        if os.path.basename(src) == c["cover"]: c["coverFile"] = e["thumb"]
        entries.append(e)
    manifest["collections"].append({k: c[k] for k in ("id","numeral","title","place","date","note","commission") if k in c} | {"cover": c["coverFile"], "photos": entries})
    print(c["id"], len(entries))
json.dump(manifest, open(os.path.join(OUT, "photos.json"), "w"), indent=1, ensure_ascii=False)
