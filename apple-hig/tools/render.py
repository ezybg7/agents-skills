import hig2md as H, json, os, sys, glob
os.makedirs('md', exist_ok=True)
n=0
for fn in sorted(glob.glob('raw/*.json')):
    slug=os.path.basename(fn)[:-5]
    try: d=json.load(open(fn))
    except Exception: continue
    md,_=H.page_md(d)
    open(f'md/{slug}.md','w').write(md); n+=1
print(f'rendered {n}', 'UNKNOWN:', H.UNKNOWN, file=sys.stderr)
