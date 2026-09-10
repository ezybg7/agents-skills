"""Per-file coverage check: each page maps to ONE reference file.
Stricter than check.py, which searched the whole references dir."""
import re,sys,os,json
from rules import rules
STOP=set("the a an of to in for and or your you people be is are with that this it on as can when if make use using their they them how what more so at by from not do don't avoid consider prefer ensure keep help provide give show".split())
REF=os.path.expanduser('~/.claude/skills/apple-hig/references')
# page slug -> reference file
MAP=json.load(open('pagemap.json'))
cache={}
def reftext(f):
    if f not in cache: cache[f]=set(re.findall(r"[a-z]{4,}",open(os.path.join(REF,f)).read().lower()))
    return cache[f]
def toks(s): return {w for w in re.findall(r"[a-z]{4,}",s.lower()) if w not in STOP}
missing=[];total=0;unmapped=set()
for slug,ref in MAP.items():
    if ref is None: unmapped.add(slug); continue
    rt=reftext(ref)
    for r in rules(slug):
        if r.startswith('['): continue
        total+=1
        t=toks(r)
        if not t: continue
        hit=len(t&rt)/len(t)
        if hit<0.72: missing.append((round(hit,2),slug,ref,r))
missing.sort()
print(f"PER-FILE CHECK: {total} rules, {len(missing)} below threshold ({100*(total-len(missing))/total:.1f}% clean)")
if unmapped: print("UNMAPPED PAGES:", sorted(unmapped))
print()
for h,s,f,r in missing: print(f"  [{h}] {s} -> {f}\n        {r[:150]}")
