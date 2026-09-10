"""Find GENUINE gaps: a rule is missing if its distinctive concept words
(rarest words in the corpus) are absent from the mapped reference file."""
import re,os,json,collections
from rules import rules
REF=os.path.expanduser('~/.claude/skills/apple-hig/references')
MAP=json.load(open('pagemap.json'))
# corpus document frequency to find distinctive words
df=collections.Counter()
import glob
for f in glob.glob('md/*.md'):
    for w in set(re.findall(r"[a-z]{5,}", open(f).read().lower())): df[w]+=1
cache={}
def reftext(f):
    if f not in cache: cache[f]=open(os.path.join(REF,f)).read().lower()
    return cache[f]
out=[]
for slug,ref in MAP.items():
    if not ref: continue
    rt=reftext(ref)
    for r in rules(slug):
        if r.startswith('['): continue
        ws=set(re.findall(r"[a-z]{5,}", r.lower()))
        if not ws: continue
        # 3 rarest words = the concept signature
        sig=sorted(ws,key=lambda w:df.get(w,999))[:3]
        hit=sum(1 for w in sig if w in rt)
        if hit<len(sig):
            out.append((hit/len(sig),slug,ref,r,[w for w in sig if w not in rt]))
out.sort()
print(f"GENUINE GAP CANDIDATES: {len(out)}\n")
for score,slug,ref,r,miss in out:
    print(f"[{score:.2f}] {slug} -> {ref}")
    print(f"        {r[:135]}")
    print(f"        missing concepts: {miss}")
