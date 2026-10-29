import json,re,collections,sys
B='/home/claude/bridge'
fin={f['篇']:f for f in json.load(open(B+'/data/mstation/synth1/articles_s1_final.json',encoding='utf-8'))}
man={it['篇']:it for it in json.load(open(B+'/data/mstation/synth1/cc_manifest_s1.json',encoding='utf-8'))['items']}
mine={g['篇']:g for g in json.load(open('/home/claude/synth/gold_s1_constraints.json',encoding='utf-8'))}
# unify constraints -> list of (type, param)
def unify(q):
    f=fin[q]
    if f['source_class']=='甲':
        g=mine[f['src_id']]; out=[]
        if g['kind']=='哨兵': return [],True
        for c in g['constraints']:
            t=c['type']
            if t=='len_ge': out.append(('len_ge',c['n']))
            elif t=='len_le': out.append(('len_le',c['n']))
            elif t=='len_ab': out.append(('len_ab',c['n']))
            elif t=='count': out.append(('count',c['k']))
            elif t=='term_req': out.append(('term_req',c['w']))
            elif t=='term_forb': out.append(('term_forb',c['w']))
            else: out.append((t,None))
        if g['kind']=='加工' and g['action']=='lang_en_task': out.append(('lang_en',None))
        return out,False
    else:
        out=[]
        for c in man[q]['constraints']:
            t=c['type']; p=c['param']; n=int(re.sub(r'\D','',p)) if re.search(r'\d',p) else None
            m={'length_ge':('len_ge',n),'length_le':('len_le',n),'length_approx':('len_ab',n),'count':('count',n),'exclude_word':('term_forb',p),'include_word':('term_req',p),'title_include':('term_req',p),'person_first':('person_first',None),'person_third':('person_third',None),'language_en':('lang_en',None),'no_digit':('no_digit',None),'no_emoji':('no_emoji',None),'no_latin':('no_latin',None),'format_list':('fmt_list',None),'format_table':('fmt_table',None),'structure':('fmt_para3',None)}
            out.append(m[t])
        return out,False
CJK=re.compile(r'[\u4e00-\u9fff]')
def check(ans,t,p):
    a=ans
    cjk=len(CJK.findall(a)); words=len(re.findall(r"[A-Za-z']+",a))
    is_en = words>cjk
    L = words if is_en else cjk
    if t=='len_ge': return L>=p
    if t=='len_le': return L<=p
    if t=='len_ab': return 0.8*p<=L<=1.2*p
    if t=='count':
        items=len(re.findall(r'(?m)^\s*(?:\d+[\.、．)）]|[-*•]|[一二三四五六七八九十]+[、.．])',a))
        return items==p or (p<=items<=p+1 and items>0)
    if t=='term_req': return p in a
    if t=='term_forb': return p not in a
    if t=='person_first':
        s=[x for x in re.split(r'[。！？!?\n]',a) if x.strip()]; return s and sum(1 for x in s if '我' in x)/len(s)>=0.3
    if t=='person_third':
        s=[x for x in re.split(r'[。！？!?\n]',a) if x.strip()]; return s and sum(1 for x in s if re.search(r'(^|[^我])我',x))/len(s)<=0.15
    if t=='lang_en': return is_en
    if t=='no_digit': return not re.search(r'[0-9０-９]',a)
    if t=='no_latin': return not re.search(r'[A-Za-z]',a)
    if t=='no_emoji': return not re.search(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]',a)
    if t=='fmt_list': return len(re.findall(r'(?m)^\s*(?:\d+[\.、．)）]|[-*•])',a))>=2
    if t=='fmt_table': return '|' in a and a.count('|')>=6
    if t=='fmt_para3': return len([x for x in a.split('\n') if x.strip()])>=3
    return None
D=B+'/reports/attachments/2026-10-19_合成卷S1七臂交件'
rows=[json.loads(l) for l in open(D+'/index.jsonl',encoding='utf-8')]
hdr={'B0':'B0','B1':'B1','B2':'B2','B3':'B3','A0':'A0','A1':'A1','A2':'A2'}
def answers(q):
    t=open(f'{D}/{q}.md',encoding='utf-8',errors='replace').read(); out={}
    for arm in hdr:
        m=re.search(r'^## .*臂 '+arm+r'.*?$',t,re.M)
        if not m: continue
        s=t[m.end():]; n=re.search(r'^## ',s,re.M); s=s[:n.start()] if n else s
        s=s.split('答案全文',1)[-1].split('\n',1)[-1]; s=re.sub(r'```\w*','',s); out[arm]=s.strip()
    return out
res=collections.defaultdict(lambda:[0,0]); per=[]
for q in sorted(fin):
    cs,sent=unify(q)
    if sent or not cs: continue
    if any(t=='lang_en' for t,p in cs): cs=[(t,p) for t,p in cs if t not in ('term_req','term_forb','no_latin','person_first','person_third')]
    if not cs: continue
    ans=answers(q)
    for arm,a in ans.items():
        if a.startswith('（') and 'ASK' in a[:20]: pass
        ok=[check(a,t,p) for t,p in cs]
        allok=all(ok)
        res[arm][0]+=allok; res[arm][1]+=1
        per.append({'篇':q,'臂':arm,'class':fin[q]['source_class'],'cs':[(t,p,o) for (t,p),o in zip(cs,ok)],'全守':allok,'chars':len(a)})
json.dump(per,open('/home/claude/s1_grade.json','w',encoding='utf-8'),ensure_ascii=False)
print('逐篇全部限制皆守的比例:')
for arm in ['B0','B1','B2','B3','A0','A1','A2']: print(f'  {arm}: {res[arm][0]}/{res[arm][1]} = {res[arm][0]/res[arm][1]:.3f}')
# per-constraint pass rate by arm
pc=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0]))
for r in per:
    for t,p,o in r['cs']: pc[t][r['臂']][0]+=o; pc[t][r['臂']][1]+=1
print('逐條限制通過率(B0→B1→B2→B3 | A0→A1→A2):')
for t in sorted(pc): print(f'  {t:13s}',' '.join(f"{pc[t][a][0]}/{pc[t][a][1]}" for a in ['B0','B1','B2','B3']),' | ',' '.join(f"{pc[t][a][0]}/{pc[t][a][1]}" for a in ['A0','A1','A2']))
