import pandas as pd, json, re

# User's multi-tag keyword list (a session can match several). Matched on short name.
KW2 = [
 ('Grief',['grief','bereav','mourning','widow']),('Healing',['heal']),('Yourself',['yourself']),
 ('Karma',['karma']),('Karmic',['karmic']),('Gut',['gut']),('Death',['death']),
 ('Wealth',['wealth']),('Money',['money']),("Ho'oponopono",["ho'oponopono","hooponopono"]),
 ('Cord Cutting',['cord cut','cord cutting']),('Inherited',['inherit']),('Parent',['parent']),
 ('Inner',['inner']),('Chakra',['chakra']),('Manifest',['manifest']),('Block',['block']),
 ('Attract',['attract']),('Break',['break']),('Moon',['moon']),('Marriage',['marriage']),
 ('Divorce',['divorce']),('Love',['love']),
]
def kw2_block(dfc, session_list):
    name = dfc['disp_name'].astype(str).str.lower().str.replace('’', "'", regex=False)
    rows=[]; sess={}
    for label,pats in KW2:
        mask=None
        for p in pats:
            m=name.str.contains(re.escape(p), regex=True)
            mask = m if mask is None else (mask | m)
        sub=dfc[mask.values]
        if len(sub)==0: continue
        pv=sub['PV'].sum()
        rows.append({'key':label,'n':int(len(sub)),'PV_total':int(pv),
                     'PV_median':float(sub['PV'].median()),
                     'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
                     'sale':float(100*sub['sales'].sum()/pv) if pv else 0})
        sess[label]=session_list(sub)
    return sorted(rows,key=lambda r:-r['PV_total']), sess

EXCLUDE = ['Kavyal Sedanni','Dr. Tamanna C','Dr. Rashmi N Muthalkar','Munisha Khatwani']
CUTOFF = pd.Timestamp('2026-04-01')   # PV sections use sessions from 1 Apr 2026 onward
DOW_ORDER = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

# ---- Overall site page-views on course pages, by month x day-of-week (provided) ----
# Two baselines: ALL (every leader & type) and NO4 (excl 4 leaders & excl offline).
SITE_ALL_RAW = [
 ('Apr 2026','Friday',29399),('Apr 2026','Monday',33949),('Apr 2026','Saturday',22281),
 ('Apr 2026','Sunday',27720),('Apr 2026','Thursday',38756),('Apr 2026','Tuesday',29735),
 ('Apr 2026','Wednesday',41341),
 ('May 2026','Friday',46415),('May 2026','Monday',41131),('May 2026','Saturday',39507),
 ('May 2026','Sunday',44214),('May 2026','Thursday',36995),('May 2026','Tuesday',41041),
 ('May 2026','Wednesday',38970),
 ('Jun 2026','Friday',51387),('Jun 2026','Monday',59308),('Jun 2026','Saturday',37950),
 ('Jun 2026','Sunday',44420),('Jun 2026','Thursday',48538),('Jun 2026','Tuesday',60639),
 ('Jun 2026','Wednesday',51583),
 ('Jul 2026','Friday',13713),('Jul 2026','Monday',17423),('Jul 2026','Saturday',13055),
 ('Jul 2026','Sunday',16138),('Jul 2026','Thursday',17801),('Jul 2026','Tuesday',18431),
 ('Jul 2026','Wednesday',30024),
]
SITE_NO4_RAW = [
 ('Apr 2026','Friday',20768),('Apr 2026','Monday',23275),('Apr 2026','Saturday',14836),
 ('Apr 2026','Sunday',19733),('Apr 2026','Thursday',27197),('Apr 2026','Tuesday',21848),
 ('Apr 2026','Wednesday',28585),
 ('May 2026','Friday',29301),('May 2026','Monday',25199),('May 2026','Saturday',25008),
 ('May 2026','Sunday',28859),('May 2026','Thursday',25307),('May 2026','Tuesday',27662),
 ('May 2026','Wednesday',28297),
 ('Jun 2026','Friday',28705),('Jun 2026','Monday',38189),('Jun 2026','Saturday',23995),
 ('Jun 2026','Sunday',29525),('Jun 2026','Thursday',30162),('Jun 2026','Tuesday',38166),
 ('Jun 2026','Wednesday',33046),
 ('Jul 2026','Friday',8360),('Jul 2026','Monday',10442),('Jul 2026','Saturday',7191),
 ('Jul 2026','Sunday',9830),('Jul 2026','Thursday',11386),('Jul 2026','Tuesday',9392),
 ('Jul 2026','Wednesday',15805),
]
MONTH_ORDER = ['Apr 2026','May 2026','Jun 2026','Jul 2026']

