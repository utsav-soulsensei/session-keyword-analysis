import pandas as pd, numpy as np
from scipy import stats
pd.set_option('display.width', 160, 'display.max_columns', 30)

df = pd.read_csv('merged_analysis.csv')

def pooled(g):
    """Volume-weighted funnel for a group: cart% = sum(carts)/sum(PV), sale% = sum(sales)/sum(PV)."""
    pv = g['PV'].sum()
    carts = g['carts'].sum()
    sales = g['sales'].sum()
    return pd.Series({
        'n': len(g),
        'PV_total': pv,
        'PV_median': g['PV'].median(),
        'PV_mean': g['PV'].mean(),
        'cart%_pooled': 100*carts/pv if pv else np.nan,
        'sale%_pooled': 100*sales/pv if pv else np.nan,
        'cart_per_1k_PV': 1000*carts/pv if pv else np.nan,
        'sale_per_1k_PV': 1000*sales/pv if pv else np.nan,
    })

def show(title, col, order=None, minn=1):
    print('\n' + '='*90)
    print(title)
    print('='*90)
    t = df.groupby(col).apply(pooled, include_groups=False)
    if order: t = t.reindex(order)
    t = t[t['n'] >= minn]
    print(t.round(2).to_string())
    return t

print('OVERALL FUNNEL')
print('  Sessions:', len(df))
print('  Total PV (demand):', int(df['PV'].sum()))
print('  Pooled cart%% (PV->RC): %.2f%%' % (100*df['carts'].sum()/df['PV'].sum()))
print('  Pooled sale%% (PV->RS): %.2f%%' % (100*df['sales'].sum()/df['PV'].sum()))
print('  Median PV per session:', df['PV'].median())

# 1. TYPE
show('1. TYPE (online STANDARD vs OFFLINE)', 'type')

# 2. PRICE tiers
show('2. PRICE TIER', 'price_tier',
     order=['0 Free','1-300','301-600','601-1000','1001-1500','1500+'])

# price correlation (paid only, log PV)
paid = df[df['price']>0].copy()
paid['logPV'] = np.log1p(paid['PV'])
r_pv,p_pv = stats.spearmanr(paid['price'], paid['PV'])
r_rc,p_rc = stats.spearmanr(paid['price'], paid['RC_rate'])
r_rs,p_rs = stats.spearmanr(paid['price'], paid['RS_rate'])
print('\nPrice Spearman corr (paid n=%d): PV r=%.3f p=%.1e | cart%% r=%.3f p=%.1e | sale%% r=%.3f p=%.1e'
      % (len(paid), r_pv,p_pv, r_rc,p_rc, r_rs,p_rs))
# free vs paid demand
fe = df[df['is_free']]['PV']; pa = df[~df['is_free']]['PV']
print('Free median PV %.0f (n=%d) vs Paid median PV %.0f (n=%d)' % (fe.median(),len(fe),pa.median(),len(pa)))

# 3. DAY OF WEEK
show('3. DAY OF WEEK', 'dow_name',
     order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
show('   WEEKEND vs WEEKDAY', 'is_weekend')

# 4. TIME OF DAY
show('4. TIME OF DAY', 'time_bucket')

# 5. NAME
print('\n' + '='*90); print('5. NAME LENGTH (word-count quartiles)'); print('='*90)
df['wordq'] = pd.qcut(df['name_len_words'], 4, duplicates='drop')
print(df.groupby('wordq', observed=True).apply(pooled, include_groups=False).round(2).to_string())

print('\n--- KEYWORD IMPACT (pooled cart%/sale% when keyword present, sorted by PV_total) ---')
kw_cols = [c for c in df.columns if c.startswith('kw_')]
rows=[]
totPV = df['PV'].sum()
for c in kw_cols:
    sub = df[df[c]==1]
    if len(sub) < 15: continue
    pv=sub['PV'].sum()
    rows.append({'keyword':c[3:], 'n':len(sub), 'PV_total':int(pv),
                 'PV_median':sub['PV'].median(),
                 'cart%':100*sub['carts'].sum()/pv if pv else 0,
                 'sale%':100*sub['sales'].sum()/pv if pv else 0})
kwt = pd.DataFrame(rows).sort_values('PV_total', ascending=False)
print(kwt.round(2).to_string(index=False))

# 6. LEADER (top by demand, min 3 sessions)
print('\n' + '='*90); print('6. TOP 20 LEADERS by total PV (min 3 sessions)'); print('='*90)
lt = df.groupby('leader_name').apply(pooled, include_groups=False)
lt = lt[lt['n']>=3].sort_values('PV_total', ascending=False).head(20)
print(lt.round(2).to_string())
print('\nLeader count:', df['leader_name'].nunique(), '| sessions/leader median:', df.groupby('leader_name').size().median())

# 7. Driver ranking via regression on log(PV) and on rates
print('\n' + '='*90); print('7. MULTIVARIATE DRIVER RANKING'); print('='*90)
import numpy as np
reg = df.copy()
reg['logPV'] = np.log1p(reg['PV'])
reg['is_offline'] = (reg['type']=='OFFLINE').astype(int)
X_num = reg[['price','is_offline','is_weekend','hour','name_len_words','is_free']].astype(float)
X_num['is_weekend']=X_num['is_weekend'].astype(float)
for target in ['logPV','RC_rate','RS_rate']:
    y = reg[target]
    # standardized simple correlations
    print('\nTarget = %s  (Spearman |r| ranked):' % target)
    cors=[]
    for c in X_num.columns:
        r,p = stats.spearmanr(X_num[c], y, nan_policy='omit')
        cors.append((c,r,p))
    for c,r,p in sorted(cors,key=lambda t:-abs(t[1])):
        sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else ''
        print('   %-16s r=%+.3f p=%.1e %s' % (c,r,p,sig))

# save summary tables for dashboard
import json
summary = {
 'overall': {'sessions':len(df),'PV_total':int(df['PV'].sum()),
             'cart_pooled':100*df['carts'].sum()/df['PV'].sum(),
             'sale_pooled':100*df['sales'].sum()/df['PV'].sum(),
             'PV_median':float(df['PV'].median())},
}
with open('summary.json','w') as f: json.dump(summary,f)
print('\nDone.')
