import pandas as pd
import numpy as np
import re

# ---------- Load ----------
s1 = pd.read_csv('Raw Data - Course - Sheet1.csv')
s2 = pd.read_csv('Raw Data - Course - Sheet2.csv')

# Normalize join keys
def to_int(x):
    if pd.isna(x): return np.nan
    return int(float(str(x).replace(',', '').strip()))

s1['id'] = s1['course_instance_new'].apply(to_int)
s2['id'] = s2['id'].apply(to_int)

# Clean numeric funnel fields
s1['PV'] = pd.to_numeric(s1['A. PV'].astype(str).str.replace(',', '', regex=False), errors='coerce')
s1['RC_rate'] = s1['B. PV to RC'].astype(str).str.replace('%', '', regex=False)
s1['RC_rate'] = pd.to_numeric(s1['RC_rate'], errors='coerce')  # percent already (0-100)
s1['RS_rate'] = s1['C. PV to RS'].astype(str).str.replace('%', '', regex=False)
s1['RS_rate'] = pd.to_numeric(s1['RS_rate'], errors='coerce')

# Clean course info
s2['price'] = pd.to_numeric(s2['price'].astype(str).str.replace(',', '', regex=False), errors='coerce')
s2['startDate'] = pd.to_datetime(s2['startDate'], errors='coerce')
s2['type'] = s2['type'].str.strip()

# ---------- Merge ----------
df = s1.merge(s2[['id', 'startDate', 'type', 'price', 'shortName']], on='id', how='inner')
print('Merged rows:', len(df))

# ---------- Derived funnel counts ----------
# RC_rate / RS_rate are % of PV. Estimate absolute carts & sales.
df['carts'] = df['PV'] * df['RC_rate'] / 100.0
df['sales'] = df['PV'] * df['RS_rate'] / 100.0

# ---------- Feature engineering ----------
# Timestamps are UTC; audience is India. Convert to IST (+5:30) for real local time.
df['startIST'] = df['startDate'] + pd.Timedelta(hours=5, minutes=30)
df['dow'] = df['startIST'].dt.dayofweek          # 0=Mon
df['dow_name'] = df['startIST'].dt.day_name()
df['hour'] = df['startIST'].dt.hour
df['month'] = df['startIST'].dt.to_period('M').astype(str)
df['is_weekend'] = df['dow'].isin([5, 6])

# Times in the raw file: many are 05:30, 14:30 etc. Bucket by hour.
def tod(h):
    if pd.isna(h): return 'Unknown'
    h = int(h)
    if h < 9:   return '1 Early AM (<9)'
    if h < 12:  return '2 Late Morning (9-12)'
    if h < 15:  return '3 Afternoon (12-15)'
    if h < 18:  return '4 Late Afternoon (15-18)'
    if h < 21:  return '5 Evening (18-21)'
    return '6 Night (21+)'
df['time_bucket'] = df['hour'].apply(tod)

# Price tiers
df['is_free'] = df['price'] == 0
def price_tier(p):
    if pd.isna(p): return 'Unknown'
    if p == 0: return '0 Free'
    if p <= 300: return '1-300'
    if p <= 600: return '301-600'
    if p <= 1000: return '601-1000'
    if p <= 1500: return '1001-1500'
    return '1500+'
df['price_tier'] = df['price'].apply(price_tier)

# Name features
name = df['course_name'].fillna('').str.replace('\n', ' ', regex=False)
df['name_clean'] = name.str.strip()
df['name_len_chars'] = df['name_clean'].str.len()
df['name_len_words'] = df['name_clean'].str.split().apply(len)
df['name_has_colon'] = df['name_clean'].str.contains(':')
df['name_has_amp'] = df['name_clean'].str.contains('&')

# Theme keywords (wellness/manifestation vocabulary seen in the data)
KEYWORDS = ['manifest','heal','healing','money','wealth','abundance','love','relationship',
            'stress','anxiety','sleep','dream','moon','chakra','energy','yoga','meditat',
            'confidence','fear','block','release','reiki','tarot','astro','numerolog',
            'workshop','masterclass','joyshop','free','glow','weight','posture','gut',
            'karma','soul','angel','manifestation','breath','inner child','ancestral']
low = df['name_clean'].str.lower()
for kw in KEYWORDS:
    col = 'kw_' + re.sub(r'[^a-z]', '_', kw)
    df[col] = low.str.contains(re.escape(kw)).astype(int)

df['leader_name'] = df['leader_name'].fillna('Unknown').str.strip()

