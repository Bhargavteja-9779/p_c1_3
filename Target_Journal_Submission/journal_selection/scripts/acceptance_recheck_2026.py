import json,sys,urllib.request,statistics,datetime as dt,re
def get(issn,year,rows=1000):
    url=f"https://api.crossref.org/journals/{issn}/works?filter=from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,type:journal-article&rows={rows}&select=DOI,assertion,title"
    try: d=json.load(urllib.request.urlopen(url,timeout=60))
    except Exception as e: return None,str(e)
    days=[]
    for it in d['message']['items']:
        a={x.get('name','').lower():x.get('value','') for x in it.get('assertion',[])}
        r=a.get('received'); c=a.get('accepted')
        if r and c:
            try:
                f=lambda s: dt.datetime.strptime(s.strip()[:10] if re.match(r'\d{4}-',s) else s.strip(), '%Y-%m-%d' if re.match(r'\d{4}-',s) else '%d %B %Y')
                days.append((f(c)-f(r)).days)
            except Exception: pass
    return days,d['message']['total-results']
for line in sys.argv[1:]:
    name,issn=line.split('=')
    for y in (2025,2026):
        days,tot=get(issn,y)
        if days is None or not days: print(f"{name:35s} {issn} {y} total={tot} n_dates=0"); continue
        days=[x for x in days if 0<x<1500]
        q=statistics.quantiles(days,n=4)
        print(f"{name:35s} {issn} {y} total={tot} n={len(days)} median={statistics.median(days)} q1={q[0]} q3={q[2]} le72={sum(x<=72 for x in days)/len(days):.2f}")
