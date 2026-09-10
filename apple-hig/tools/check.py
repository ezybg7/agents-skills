import re,sys,os
from rules import rules
STOP=set('the a an of to in for and or your you people be is are with that this it on as can when if make use using their they them how what more so at by from not do don''t avoid consider prefer ensure keep help provide give show'.split())
def toks(s):
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOP}
ref_dir=os.path.expanduser('~/.claude/skills/apple-hig/references')
refs=' '.join(open(os.path.join(ref_dir,f)).read().lower() for f in os.listdir(ref_dir))
reftok=re.findall(r"[a-z]{4,}",refs)
refset=set(reftok)
missing=[]
total=0
for slug in sys.argv[1:]:
    for r in rules(slug):
        total+=1
        t=toks(r)
        if not t: continue
        hit=len(t & refset)/len(t)
        if hit<0.72: missing.append((slug,round(hit,2),r))
print(f'checked {total} rules across {len(sys.argv)-1} pages; {len(missing)} weakly covered\n')
for s,h,r in missing: print(f'  [{h}] {s}: {r}')