def agg_site(raw):
    dow, month = {}, {}
    for m,day,v in raw:
        dow[day]=dow.get(day,0)+v
        month[m]=month.get(m,0)+v
    avg=sum(dow.values())/len(dow)
    block={
        'by_dow':   [{'day':d,'pv':dow[d],'index':round(100*dow[d]/avg,1)} for d in DOW_ORDER],
        'by_month': [{'month':m,'pv':month[m]} for m in MONTH_ORDER],
        'matrix':   [{'month':m,'day':day,'pv':v} for (m,day,v) in raw],
        'total':    sum(dow.values()),
    }
    return dow, block

SITE_ALL_DOW, SITE_ALL_BLOCK = agg_site(SITE_ALL_RAW)
SITE_NO4_DOW, SITE_NO4_BLOCK = agg_site(SITE_NO4_RAW)

# ---- Site PV by hour-of-day (IST), excl 4 leaders & offline cohort ----
SITE_HOUR_NO4_RAW = [
 ('Apr 2026',0,3899),('Apr 2026',1,3058),('Apr 2026',2,1617),('Apr 2026',3,989),('Apr 2026',4,921),
 ('Apr 2026',5,1204),('Apr 2026',6,2167),('Apr 2026',7,4453),('Apr 2026',8,6217),('Apr 2026',9,7233),
 ('Apr 2026',10,8261),('Apr 2026',11,9747),('Apr 2026',12,9636),('Apr 2026',13,9615),('Apr 2026',14,9941),
 ('Apr 2026',15,9908),('Apr 2026',16,9889),('Apr 2026',17,8641),('Apr 2026',18,8444),('Apr 2026',19,8479),
 ('Apr 2026',20,9298),('Apr 2026',21,10059),('Apr 2026',22,11134),('Apr 2026',23,8648),
 ('May 2026',0,5588),('May 2026',1,2884),('May 2026',2,1698),('May 2026',3,1166),('May 2026',4,1146),
 ('May 2026',5,1863),('May 2026',6,3102),('May 2026',7,4967),('May 2026',8,7193),('May 2026',9,9752),
 ('May 2026',10,10370),('May 2026',11,11513),('May 2026',12,11240),('May 2026',13,11522),('May 2026',14,11364),
 ('May 2026',15,11048),('May 2026',16,10586),('May 2026',17,9059),('May 2026',18,8140),('May 2026',19,7992),
 ('May 2026',20,9400),('May 2026',21,14138),('May 2026',22,17531),('May 2026',23,13913),
 ('Jun 2026',0,6635),('Jun 2026',1,4283),('Jun 2026',2,2375),('Jun 2026',3,1465),('Jun 2026',4,1502),
 ('Jun 2026',5,2512),('Jun 2026',6,4199),('Jun 2026',7,7659),('Jun 2026',8,10897),('Jun 2026',9,11159),
 ('Jun 2026',10,11554),('Jun 2026',11,12344),('Jun 2026',12,13895),('Jun 2026',13,14516),('Jun 2026',14,13908),
 ('Jun 2026',15,13480),('Jun 2026',16,11524),('Jun 2026',17,9753),('Jun 2026',18,8588),('Jun 2026',19,8742),
 ('Jun 2026',20,11385),('Jun 2026',21,14855),('Jun 2026',22,18222),('Jun 2026',23,14288),
 ('Jul 2026',0,2495),('Jul 2026',1,1407),('Jul 2026',2,810),('Jul 2026',3,512),('Jul 2026',4,529),
 ('Jul 2026',5,766),('Jul 2026',6,1294),('Jul 2026',7,2193),('Jul 2026',8,3208),('Jul 2026',9,3910),
 ('Jul 2026',10,3937),('Jul 2026',11,4295),('Jul 2026',12,4397),('Jul 2026',13,4391),('Jul 2026',14,4593),
 ('Jul 2026',15,4200),('Jul 2026',16,3580),('Jul 2026',17,3468),('Jul 2026',18,3348),('Jul 2026',19,3286),
 ('Jul 2026',20,3530),('Jul 2026',21,4790),('Jul 2026',22,6277),('Jul 2026',23,4519),
]
def hour_bucket(h):
    if h < 9:  return '1 Early AM (<9)'
    if h < 12: return '2 Late Morning (9-12)'
    if h < 15: return '3 Afternoon (12-15)'
    if h < 18: return '4 Late Afternoon (15-18)'
    if h < 21: return '5 Evening (18-21)'
    return '6 Night (21+)'
