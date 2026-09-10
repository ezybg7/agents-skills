import json, sys, re, os, urllib.request, time

UA = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'}
BASE = "https://developer.apple.com/tutorials/data/design/Human-Interface-Guidelines/"
UNKNOWN = set()

def fetch(slug, cache='raw'):
    os.makedirs(cache, exist_ok=True)
    fn = os.path.join(cache, slug.replace('/','__')+'.json')
    if os.path.exists(fn) and os.path.getsize(fn)>100:
        return json.load(open(fn))
    url = BASE + slug + '.json' if slug else "https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = urllib.request.urlopen(req, timeout=45).read()
            d = json.loads(data)
            open(fn,'wb').write(data)
            return d
        except Exception as e:
            if attempt==2:
                print(f"  !! FAIL {slug}: {e}", file=sys.stderr); return None
            time.sleep(2)

def inline(nodes, refs):
    out=[]
    for n in nodes or []:
        t=n.get('type')
        if t=='text': out.append(n.get('text',''))
        elif t=='emphasis': out.append('*'+inline(n.get('inlineContent'),refs)+'*')
        elif t=='strong': out.append('**'+inline(n.get('inlineContent'),refs)+'**')
        elif t=='inlineHead': out.append('**'+inline(n.get('inlineContent'),refs)+'**')
        elif t=='codeVoice': out.append('`'+n.get('code','')+'`')
        elif t=='newTerm': out.append('**'+inline(n.get('inlineContent'),refs)+'**')
        elif t=='superscript': out.append('^'+inline(n.get('inlineContent'),refs))
        elif t=='subscript': out.append('_'+inline(n.get('inlineContent'),refs))
        elif t=='strikethrough': out.append('~~'+inline(n.get('inlineContent'),refs)+'~~')
        elif t=='reference':
            r=refs.get(n.get('identifier'),{})
            title=r.get('title') or ''.join(x.get('text','') for x in r.get('titleInlineContent',[]) if isinstance(x,dict))
            out.append(title or n.get('identifier','').split('/')[-1])
        elif t=='link': out.append(n.get('title',''))
        elif t=='image':
            r=refs.get(n.get('identifier'),{})
            alt=r.get('alt') or ''
            if alt: out.append(f'[img: {alt}]')
        else:
            if 'inlineContent' in n: out.append(inline(n['inlineContent'],refs))
            elif 'text' in n: out.append(n['text'])
            else: UNKNOWN.add('inline:'+str(t))
    return ''.join(out)

def block(nodes, refs, lvl=2, indent=''):
    out=[]
    for n in nodes or []:
        t=n.get('type')
        if t=='paragraph':
            s=inline(n.get('inlineContent'),refs).strip()
            if s: out.append(indent+s)
        elif t=='heading':
            l=min(n.get('level',lvl),6)
            out.append('#'*l+' '+n.get('text','').strip())
        elif t=='aside':
            name=(n.get('name') or n.get('style','note')).upper()
            inner=block(n.get('content'),refs,lvl,'')
            body='\n'.join('> '+ln if ln.strip() else '>' for ln in inner.split('\n'))
            out.append(f'> **{name}:**\n{body}')
        elif t in ('unorderedList','orderedList'):
            for i,it in enumerate(n.get('items',[])):
                mark = f'{i+1}.' if t=='orderedList' else '-'
                inner=block(it.get('content'),refs,lvl,'').strip()
                lines=inner.split('\n')
                out.append(indent+mark+' '+lines[0])
                for ln in lines[1:]:
                    out.append(indent+'  '+ln)
        elif t=='termList':
            for it in n.get('items',[]):
                term=inline(it.get('term',{}).get('inlineContent'),refs)
                dfn=block(it.get('definition',{}).get('content'),refs,lvl,'').strip()
                out.append(f'{indent}- **{term}** — {dfn}')
        elif t=='codeListing':
            code='\n'.join(n.get('code',[]))
            out.append('```'+(n.get('syntax') or '')+'\n'+code+'\n```')
        elif t=='table':
            hdr=n.get('header')
            rows=n.get('rows',[])
            if not rows: continue
            md=[]
            def cell(c): return inline(c[0].get('inlineContent'),refs).replace('|','\\|') if c and isinstance(c[0],dict) else ' '.join(inline(x.get('inlineContent'),refs) for x in c if isinstance(x,dict))
            def row2(r): return '| '+' | '.join(block(c,refs,lvl,'').replace('\n',' ').replace('|','\\|') for c in r)+' |'
            start=0
            if hdr in ('row','both'):
                md.append(row2(rows[0])); md.append('|'+'---|'*len(rows[0])); start=1
            else:
                md.append('|'+' |'*len(rows[0])); md.append('|'+'---|'*len(rows[0]))
            for r in rows[start:]: md.append(row2(r))
            out.append('\n'.join(md))
        elif t=='image':
            r=refs.get(n.get('identifier'),{})
            alt=r.get('alt')
            if alt: out.append(f'{indent}![{alt}]')
        elif t=='tabNavigator':
            for tab in n.get('tabs',[]):
                out.append(f'{indent}**[{tab.get("title","")}]**')
                out.append(block(tab.get('content'),refs,lvl,indent))
        elif t in ('row',):
            for col in n.get('columns',[]): out.append(block(col.get('content'),refs,lvl,indent))
        elif t=='small':
            out.append(indent+'_'+inline(n.get('inlineContent'),refs)+'_')
        elif t in ('video','links','thematicBreak','deprecationSummary'):
            if n.get('content'): out.append(block(n.get('content'),refs,lvl,indent))
        else:
            UNKNOWN.add('block:'+str(t))
            if n.get('content'): out.append(block(n.get('content'),refs,lvl,indent))
            elif n.get('inlineContent'): out.append(indent+inline(n['inlineContent'],refs))
    return '\n\n'.join(x for x in out if x.strip())

def page_md(d):
    refs=d.get('references',{})
    md=[]
    title=d.get('metadata',{}).get('title','')
    md.append('# '+title)
    ab=inline(d.get('abstract'),refs).strip()
    if ab: md.append('_'+ab+'_')
    for sec in d.get('primaryContentSections',[]):
        if sec.get('kind')=='content': md.append(block(sec.get('content'),refs))
        elif sec.get('content'): md.append(block(sec.get('content'),refs))
    return '\n\n'.join(md), refs

def children(d):
    """Return ordered list of (slug) for topicSections + seeAlso of this page."""
    refs=d.get('references',{})
    kids=[]
    for ts in (d.get('topicSections') or []):
        for ident in ts.get('identifiers',[]):
            r=refs.get(ident,{})
            u=r.get('url','')
            if '/design/Human-Interface-Guidelines/' in u.replace('human-interface-guidelines','Human-Interface-Guidelines'):
                slug=u.split('Human-Interface-Guidelines/')[-1] if 'Human-Interface-Guidelines/' in u else u.split('human-interface-guidelines/')[-1]
                kids.append(slug.strip('/'))
    return kids
