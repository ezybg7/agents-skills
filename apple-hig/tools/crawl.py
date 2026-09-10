import hig2md as H, json, os, sys, collections

root = H.fetch('')  # root
tree = collections.OrderedDict()
order = []
seen = set()

def refs_urls(d):
    return d.get('references',{})

def kids_of(d):
    refs = d.get('references',{})
    out=[]
    for ts in (d.get('topicSections') or []):
        sect = ts.get('title')
        for ident in ts.get('identifiers',[]):
            r = refs.get(ident,{})
            u = r.get('url','')
            low = u.lower()
            if '/design/human-interface-guidelines/' in low:
                slug = u[low.index('/design/human-interface-guidelines/')+len('/design/human-interface-guidelines/'):].strip('/')
                if slug: out.append((slug, r.get('title',''), sect))
    return out

queue = [(s,t,sec,'root') for s,t,sec in kids_of(root)]
inventory = []
while queue:
    slug, title, sect, parent = queue.pop(0)
    if slug in seen: continue
    seen.add(slug)
    d = H.fetch(slug)
    if d is None: continue
    inventory.append({'slug':slug,'title':title or slug,'parent':parent,'section':sect})
    for s,t,sec in kids_of(d):
        if s not in seen: queue.append((s,t,sec,slug))
    sys.stderr.write(f'\r{len(inventory)} pages')

json.dump(inventory, open('inventory.json','w'), indent=1)
sys.stderr.write(f'\nDONE {len(inventory)} pages\n')
print('UNKNOWN:', H.UNKNOWN)