TIME_ORDER = ['1 Early AM (<9)','2 Late Morning (9-12)','3 Afternoon (12-15)',
              '4 Late Afternoon (15-18)','5 Evening (18-21)','6 Night (21+)']
def agg_site_hour(raw):
    hour, bucket = {}, {}
    for m,h,v in raw:
        hour[h] = hour.get(h,0)+v
        bucket[hour_bucket(h)] = bucket.get(hour_bucket(h),0)+v
    avg = sum(bucket.values())/len(bucket)
    block = {
        'by_hour':   [{'hour':h,'pv':hour.get(h,0)} for h in range(24)],
        'by_bucket': [{'key':b,'pv':bucket[b],'index':round(100*bucket[b]/avg,1)} for b in TIME_ORDER],
        'total':     sum(hour.values()),
    }
    return bucket, block
SITE_NO4_TBUCKET, SITE_NO4_TIME_BLOCK = agg_site_hour(SITE_HOUR_NO4_RAW)

# ---- Site PV by hour-of-day (IST), OVERALL cohort (all leaders & types) ----
SITE_HOUR_ALL_RAW = [
 ('Apr 2026',0,5924),('Apr 2026',1,4375),('Apr 2026',2,2480),('Apr 2026',3,1480),('Apr 2026',4,1331),
 ('Apr 2026',5,1781),('Apr 2026',6,3303),('Apr 2026',7,6796),('Apr 2026',8,9438),('Apr 2026',9,10751),
 ('Apr 2026',10,11953),('Apr 2026',11,13940),('Apr 2026',12,13994),('Apr 2026',13,13524),('Apr 2026',14,14098),
 ('Apr 2026',15,14537),('Apr 2026',16,14577),('Apr 2026',17,12896),('Apr 2026',18,12172),('Apr 2026',19,11992),
 ('Apr 2026',20,12922),('Apr 2026',21,13865),('Apr 2026',22,15358),('Apr 2026',23,12140),
 ('May 2026',0,10336),('May 2026',1,5592),('May 2026',2,3120),('May 2026',3,1953),('May 2026',4,1766),
 ('May 2026',5,2566),('May 2026',6,4354),('May 2026',7,7098),('May 2026',8,10710),('May 2026',9,14420),
 ('May 2026',10,15680),('May 2026',11,16971),('May 2026',12,17431),('May 2026',13,17125),('May 2026',14,17411),
 ('May 2026',15,17374),('May 2026',16,17297),('May 2026',17,14662),('May 2026',18,13202),('May 2026',19,12897),
 ('May 2026',20,14665),('May 2026',21,20155),('May 2026',22,24559),('May 2026',23,20781),
 ('Jun 2026',0,12052),('Jun 2026',1,7620),('Jun 2026',2,4165),('Jun 2026',3,2510),('Jun 2026',4,2431),
 ('Jun 2026',5,3727),('Jun 2026',6,6642),('Jun 2026',7,11864),('Jun 2026',8,16973),('Jun 2026',9,17937),
 ('Jun 2026',10,19233),('Jun 2026',11,19832),('Jun 2026',12,21729),('Jun 2026',13,22559),('Jun 2026',14,21857),
 ('Jun 2026',15,21352),('Jun 2026',16,20090),('Jun 2026',17,17149),('Jun 2026',18,15464),('Jun 2026',19,15851),
 ('Jun 2026',20,18675),('Jun 2026',21,22410),('Jun 2026',22,26994),('Jun 2026',23,22457),
 ('Jul 2026',0,5200),('Jul 2026',1,2929),('Jul 2026',2,1739),('Jul 2026',3,1081),('Jul 2026',4,1061),
 ('Jul 2026',5,1481),('Jul 2026',6,2644),('Jul 2026',7,4663),('Jul 2026',8,5798),('Jul 2026',9,6424),
 ('Jul 2026',10,6534),('Jul 2026',11,7176),('Jul 2026',12,7412),('Jul 2026',13,7335),('Jul 2026',14,7863),
 ('Jul 2026',15,6967),('Jul 2026',16,6420),('Jul 2026',17,5984),('Jul 2026',18,5655),('Jul 2026',19,6219),
 ('Jul 2026',20,6381),('Jul 2026',21,8121),('Jul 2026',22,11268),('Jul 2026',23,8132),
]
SITE_ALL_TBUCKET, SITE_ALL_TIME_BLOCK = agg_site_hour(SITE_HOUR_ALL_RAW)

