import re,sys,os
# HIG guidance = paragraphs that OPEN with a bold imperative sentence.
def rules(slug):
    p=f'md/{slug}.md'
    if not os.path.exists(p): return []
    out=[]
    for ln in open(p):
        m=re.match(r'^\s*(?:[-*]\s*)?\*\*(.+?)\*\*',ln)
        if m and len(m.group(1))>15: out.append(m.group(1).strip())
    return out
if __name__=='__main__':
    for s in sys.argv[1:]:
        r=rules(s); print(f'### {s} ({len(r)} rules)')
        for x in r: print('  -',x)
