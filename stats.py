"""Look Twice numbers: python3 stats.py  (anonymous totals from abacus.jasoncameron.dev)."""
import json, urllib.request
NS = "looktwice-t1"
def get(k):
    try:
        with urllib.request.urlopen(f"https://abacus.jasoncameron.dev/get/{NS}/{k}", timeout=10) as r:
            return json.load(r).get("value", 0)
    except Exception:
        return 0  # a counter that was never hit does not exist yet
srcs = ["yt", "ig", "tt", "friend", "ref", "direct"]
visits = {s: get("visit-" + s) for s in srcs}
v = sum(visits.values()); st = get("start")
fin = {i: get(f"finish-{i}") for i in range(13)}; f = sum(fin.values())
g = get("giveaways"); sh = get("share-top") + get("share-bottom")
pct = lambda a, b: f"{a / b:.0%}" if b else "-"
print(f"Opened the page   {v:>5}   " + ", ".join(f"{k} {n}" for k, n in visits.items() if n))
print(f"Started the test  {st:>5}   {pct(st, v)} of visitors")
print(f"Saw their result  {f:>5}   {pct(f, st)} of starters")
print(f"Read giveaways    {g:>5}   {pct(g, f)} of finishers")
print(f"Shared            {sh:>5}   {pct(sh, f)} of finishers")
if f: print("Scores: " + ", ".join(f"{i}:{n}" for i, n in fin.items() if n))
