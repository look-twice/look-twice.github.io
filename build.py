"""Build Look Twice test pages from images/manifest.json.

  python3 build.py            -> site/index.html (images referenced from site/img/) and preview.html (images inlined)
Picks 12 items: 6 real + 6 AI, two easy ones first, then medium, hard last, answers mixed.
"""
import base64
import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
man = json.loads((ROOT / "images" / "manifest.json").read_text())
chosen_path = ROOT / "chosen.json"
if chosen_path.exists():  # a hand-picked order wins
    order = json.loads(chosen_path.read_text())
    items = [next(m for m in man if m["file"] == f) for f in order]
else:
    rng = random.Random(1)
    real = sorted([m for m in man if m["answer"] == "real"], key=lambda m: m["difficulty"])[:6]
    ai = sorted([m for m in man if m["answer"] == "ai"], key=lambda m: m["difficulty"])[:6]
    items = real + ai
    rng.shuffle(items)
    items.sort(key=lambda m: m["difficulty"])

tpl = (ROOT / "template.html").read_text()
keys = ["answer", "title", "giveaway", "author", "licence", "licence_url", "source_url"]
from PIL import Image
def extra(m):
    w, h = Image.open(ROOT / "images" / m["file"]).size
    return {"ar": round(h / w, 4), "spots": m.get("spots", [])}

site = ROOT / "site"
(site / "img").mkdir(parents=True, exist_ok=True)
web = []
for i, m in enumerate(items, 1):
    name = f"{i:02d}.jpg"  # neutral names: the file name must not give the answer away
    shutil.copy(ROOT / "images" / m["file"], site / "img" / name)
    web.append({"src": f"img/{name}", **{k: m[k] for k in keys}, **extra(m)})
(site / "index.html").write_text(tpl.replace("/*__DATA__*/[]", json.dumps(web, ensure_ascii=False)))

inline = []
for m in items:
    b64 = base64.b64encode((ROOT / "images" / m["file"]).read_bytes()).decode()
    inline.append({"src": f"data:image/jpeg;base64,{b64}", **{k: m[k] for k in keys}, **extra(m)})
(ROOT / "preview.html").write_text(tpl.replace("/*__DATA__*/[]", json.dumps(inline, ensure_ascii=False)))
print("built", len(items), "items:", ", ".join(f'{m["file"]}({m["difficulty"]})' for m in items))