# Display name = shortName (marketing title), falling back to the full course
# name only when shortName is missing/"[NULL]".
_sn = df['shortName'].astype(str).str.replace('\n', ' ', regex=False).str.strip()
_bad = _sn.str.upper().isin(['[NULL]', 'NAN', ''])
df['disp_name'] = _sn.where(~_bad, df['name_clean'])

# ---------- Single "main keyword" per session (mutually exclusive, short titles) ----------
# Priority-ordered: the FIRST theme whose pattern matches the name wins, so each
# session is counted under exactly one theme. Distinctive modalities rank above
# broad life-goals, which rank above generic words like "heal"/"energy".
KW_PRIORITY = [
    ('Tarot',               ['tarot']),
    ('Angel',               ['angel']),
    ('Reiki',               ['reiki']),
    ('Chakra',              ['chakra']),
    ('Numerology',          ['numerolog']),
    ('Astrology',           ['astro', 'zodiac', 'horoscope', 'nakshatra']),
    ('Moon',                ['moon']),
    ('Protection & Evil Eye',['nazar', 'evil eye', 'cord cut', 'cord-cut', 'cutting cord', 'protection', 'psychic attack', 'shield', 'black magic']),
    ('Psychic & Activation',['psychic', 'intuition', 'third eye', 'clairvoy', 'sixth sense', 'activation', 'activate', 'awaken', 'abilities', 'telepath']),
    ('Devotional & Deity',  ['sadhana', 'naamjap', 'namjap', 'hanuman', 'gita', 'ganesh', 'durga', 'lakshmi', 'shiv', 'krishna', 'kali', 'sai', 'buddha', 'puja', 'pooja', 'vidhi', 'bhajan', 'kirtan', 'chant', 'mantra', 'prayer', 'navratri', 'shani']),
    ('Ancestral',           ['ancestral', 'lineage']),
    ('Inner Child',         ['inner child', 'inner-child']),
    ('Karma & Past Life',   ['karma', 'past life', 'past-life']),
    ('Dreams',              ['dream']),
    ('Wealth & Money',      ['wealth', 'money', 'abundance', 'prosper', 'financ', 'rich']),
    ('Love & Relationships',['love', 'relationship', 'partner', 'marriage', 'soulmate', 'breakup', 'divorce', 'romance']),
    ('Manifestation',       ['manifest']),
    ('Yoga',                ['yoga']),
    ('Meditation',          ['meditat', 'mindful']),
    ('Breathwork',          ['breath', 'pranayam']),
    ('Sleep',               ['sleep', 'insomnia']),
    ('Stress & Anxiety',    ['stress', 'anxiet', 'overthink', 'worry', 'calm', 'peace', 'emotional', 'emotion']),
    ('Confidence & Self-Worth', ['confidence', 'self-worth', 'self worth', 'self-love', 'self esteem', 'self-esteem', 'self worth']),
    ('Fear',                ['fear', 'phobia']),
    ('Body & Health',       ['gut', 'weight', 'posture', 'pain', 'hormone', 'fitness', 'detox', 'skin', 'hair', 'body', 'lymph', 'thyroid', 'pcos', 'pcod', 'face']),
    ('Clarity & Mind',      ['clarity', 'focus', 'mental', 'conscious', 'awareness', 'voice', 'decision', 'mind']),
    ('Energy & Aura',       ['energy', 'aura', 'vibration', 'frequency']),
    ('Release & Blocks',    ['release', 'block', 'let go', 'letting go', 'clear', 'break free', 'pattern']),
    ('Healing',             ['heal']),
    ('Soul & Spirit',       ['soul', 'spirit', 'divine', 'god', 'dharma', 'purpose', 'awaken', 'transform', 'journey']),
    ('Vision & Goals',      ['vision', 'goal', 'success', 'power']),
]
def main_kw(name):
    n = str(name).lower()
    for title, pats in KW_PRIORITY:
        for p in pats:
            if p in n:
                return title
    return 'Other'
df['main_keyword'] = df['name_clean'].apply(main_kw)

# Save
df.to_csv('merged_analysis.csv', index=False)
print('Saved merged_analysis.csv')
print(df[['id','PV','RC_rate','RS_rate','price','type','dow_name','hour','time_bucket','price_tier']].head())
print('\nPV describe:\n', df['PV'].describe())
print('\nRC_rate describe:\n', df['RC_rate'].describe())
print('\nRS_rate describe:\n', df['RS_rate'].describe())
print('\nMissing startDate:', df['startDate'].isna().sum())
print('Missing price:', df['price'].isna().sum())