def session_list(sub):
    top = sub.sort_values('PV', ascending=False).head(5)
    return [{
        'name':str(r['disp_name']),'leader':str(r['leader_name']),
        'PV':int(r['PV']),'cart':float(r['RC_rate']),'sale':float(r['RS_rate']),
        'price':int(r['price']),'type':str(r['type']),
        'date':str(r['startIST'])[:16] if pd.notna(r.get('startIST')) else ''
    } for _,r in top.iterrows()]

def build(df, single_kw=False, site_dow=None, site_block=None, site_scope='all',
          site_tbucket=None, site_time_block=None):
    # PV universe = sessions from 1 Apr onward; keyword universe = ALL dates
    pv = df[df['startIST'] >= CUTOFF].copy()

    def pooled_rows(frame, col, order=None):
        out=[]
        for k, sub in frame.groupby(col):
            s=sub['PV'].sum()
            out.append({'key':str(k),'n':int(len(sub)),'PV_total':int(s),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/s) if s else None,
                        'sale':float(100*sub['sales'].sum()/s) if s else None})
        if order:
            out = sorted(out, key=lambda r: order.index(r['key']) if r['key'] in order else 999)
        return out

    d = {}
    d['overall'] = {
        'sessions': int(len(pv)), 'sessions_all': int(len(df)),
        'PV_total': int(pv['PV'].sum()),
        'cart': float(100*pv['carts'].sum()/pv['PV'].sum()) if pv['PV'].sum() else 0,
        'sale': float(100*pv['sales'].sum()/pv['PV'].sum()) if pv['PV'].sum() else 0,
        'PV_median': float(pv['PV'].median()),
        'carts_total': int(pv['carts'].sum()), 'sales_total': int(pv['sales'].sum()),
    }
    d['type'] = pooled_rows(pv, 'type')
    d['price_tier'] = pooled_rows(pv, 'price_tier', ['0 Free','1-300','301-600','601-1000','1001-1500','1500+'])
    d['dow'] = pooled_rows(pv, 'dow_name', DOW_ORDER)
    d['time'] = pooled_rows(pv, 'time_bucket', ['1 Early AM (<9)','2 Late Morning (9-12)','3 Afternoon (12-15)','4 Late Afternoon (15-18)','5 Evening (18-21)','6 Night (21+)'])

    # Normalize session demand by site traffic on each day-of-week (both Apr+ windows)
    norms=[]
    for r in d['dow']:
        sp = (site_dow or {}).get(r['key'])
        r['site_pv'] = sp
        r['pv_per_1k_site'] = round(1000.0*r['PV_total']/sp, 2) if sp else None
        if r['pv_per_1k_site'] is not None: norms.append(r['pv_per_1k_site'])
    navg = sum(norms)/len(norms) if norms else None
    for r in d['dow']:
        r['demand_index'] = round(100*r['pv_per_1k_site']/navg,1) if (navg and r['pv_per_1k_site'] is not None) else None
    d['site_pv'] = site_block
    d['site_scope'] = site_scope

    # Normalize session demand by site traffic in each time-of-day bucket (when available)
    if site_tbucket:
        tnorms=[]
        for r in d['time']:
            sp = site_tbucket.get(r['key'])
            r['site_pv'] = sp
            r['pv_per_1k_site'] = round(1000.0*r['PV_total']/sp, 2) if sp else None
            if r['pv_per_1k_site'] is not None: tnorms.append(r['pv_per_1k_site'])
        tavg = sum(tnorms)/len(tnorms) if tnorms else None
        for r in d['time']:
            r['demand_index'] = round(100*r['pv_per_1k_site']/tavg,1) if (tavg and r['pv_per_1k_site'] is not None) else None
    d['site_time'] = site_time_block

    dd = pv.copy()
    dd['wordq'] = pd.qcut(dd['name_len_words'], 4, duplicates='drop')
    wq=[]
    for k,sub in dd.groupby('wordq', observed=True):
        s=sub['PV'].sum()
        wq.append({'key':str(k),'n':int(len(sub)),'PV_total':int(s),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/s) if s else 0,'sale':float(100*sub['sales'].sum()/s) if s else 0})
    d['wordq']=wq

    # ---- Keywords: ALL dates (full df), per user instruction ----
    kws=[]; kw_sessions={}
    if single_kw:
        for key, sub in df.groupby('main_keyword'):
            if len(sub) < 3: continue
            s=sub['PV'].sum()
            kws.append({'key':str(key),'n':int(len(sub)),'PV_total':int(s),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/s) if s else 0,
                        'sale':float(100*sub['sales'].sum()/s) if s else 0})
            kw_sessions[str(key)]=session_list(sub)
    else:
        for c in [c for c in df.columns if c.startswith('kw_')]:
            sub=df[df[c]==1]
            if len(sub)<15: continue
            key=c[3:].replace('_',' ')
            s=sub['PV'].sum()
            kws.append({'key':key,'n':int(len(sub)),'PV_total':int(s),
                        'PV_median':float(sub['PV'].median()),
                        'cart':float(100*sub['carts'].sum()/s) if s else 0,
                        'sale':float(100*sub['sales'].sum()/s) if s else 0})
            kw_sessions[key]=session_list(sub)
    d['keywords']=sorted(kws,key=lambda r:-r['PV_total'])
    d['keyword_sessions']=kw_sessions
    d['kw_mode']='single' if single_kw else 'multi'

    # Second table: user's multi-tag keyword list (all dates, this cohort)
    kt, ks = kw2_block(df, session_list)
    d['kwtable']=kt
    d['kwtable_sessions']=ks

    lt=[]
    for k,sub in pv.groupby('leader_name'):
        if len(sub)<3: continue
        s=sub['PV'].sum()
        lt.append({'key':str(k),'n':int(len(sub)),'PV_total':int(s),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/s) if s else 0,
                   'sale':float(100*sub['sales'].sum()/s) if s else 0})
    d['leaders']=sorted(lt,key=lambda r:-r['PV_total'])

    mt=[]
    for k,sub in pv.groupby('month'):
        if len(sub)<3: continue
        s=sub['PV'].sum()
        mt.append({'key':str(k),'n':int(len(sub)),'PV_total':int(s),'PV_median':float(sub['PV'].median()),
                   'cart':float(100*sub['carts'].sum()/s) if s else 0,
                   'sale':float(100*sub['sales'].sum()/s) if s else 0})
    d['monthly']=sorted(mt,key=lambda r:r['key'])
    return d

