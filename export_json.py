import pandas as pd, json

EXCLUDE = ['Kavyal Sedanni','Dr. Tamanna C','Dr. Rashmi N Muthalkar','Munisha Khatwani']

def session_list(sub):
    top = sub.sort_values('PV', ascending=False).head(5)
    return [{
        'name':str(r['name_clean']),'leader':str(r['leader_name']),
        'PV':int(r['PV']),'cart':float(r['RC_rate']),'sale':float(r['RS_rate']),
        'price':int(r['price']),'type':str(r['type']),
        'date':str(r['startIST'])[:16] if pd.notna(r.get('startIST')) else ''
    } for _,r in top.iterrows()]

def build(df, single_kw=False):
    def pooled_rows(col, order=None):
        out=[]
        for k, sub in df.groupby(col):
            pv=sub['PV'].sum()
            out.append({'key':str(k),'n':int(len(sub)),'PV_total':int(pv),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/pv) if pv else None,
                        'sale':float(100*sub['sales'].sum()/pv) if pv else None})
        if order:
            out = sorted(out, key=lambda r: order.index(r['key']) if r['key'] in order else 999)
        return out

    d = {}
    d['overall'] = {
        'sessions': int(len(df)), 'PV_total': int(df['PV'].sum()),
        'cart': float(100*df['carts'].sum()/df['PV'].sum()),
        'sale': float(100*df['sales'].sum()/df['PV'].sum()),
        'PV_median': float(df['PV'].median()),
        'carts_total': int(df['carts'].sum()), 'sales_total': int(df['sales'].sum()),
    }
    d['type'] = pooled_rows('type')
    d['price_tier'] = pooled_rows('price_tier', ['0 Free','1-300','301-600','601-1000','1001-1500','1500+'])
    d['dow'] = pooled_rows('dow_name', ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    d['time'] = pooled_rows('time_bucket', ['1 Early AM (<9)','2 Late Morning (9-12)','3 Afternoon (12-15)','4 Late Afternoon (15-18)','5 Evening (18-21)','6 Night (21+)'])

    dd = df.copy()
    dd['wordq'] = pd.qcut(dd['name_len_words'], 4, duplicates='drop')
    wq=[]
    for k,sub in dd.groupby('wordq', observed=True):
        pv=sub['PV'].sum()
        wq.append({'key':str(k),'n':int(len(sub)),'PV_total':int(pv),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/pv),'sale':float(100*sub['sales'].sum()/pv)})
    d['wordq']=wq

    kws=[]
    kw_sessions={}
    if single_kw:
        # Each session under exactly ONE main keyword (short titles)
        for key, sub in df.groupby('main_keyword'):
            if len(sub) < 3: continue
            pv=sub['PV'].sum()
            kws.append({'key':str(key),'n':int(len(sub)),'PV_total':int(pv),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
                        'sale':float(100*sub['sales'].sum()/pv) if pv else 0})
            kw_sessions[str(key)]=session_list(sub)
    else:
        # Multi-tag: a session appears under every theme word it contains
        for c in [c for c in df.columns if c.startswith('kw_')]:
            sub=df[df[c]==1]
            if len(sub)<15: continue
            key=c[3:].replace('_',' ')
            pv=sub['PV'].sum()
            kws.append({'key':key,'n':int(len(sub)),'PV_total':int(pv),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
                        'sale':float(100*sub['sales'].sum()/pv) if pv else 0})
            kw_sessions[key]=session_list(sub)
    d['keywords']=sorted(kws,key=lambda r:-r['PV_total'])
    d['keyword_sessions']=kw_sessions
    d['kw_mode']='single' if single_kw else 'multi'

    lt=[]
    for k,sub in df.groupby('leader_name'):
        if len(sub)<3: continue
        pv=sub['PV'].sum()
        lt.append({'key':str(k),'n':int(len(sub)),'PV_total':int(pv),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
                   'sale':float(100*sub['sales'].sum()/pv) if pv else 0})
    d['leaders']=sorted(lt,key=lambda r:-r['PV_total'])

    mt=[]
    for k,sub in df.groupby('month'):
        if len(sub)<5: continue
        pv=sub['PV'].sum()
        mt.append({'key':str(k),'n':int(len(sub)),'PV_total':int(pv),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
                   'sale':float(100*sub['sales'].sum()/pv) if pv else 0})
    d['monthly']=sorted(mt,key=lambda r:r['key'])
    return d

df = pd.read_csv('merged_analysis.csv')
no4 = df[~df['leader_name'].isin(EXCLUDE)].copy()
online_no4 = no4[no4['type'] != 'OFFLINE'].copy()
out = {
    'all': build(df),
    'filtered': build(no4),
    'online_clean': build(online_no4),
    'online_single': build(online_no4, single_kw=True),
    'excluded_leaders': EXCLUDE,
}
with open('dashboard_data.json','w') as f:
    json.dump(out,f,indent=1)
print('wrote dashboard_data.json (all + filtered + online_clean + online_single)')
for k in ['all','filtered','online_clean','online_single']:
    print(f'{k:14s}:', out[k]['overall'])
print('single-kw categories:', len(out['online_single']['keywords']))
