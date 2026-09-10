"""Line-level semantic presence check: a rule is PRESENT if some window of the
mapped reference file shares a high fraction of the rule's content words."""
import re,os,json
from rules import rules
REF=os.path.expanduser('~/.claude/skills/apple-hig/references')
MAP=json.load(open('pagemap.json'))
STOP=set("""the a an of to in for and or your you people be is are with that this it on as can when
if make use using their they them how what more so at by from not do don't dont a's you're it's its
also when where which who while into out up down more most other some such only own same than then
too very just about after before over under again once here there all any both each few nor own
because until against between during above below have has had was were been being will would should
could may might must shall can't cannot let lets let's""".split())
def toks(s): return [w for w in re.findall(r"[a-z']{3,}", s.lower()) if w not in STOP]
present=[];missing=[]
for slug,ref in MAP.items():
    if not ref: continue
    lines=[l for l in open(os.path.join(REF,ref)).read().split('\n')]
    # windows of 3 consecutive lines
    wins=[' '.join(lines[i:i+4]).lower() for i in range(len(lines))]
    winsets=[set(toks(w)) for w in wins]
    for r in rules(slug):
        if r.startswith('['): continue
        t=set(toks(r))
        if len(t)<3: continue
        best=max((len(t&w)/len(t) for w in winsets), default=0)
        (present if best>=0.6 else missing).append((round(best,2),slug,ref,r))
missing.sort()
tot=len(present)+len(missing)
print(f"LINE-LEVEL VERIFY: {tot} rules | present {len(present)} ({100*len(present)/tot:.1f}%) | to review {len(missing)}")
print()
for b,s,f,r in missing: print(f"[{b}] {s} ({f})\n     {r[:145]}")