def mom_block(dfc, site_dow_raw, site_hour_raw):
    """Month-on-month: platform PV + session funnel (PV/carts/sales) by month x DOW and x hour."""
    pv = dfc[dfc['startIST'] >= CUTOFF].copy()
    pv['mlabel'] = pv['startIST'].dt.strftime('%b %Y')
    sdow, shour = {}, {}
    for (m,day),sub in pv.groupby(['mlabel','dow_name']):
        sdow[(m,day)] = (sub['PV'].sum(), sub['carts'].sum(), sub['sales'].sum())
    for (m,h),sub in pv.groupby(['mlabel','hour']):
        shour[(m,int(h))] = (sub['PV'].sum(), sub['carts'].sum(), sub['sales'].sum())
    plat_dow  = {(m,d):v for m,d,v in site_dow_raw}
    plat_hour = {(m,h):v for m,h,v in site_hour_raw}
    dow_rows=[]
    for m in MONTH_ORDER:
        for d in DOW_ORDER:
            s=sdow.get((m,d),(0,0,0))
            dow_rows.append({'month':m,'day':d,'platform_pv':int(plat_dow.get((m,d),0)),
                             'session_pv':int(s[0]),'carts':int(round(s[1])),'sales':int(round(s[2]))})
    hour_rows=[]
    for m in MONTH_ORDER:
        for h in range(24):
            s=shour.get((m,h),(0,0,0))
            hour_rows.append({'month':m,'hour':h,'platform_pv':int(plat_hour.get((m,h),0)),
                              'session_pv':int(s[0]),'carts':int(round(s[1])),'sales':int(round(s[2]))})
    return {'dow':dow_rows,'hour':hour_rows}

# ---- Per-leader deep-dive (top 4 leaders, online only, last ~6 months) ----
LEAD_ORDER = ['Kavyal Sedanni','Dr. Tamanna C','Dr. Rashmi N Muthalkar','Munisha Khatwani']
LEAD_CUTOFF = pd.Timestamp('2026-01-01')  # ~6 months of active/upcoming sessions
TIME_ORDER = ['1 Early AM (<9)','2 Late Morning (9-12)','3 Afternoon (12-15)',
              '4 Late Afternoon (15-18)','5 Evening (18-21)','6 Night (21+)']
PRICE_ORDER = ['0 Free','1-300','301-600','601-1000','1001-1500','1500+']

def _brk(sub, col, order=None):
    out=[]
    for k,g in sub.groupby(col):
        pv=g['PV'].sum()
        out.append({'key':str(k),'n':int(len(g)),'PV_total':int(pv),
                    'cart':float(100*g['carts'].sum()/pv) if pv else 0,
                    'sale':float(100*g['sales'].sum()/pv) if pv else 0})
    if order: out=sorted(out,key=lambda r: order.index(r['key']) if r['key'] in order else 999)
    else: out=sorted(out,key=lambda r:-r['PV_total'])
    return out

def leader_detail(sub):
    pv=sub['PV'].sum()
    d={'overall':{'n':int(len(sub)),'PV_total':int(pv),
        'cart':float(100*sub['carts'].sum()/pv) if pv else 0,
        'sale':float(100*sub['sales'].sum()/pv) if pv else 0,
        'PV_median':float(sub['PV'].median()) if len(sub) else 0}}
    d['theme']=_brk(sub,'main_keyword')
    d['dow']=_brk(sub,'dow_name',DOW_ORDER)
    d['time']=_brk(sub,'time_bucket',TIME_ORDER)
    d['price']=_brk(sub,'price_tier',PRICE_ORDER)
    d['sessions']=[{'name':str(r['disp_name']),'theme':str(r['main_keyword']),'dow':str(r['dow_name']),
                    'time':str(r['time_bucket']),'price':int(r['price']),'PV':int(r['PV']),
                    'cart':float(r['RC_rate']),'sale':float(r['RS_rate']),'date':str(r['startIST'])[:16]}
                   for _,r in sub.sort_values('PV',ascending=False).iterrows()]
    kt, ks = kw2_block(sub, session_list)
    d['kwtable']=kt
    d['kwtable_sessions']=ks
    return d

df = pd.read_csv('merged_analysis.csv')
df['startIST'] = pd.to_datetime(df['startIST'], errors='coerce')
no4 = df[~df['leader_name'].isin(EXCLUDE)].copy()
online_no4 = no4[no4['type'] != 'OFFLINE'].copy()
out = {
    # Both tabs use the single main-keyword format; they differ only in cohort.
    'all': build(df, single_kw=True, site_dow=SITE_ALL_DOW, site_block=SITE_ALL_BLOCK, site_scope='all',
                 site_tbucket=SITE_ALL_TBUCKET, site_time_block=SITE_ALL_TIME_BLOCK),
    'online_single': build(online_no4, single_kw=True, site_dow=SITE_NO4_DOW, site_block=SITE_NO4_BLOCK, site_scope='no4',
                      site_tbucket=SITE_NO4_TBUCKET, site_time_block=SITE_NO4_TIME_BLOCK),
    'excluded_leaders': EXCLUDE,
    'cutoff': '2026-04-01',
    'mom': {
        'all': mom_block(df, SITE_ALL_RAW, SITE_HOUR_ALL_RAW),
        'no4': mom_block(online_no4, SITE_NO4_RAW, SITE_HOUR_NO4_RAW),
    },
    'leaders_detail': {
        L: leader_detail(df[(df['leader_name']==L) & (df['type']!='OFFLINE') & (df['startIST']>=LEAD_CUTOFF)].copy())
        for L in LEAD_ORDER
    },
}
with open('dashboard_data.json','w') as f:
    json.dump(out,f,indent=1)
print('wrote dashboard_data.json (PV sections from 1 Apr; keywords all-dates)')
for k in ['all','online_single']:
    o=out[k]['overall']
    print(f"{k:14s}: PV-sessions={o['sessions']:4d} (all={o['sessions_all']:4d})  PV={o['PV_total']:>7d}  cart={o['cart']:.2f}%  sale={o['sale']:.2f}%  site={out[k]['site_scope']}")
print('SITE_ALL DOW index:', {r['day'][:3]:r['index'] for r in SITE_ALL_BLOCK['by_dow']})
print('SITE_NO4 DOW index:', {r['day'][:3]:r['index'] for r in SITE_NO4_BLOCK['by_dow']})
print('online_single demand_index by DOW:', {r['key'][:3]:r['demand_index'] for r in out['online_single']['dow']})
