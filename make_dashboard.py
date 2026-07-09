import json
data = json.load(open('dashboard_data.json'))
DATA_JS = json.dumps(data)

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Session Demand Analytics</title>
<style>
:root{
  --surface-1:#fcfcfb; --page:#f9f9f7;
  --text-primary:#0b0b0b; --text-secondary:#52514e; --muted:#898781;
  --grid:#e1e0d9; --baseline:#c3c2b7; --border:rgba(11,11,11,0.10);
  --s1:#2a78d6; --s2:#1baf7a; --s3:#eb6834; --s4:#4a3aa7; --good:#0ca30c; --warn:#fab219;
}
@media (prefers-color-scheme: dark){
  :root{
    --surface-1:#1a1a19; --page:#0d0d0d;
    --text-primary:#fff; --text-secondary:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,0.10);
    --s1:#3987e5; --s2:#199e70; --s3:#d95926; --s4:#9085e9; --good:#0ca30c;
  }
}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--text-primary);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.5;}
.wrap{max-width:1120px;margin:0 auto;padding:32px 24px 80px;}
header h1{font-size:26px;margin:0 0 4px;letter-spacing:-0.02em;}
header p{color:var(--text-secondary);margin:0 0 4px;font-size:14px;}
.note{font-size:12px;color:var(--muted);margin-top:8px;max-width:820px;}
.tabs{display:flex;gap:6px;margin:22px 0 4px;border-bottom:1px solid var(--border);}
.tab{appearance:none;border:none;background:none;cursor:pointer;font:inherit;
  padding:10px 16px;font-size:13.5px;font-weight:600;color:var(--muted);
  border-bottom:2px solid transparent;margin-bottom:-1px;}
.tab.on{color:var(--text-primary);border-bottom-color:var(--s1);}
.tab .c{font-weight:400;font-size:11px;color:var(--muted);display:block;margin-top:1px;}
.momctrl{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin:16px 0 4px;}
.momctrl .grp{display:flex;align-items:center;gap:7px;}
.momctrl .lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:0.03em;}
.pillrow{display:inline-flex;gap:3px;background:var(--surface-1);border:1px solid var(--border);border-radius:9px;padding:3px;}
.pill{border:none;background:none;font:inherit;font-size:12.5px;padding:6px 12px;border-radius:6px;cursor:pointer;color:var(--text-secondary);white-space:nowrap;}
.pill.on{background:var(--s1);color:#fff;}
.heatwrap{overflow-x:auto;}
.heat{border-collapse:separate;border-spacing:3px;}
.heat td,.heat th{text-align:center;font-variant-numeric:tabular-nums;}
.heat .rk{font-size:11px;color:var(--text-secondary);text-align:left;white-space:nowrap;padding-right:6px;}
.heat .ch{font-size:10px;color:var(--muted);font-weight:600;}
.banner{font-size:12.5px;color:var(--text-secondary);background:var(--surface-1);
  border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin:12px 0 4px;}
h2{font-size:15px;margin:36px 0 4px;letter-spacing:-0.01em;}
h2 .sub{font-weight:400;color:var(--muted);font-size:12px;margin-left:8px;}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:20px;}
.kpi{background:var(--surface-1);border:1px solid var(--border);border-radius:12px;padding:16px 18px;}
.kpi .v{font-size:28px;font-weight:650;letter-spacing:-0.02em;}
.kpi .l{font-size:12px;color:var(--text-secondary);margin-top:2px;}
.kpi .d{font-size:11px;color:var(--muted);margin-top:6px;}
.kpi .delta{font-size:11px;margin-top:4px;font-variant-numeric:tabular-nums;}
.card{background:var(--surface-1);border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-top:12px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.row{display:flex;align-items:center;gap:10px;margin:7px 0;font-size:13px;}
.row .name{width:182px;flex:0 0 182px;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.row .track{flex:1;display:flex;align-items:center;gap:8px;}
.bar{height:16px;border-radius:0 4px 4px 0;min-width:2px;}
.row .val{font-variant-numeric:tabular-nums;color:var(--text-primary);font-size:12px;}
.legend{display:flex;gap:16px;font-size:12px;color:var(--text-secondary);margin:2px 0 10px;flex-wrap:wrap;}
.legend .sw{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:middle;}
.dual .name{width:172px;flex:0 0 172px;}
table{border-collapse:collapse;width:100%;font-size:12.5px;margin-top:4px;}
th,td{text-align:right;padding:6px 10px;border-bottom:1px solid var(--grid);font-variant-numeric:tabular-nums;}
th:first-child,td:first-child{text-align:left;font-variant-numeric:normal;}
th{color:var(--muted);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.03em;}
.insight{background:var(--surface-1);border:1px solid var(--border);border-left:3px solid var(--s1);
  border-radius:8px;padding:12px 16px;margin:8px 0;font-size:13.5px;}
.insight b{color:var(--text-primary);}
.axis{font-size:10px;color:var(--muted);font-variant-numeric:tabular-nums;}
tr.kwrow{cursor:pointer;}
tr.kwrow:hover td{background:var(--grid);}
tr.kwrow td:first-child::before{content:"▸";display:inline-block;width:14px;color:var(--muted);transition:transform .12s;}
tr.kwrow.open td:first-child::before{transform:rotate(90deg);}
tr.kwrow.open td{font-weight:600;}
.drill{background:var(--page);}
.drill td{padding:0;border-bottom:1px solid var(--grid);}
.drill table{margin:0;}
.drill th{font-size:10px;background:var(--page);}
.drill td{padding:5px 10px;}
.drill .dname{max-width:320px;white-space:normal;color:var(--text-primary);}
.drill .dsub{color:var(--muted);font-size:11px;}
.tbar{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap;}
.tsearch{padding:7px 11px;font:inherit;font-size:13px;border:1px solid var(--border);
  border-radius:8px;background:var(--page);color:var(--text-primary);width:240px;max-width:100%;}
.tsearch::placeholder{color:var(--muted);}
.tcount{font-size:11px;color:var(--muted);}
.thost{max-height:520px;overflow:auto;border-radius:8px;}
.thost table{margin-top:0;}
.thost thead th{position:sticky;top:0;z-index:1;background:var(--surface-1);}
th.sortable{cursor:pointer;user-select:none;white-space:nowrap;}
th.sortable:hover{color:var(--text-secondary);}
th.sortable .ar{color:var(--s1);font-size:10px;}
.drill .thost{max-height:none;overflow:visible;}
.foot{margin-top:40px;font-size:11px;color:var(--muted);text-align:center;}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Session Demand Analytics</h1>
  <p>What drives demand (page views), add-to-cart, and conversion</p>
  <p class="note"><b>How to read this.</b> <b>Demand</b> = page views (PV). <b>Add-to-cart</b> and <b>Conversion</b> are <i>volume-weighted rates</i>
  (total carts / sales ÷ total page views for the group), so tiny sessions can't distort them. Times are <b>IST</b> (source is UTC).
  <b>All page-view sections use sessions dated from 1 Apr 2026 onward</b> (page views concentrate on open-enrollment sessions);
  the <b>keyword/theme tables use all available dates</b>.</p>
</header>

<div class="tabs" id="tabs"></div>
<div class="banner" id="banner"></div>
<div class="momctrl" style="margin:10px 0 0"><div class="grp"><span class="lbl">Months</span><div class="pillrow" id="monthsel"></div><span class="lbl" style="text-transform:none">affects month-by-month charts</span></div></div>

<div id="std-view">
<div class="kpis" id="kpis"></div>

<h2>The funnel <span class="sub">page view → add to cart → purchase</span></h2>
<div class="card" id="funnel"></div>

<h2>1 · Price <span class="sub">does what you charge move demand & conversion?</span></h2>
<div id="ins-price"></div>
<div class="grid2">
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV)</span></div><div id="price-pv"></div></div>
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s2)"></span>Add-to-cart %</span><span><span class="sw" style="background:var(--s3)"></span>Conversion %</span></div><div id="price-rate" class="dual"></div></div>
</div>

<h2>2 · Session type <span class="sub">online (STANDARD) vs OFFLINE</span></h2>
<div id="ins-type"></div>
<div class="card"><div id="type-tbl"></div></div>

<h2>3 · Day of week <span class="sub">by session's scheduled start day</span></h2>
<div id="ins-dow"></div>
<div class="grid2">
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV)</span></div><div id="dow-pv"></div></div>
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s2)"></span>Add-to-cart %</span><span><span class="sw" style="background:var(--s3)"></span>Conversion %</span></div><div id="dow-rate" class="dual"></div></div>
</div>
<div class="card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:6px">Session demand <b>normalized by site traffic</b> that weekday — demand index (100 = average day). <span style="color:var(--muted)">Caveat: session day = scheduled start; site traffic = browse day.</span></div>
  <div id="dow-norm"></div>
</div>

<h2>4 · Site traffic benchmark <span class="sub">overall course-page page views · Apr–Jul 2026 · browse day</span></h2>
<div id="ins-site"></div>
<div class="grid2">
  <div class="card"><div style="font-size:12px;color:var(--muted);margin-bottom:6px">Site PV by day of week <span style="color:var(--muted)">(number = demand index, 100 = avg)</span></div><div id="site-dow"></div></div>
  <div class="card"><div style="font-size:12px;color:var(--muted);margin-bottom:6px">Site PV by month</div><div id="site-month"></div></div>
</div>
<div class="card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:8px">Site PV by weekday, <b>one line per month</b> — the month-on-month pattern</div>
  <div id="site-heat"></div>
</div>

<h2>5 · Time of day <span class="sub">IST · session start time</span></h2>
<div id="ins-time"></div>
<div class="grid2">
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV)</span></div><div id="time-pv"></div></div>
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s2)"></span>Add-to-cart %</span><span><span class="sw" style="background:var(--s3)"></span>Conversion %</span></div><div id="time-rate" class="dual"></div></div>
</div>
<div class="card" id="time-norm-card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:6px">Session demand <b>normalized by site traffic</b> in that window — demand index (100 = average window). <span style="color:var(--muted)">Caveat: session time = scheduled start; site traffic = browse hour.</span></div>
  <div id="time-norm"></div>
</div>
<div class="card" id="site-hour-card">
  <div id="site-hour-note" style="font-size:12px;color:var(--muted);margin-bottom:6px"></div>
  <div id="site-hour"></div>
</div>

<h2>6 · Session name <span class="sub">length & theme keywords</span></h2>
<div id="ins-name"></div>
<div class="card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:6px">Name length (words) vs conversion — volume-weighted</div>
  <div id="word-rate" class="dual"></div>
</div>
<div class="card">
  <div id="kw-note" style="font-size:12px;color:var(--muted);margin-bottom:6px"></div>
  <div id="kw-tbl"></div>
</div>

<h2>7 · Session leaders <span class="sub">sort any column · search by name · min 3 sessions</span></h2>
<div class="card"><div id="leader-tbl"></div></div>

<h2>8 · Demand trend over time <span class="sub">monthly, by session start month (IST) · from Apr 2026</span></h2>
<div class="card"><div id="month-chart"></div></div>
</div><!-- /std-view -->

<div id="mom-view" style="display:none">
  <div class="momctrl">
    <div class="grp"><span class="lbl">Cohort</span><div class="pillrow" id="mom-cohort"></div></div>
    <div class="grp"><span class="lbl">Metric</span><div class="pillrow" id="mom-metric"></div></div>
  </div>
  <div id="mom-note" style="font-size:12px;color:var(--muted);margin:6px 0 4px"></div>
  <h2>Day of week — month on month <span class="sub">one line per month · x = weekday</span></h2>
  <div class="card"><div id="mom-dow"></div></div>
  <h2>Hour of day — month on month <span class="sub">one line per month · x = hour (IST)</span></h2>
  <div class="card"><div id="mom-hour"></div></div>
</div><!-- /mom-view -->

<div class="foot">Sheet1 (funnel) + Sheet2 (course info), joined on instance id · rates are PV-weighted</div>
</div>

<script>
const DATA = ''' + DATA_JS + r''';
const EXCL = DATA.excluded_leaders;
const fmt=n=>n>=1000?(n/1000).toFixed(n>=10000?0:1)+'k':(''+Math.round(n));
const pct=n=>n==null?'—':n.toFixed(2)+'%';
function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim();}
const cleanKey=k=>k.replace(/^\d+\s/,'').replace(/\(.*?\)/,'').trim()||k;
// time-of-day label with its IST hour-range definition, e.g. "Evening (6–9pm)"
const TIME_DEF={
 '1 Early AM (<9)':'Early AM (before 9am)',
 '2 Late Morning (9-12)':'Late Morning (9am–12pm)',
 '3 Afternoon (12-15)':'Afternoon (12–3pm)',
 '4 Late Afternoon (15-18)':'Late Afternoon (3–6pm)',
 '5 Evening (18-21)':'Evening (6–9pm)',
 '6 Night (21+)':'Night (9pm+)',
};
const timeLab=k=>TIME_DEF[k]||cleanKey(k);

// index bars centered on 100 (above avg = blue, below = orange)
function indexBars(el,rows,valFn,labFn,fmtFn){
 const max=Math.max(...rows.map(valFn),120);
 el.innerHTML=rows.map(r=>{
   const v=valFn(r); const w=max>0?Math.max(0.5,100*v/max):0;
   const col=v>=100?'var(--s1)':'var(--s3)';
   return `<div class="row"><div class="name" title="${labFn(r)}">${labFn(r)}</div>
   <div class="track"><div class="bar" style="width:${w}%;background:${col}"></div>
   <span class="val">${fmtFn(v)}</span></div></div>`;
 }).join('');
}
// vertical hourly bar chart (0-23), peak highlighted
function hourCurve(el,byHour){
 const max=Math.max(...byHour.map(x=>x.pv));
 let h='<div style="display:flex;align-items:flex-end;gap:2px;height:130px;border-bottom:1px solid var(--baseline)">';
 h+=byHour.map(x=>{const ht=max>0?Math.max(1,100*x.pv/max):1; const peak=x.pv===max;
   return `<div title="${String(x.hour).padStart(2,'0')}:00 IST — ${x.pv.toLocaleString()} PV" style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:100%">
     <div style="background:${peak?'var(--s3)':'var(--s1)'};height:${ht}%;border-radius:2px 2px 0 0;min-height:1px"></div></div>`;}).join('');
 h+='</div><div style="display:flex;gap:2px;margin-top:3px">';
 h+=byHour.map(x=>`<div class="axis" style="flex:1;text-align:center;font-size:8px">${x.hour%3===0?String(x.hour).padStart(2,'0'):''}</div>`).join('');
 h+='</div>';
 el.innerHTML=h;
}
// month x dow heatmap for site PV (S = this tab's matched baseline)
function renderSite(V){
 const S=V.site_pv; const scope=V.site_scope;
 barChart(document.getElementById('site-dow'),S.by_dow,r=>r.pv,r=>r.day,css('--s1'),
   (v)=>fmt(v));
 // overlay index label: re-render with index shown
 document.getElementById('site-dow').querySelectorAll('.row').forEach((row,i)=>{
   const idx=S.by_dow[i].index; const s=row.querySelector('.val');
   s.innerHTML=`${fmt(S.by_dow[i].pv)} <span style="color:var(--muted)">· ${idx}</span>`;
 });
 barChart(document.getElementById('site-month'),S.by_month.filter(r=>monthOK(r.month)),r=>r.pv,r=>r.month.replace(' 2026',''),css('--s2'),fmt);
 // month-on-month line chart: site PV by weekday, one line per month
 const days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
 const months=[...new Set(S.matrix.map(m=>m.month))];
 const cell=(m,d)=>{const c=S.matrix.find(x=>x.month===m&&x.day===d); return c?c.pv:0;};
 const siteSeries=months.map((m,i)=>({name:m.replace(' 2026',''),color:MONTH_COLORS[i%MONTH_COLORS.length],
   values:days.map(d=>cell(m,d))})).filter(s=>monthsOn.has(s.name));
 lineChart(document.getElementById('site-heat'), ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], siteSeries, fmt);
 const bd=[...S.by_dow].sort((a,b)=>b.pv-a.pv);
 const bm=[...S.by_month].sort((a,b)=>b.pv-a.pv);
 const scopeTxt = scope==='no4'
   ? 'This benchmark <b>excludes the 4 outlier leaders and offline</b>, matching this tab.'
   : 'This is the <b>overall</b> course-page benchmark (every leader & type), matching the “All sessions” tab.';
 ins('ins-site',`<b>The site is busiest mid-week and quietest on weekends.</b> <b>${bd[0].day}</b> pulls the most course-page traffic (index ${bd[0].index}), while <b>${bd[bd.length-1].day}</b> is lowest (${bd[bd.length-1].index}). By month, <b>${bm[0].month}</b> peaked (${fmt(bm[0].pv)} PV); ${bm[bm.length-1].month} is lowest/partial. ${scopeTxt} This is <i>browse-day</i> traffic — a scheduling & promotion benchmark, not tied to any one session.`);
}
function barChart(el,rows,valFn,labFn,color,fmtFn,suffixFn){
 const max=Math.max(...rows.map(valFn));
 el.innerHTML=rows.map(r=>{
   const v=valFn(r); const w=max>0?Math.max(0.5,100*v/max):0;
   const suf=suffixFn?` <span style="color:var(--muted)">${suffixFn(r)}</span>`:'';
   return `<div class="row"><div class="name" title="${labFn(r)}">${labFn(r)}</div>
   <div class="track"><div class="bar" style="width:${w}%;background:${color}"></div>
   <span class="val">${fmtFn(v)}${suf}</span></div></div>`;
 }).join('');
}
function dualChart(el,rows,labFn){
 const max=Math.max(...rows.map(r=>r.cart||0));
 el.innerHTML=rows.map(r=>{
   const wc=max>0?Math.max(0.5,100*(r.cart||0)/max):0;
   const ws=max>0?Math.max(0.5,100*(r.sale||0)/max):0;
   return `<div class="row"><div class="name" title="${labFn(r)}">${labFn(r)}</div>
   <div class="track" style="flex-direction:column;align-items:stretch;gap:3px">
     <div style="display:flex;align-items:center;gap:8px"><div class="bar" style="width:${wc}%;background:var(--s2)"></div><span class="val">${pct(r.cart)}</span></div>
     <div style="display:flex;align-items:center;gap:8px"><div class="bar" style="width:${ws}%;background:var(--s3)"></div><span class="val">${pct(r.sale)}</span></div>
   </div></div>`;
 }).join('');
}
function tableize(el,rows,cols){
 let h='<table><tr>'+cols.map(c=>`<th>${c[0]}</th>`).join('')+'</tr>';
 h+=rows.map(r=>'<tr>'+cols.map(c=>`<td>${c[1](r)}</td>`).join('')+'</tr>').join('');
 el.innerHTML=h+'</table>';
}
const wordLab=r=>({'(0.999, 5.0]':'1–5 words','(5.0, 6.0]':'6 words','(6.0, 7.0]':'7 words','(7.0, 16.0]':'8+ words'}[r.key]||r.key);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

// Generic sortable + searchable table. cfg:
//  rows, cols:[{label,get,val,align}], searchGet, placeholder, sortCol, sortDir, expandGet(r)|null, label(noun)
function makeTable(el,cfg){
 let sortCol = cfg.sortCol==null?null:cfg.sortCol, sortDir = cfg.sortDir||-1, term='';
 const expanded=new Set();
 el.innerHTML=`<div class="tbar"><input class="tsearch" placeholder="${cfg.placeholder||'Search…'}"><span class="tcount"></span></div><div class="thost"></div>`;
 const search=el.querySelector('.tsearch'), host=el.querySelector('.thost'), count=el.querySelector('.tcount');
 function draw(){
   let rows=cfg.rows.slice();
   if(term){const t=term.toLowerCase();rows=rows.filter(r=>cfg.searchGet(r).toLowerCase().includes(t));}
   if(sortCol!=null){
     const c=cfg.cols[sortCol];
     rows.sort((a,b)=>{let va=c.val(a),vb=c.val(b);
       return typeof va==='string'?sortDir*va.localeCompare(vb):sortDir*(va-vb);});
   }
   let h='<table><thead><tr>';
   cfg.cols.forEach((c,i)=>{
     const ar=sortCol===i?`<span class="ar">${sortDir<0?'▼':'▲'}</span>`:'';
     h+=`<th class="sortable" data-c="${i}"${c.align?` style="text-align:${c.align}"`:''}>${c.label} ${ar}</th>`;
   });
   h+='</tr></thead><tbody>';
   rows.forEach(r=>{
     const key=cfg.searchGet(r), exp=cfg.expandGet&&expanded.has(key);
     const cls=cfg.expandGet?('kwrow'+(exp?' open':'')):'';
     h+=`<tr class="${cls}" data-key="${esc(key)}">`;
     cfg.cols.forEach(c=>h+=`<td${c.align?` style="text-align:${c.align}"`:''}>${c.get(r)}</td>`);
     h+='</tr>';
     if(cfg.expandGet){
       h+=`<tr class="drill" data-key="${esc(key)}" style="display:${exp?'table-row':'none'}"><td colspan="${cfg.cols.length}">${cfg.expandGet(r)}</td></tr>`;
     }
   });
   h+='</tbody></table>';
   host.innerHTML=h;
   count.textContent=`${rows.length} ${cfg.noun||'rows'}`;
   host.querySelectorAll('th.sortable').forEach(th=>th.addEventListener('click',()=>{
     const i=+th.dataset.c;
     if(sortCol===i)sortDir=-sortDir;
     else{sortCol=i;sortDir=typeof cfg.cols[i].val(cfg.rows[0])==='string'?1:-1;}
     draw();
   }));
   if(cfg.expandGet) host.querySelectorAll('tr.kwrow').forEach(row=>row.addEventListener('click',()=>{
     const k=row.dataset.key; expanded.has(k)?expanded.delete(k):expanded.add(k); draw();
   }));
 }
 search.addEventListener('input',()=>{term=search.value;draw();});
 draw();
}

function drillHtml(ss){
 let inner='<div class="thost"><table><thead><tr><th>Top 5 sessions by demand</th><th style="text-align:left">Leader</th><th>Price</th><th>PV</th><th>Cart</th><th>Conv.</th></tr></thead><tbody>';
 inner+=(ss||[]).map(s=>`<tr><td class="dname">${esc(s.name)}<div class="dsub">${esc(s.type)}${s.date?' · '+esc(s.date):''}</div></td>`
   +`<td style="text-align:left">${esc(s.leader)}</td><td>₹${s.price.toLocaleString()}</td>`
   +`<td>${fmt(s.PV)}</td><td>${pct(s.cart)}</td><td>${pct(s.sale)}</td></tr>`).join('');
 return inner+'</tbody></table></div>';
}

const RATE_COLS = noun=>[
 {label:noun,get:r=>esc(r.key),val:r=>r.key,align:'left'},
 {label:'Sessions',get:r=>r.n,val:r=>r.n},
 {label:'Total PV',get:r=>fmt(r.PV_total),val:r=>r.PV_total},
 {label:'Median PV',get:r=>Math.round(r.PV_median),val:r=>r.PV_median},
 {label:'Add-to-cart',get:r=>pct(r.cart),val:r=>r.cart||0},
 {label:'Conversion',get:r=>pct(r.sale),val:r=>r.sale||0},
];

// dynamic insight helpers
const maxBy=(a,f)=>a.reduce((m,x)=>f(x)>f(m)?x:m);
const minBy=(a,f)=>a.reduce((m,x)=>f(x)<f(m)?x:m);
function ins(id,html){document.getElementById(id).innerHTML=`<div class="insight">${html}</div>`;}

function render(V, other){
 const o=V.overall;
 // KPIs (with delta vs the other view when provided)
 function delta(cur,prev,unit){
   if(prev==null) return '';
   const d=cur-prev; const s=d>=0?'+':'';
   const col=d>=0?'var(--good)':'var(--s3)';
   return `<div class="delta" style="color:${col}">${s}${d.toFixed(unit==='%'?2:0)}${unit} vs All</div>`;
 }
 const op = other?other.overall:null;
 document.getElementById('kpis').innerHTML=[
  ['Sessions (from 1 Apr)', o.sessions.toLocaleString(), o.sessions_all.toLocaleString()+' across all dates', op?delta(o.sessions,op.sessions,''):''],
  ['Total demand (PV)', fmt(o.PV_total), 'page views, sessions from 1 Apr', ''],
  ['Add-to-cart rate', o.cart.toFixed(2)+'%', fmt(o.carts_total)+' carts (weighted)', op?delta(o.cart,op.cart,'%'):''],
  ['Conversion rate', o.sale.toFixed(2)+'%', fmt(o.sales_total)+' purchases (weighted)', op?delta(o.sale,op.sale,'%'):''],
  ['Median PV / session', Math.round(o.PV_median), 'demand is highly skewed', ''],
 ].map(k=>`<div class="kpi"><div class="v">${k[1]}</div><div class="l">${k[0]}</div><div class="d">${k[2]}</div>${k[3]}</div>`).join('');

 // funnel
 const stages=[['Page views',o.PV_total,'var(--s1)','100%'],
   ['Added to cart',o.carts_total,'var(--s2)',o.cart.toFixed(2)+'% of PV'],
   ['Purchased',o.sales_total,'var(--s3)',o.sale.toFixed(2)+'% of PV']];
 const fmax=stages[0][1];
 document.getElementById('funnel').innerHTML=stages.map(s=>{
   const w=Math.max(0.5,100*s[1]/fmax);
   return `<div class="row"><div class="name" style="color:var(--text-primary);font-weight:600">${s[0]}</div>
   <div class="track"><div class="bar" style="width:${w}%;background:${s[2]}"></div>
   <span class="val">${fmt(s[1])} <span style="color:var(--muted)">· ${s[3]}</span></span></div></div>`;
 }).join('');

 const priceRows=V.price_tier.filter(r=>r.PV_total>0);
 barChart(document.getElementById('price-pv'),priceRows,r=>r.PV_total,r=>r.key+' ₹',css('--s1'),fmt);
 dualChart(document.getElementById('price-rate'),priceRows,r=>r.key+' ₹');
 barChart(document.getElementById('dow-pv'),V.dow,r=>r.PV_total,r=>r.key,css('--s1'),fmt,r=>'('+r.n+')');
 dualChart(document.getElementById('dow-rate'),V.dow,r=>r.key.slice(0,3));
 // normalized: session demand per unit site traffic (index, 100 = avg day)
 indexBars(document.getElementById('dow-norm'),V.dow.filter(r=>r.demand_index!=null),
   r=>r.demand_index,r=>r.key,v=>v.toFixed(0));
 renderSite(V);  // site-traffic section — baseline matches this tab's cohort
 barChart(document.getElementById('time-pv'),V.time,r=>r.PV_total,r=>timeLab(r.key),css('--s1'),fmt,r=>'('+r.n+')');
 dualChart(document.getElementById('time-rate'),V.time,r=>timeLab(r.key));
 // time-of-day normalization + hourly site curve (only when this tab has matching site data)
 const tnCard=document.getElementById('time-norm-card'), shCard=document.getElementById('site-hour-card');
 if(V.site_time){
   tnCard.style.display=''; shCard.style.display='';
   indexBars(document.getElementById('time-norm'),V.time.filter(r=>r.demand_index!=null),
     r=>r.demand_index,r=>timeLab(r.key),v=>v.toFixed(0));
   document.getElementById('site-hour-note').innerHTML='Site traffic by <b>hour of day</b> (IST, browse hour) — overall course pages, '
     + (V.site_scope==='no4'?'excl. 4 leaders & offline':'all leaders & types')+'. Peak hour in orange.';
   hourCurve(document.getElementById('site-hour'),V.site_time.by_hour);
 }else{ tnCard.style.display='none'; shCard.style.display='none'; }
 dualChart(document.getElementById('word-rate'),V.wordq,wordLab);

 tableize(document.getElementById('type-tbl'),V.type,[
  ['Type',r=>r.key],['Sessions',r=>r.n],['Total PV',r=>fmt(r.PV_total)],
  ['Median PV',r=>Math.round(r.PV_median)],['Add-to-cart',r=>pct(r.cart)],['Conversion',r=>pct(r.sale)]]);

 const single=V.kw_mode==='single';
 document.getElementById('kw-note').innerHTML = (single
   ? 'Each session counted <b>once</b>, under its single <b>main theme</b> (short titles), so themes are mutually exclusive. '
   : 'Multi-tag: a session appears under <b>every</b> theme word in its name (so it can be counted more than once). ')
   + '<b>Uses all available dates</b> (not just from Apr 1). <b>Click a row</b> for its top 5 sessions.';
 makeTable(document.getElementById('kw-tbl'),{
   rows:V.keywords, cols:RATE_COLS(single?'Main theme':'Keyword'), searchGet:r=>r.key,
   placeholder:single?'Search themes…':'Search keywords…', noun:single?'themes':'keywords',
   sortCol:2, sortDir:-1,
   expandGet:r=>drillHtml((V.keyword_sessions||{})[r.key]) });

 makeTable(document.getElementById('leader-tbl'),{
   rows:V.leaders, cols:RATE_COLS('Leader'), searchGet:r=>r.key,
   placeholder:'Search leaders…', noun:'leaders (≥3 sessions)', sortCol:2, sortDir:-1 });

 // monthly
 const rows=V.monthly.filter(r=>monthOK(r.key)); const mmax=Math.max(1,...rows.map(r=>r.PV_total));
 let h='<div style="display:flex;align-items:flex-end;gap:3px;height:160px;border-bottom:1px solid var(--baseline)">';
 h+=rows.map(r=>{const ht=mmax>0?Math.max(1,100*r.PV_total/mmax):1;
   return `<div title="${r.key}: ${fmt(r.PV_total)} PV, cart ${pct(r.cart)}, sale ${pct(r.sale)}" style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:100%">
     <div style="background:var(--s1);height:${ht}%;border-radius:3px 3px 0 0;min-height:1px"></div></div>`;}).join('');
 h+='</div><div style="display:flex;gap:3px;margin-top:4px">';
 h+=rows.map(r=>`<div class="axis" style="flex:1;text-align:center;font-size:9px">${r.key.slice(2)}</div>`).join('');
 h+='</div><div class="legend" style="margin-top:10px"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV) per month — sessions dated from Apr 2026 onward</span></div>';
 document.getElementById('month-chart').innerHTML=h;

 // ---- dynamic insights ----
 const pr=priceRows;
 const cheap=pr.find(r=>r.key==='1-300')||pr[0], exp=pr.find(r=>r.key==='1500+')||pr[pr.length-1];
 ins('ins-price',`<b>Cheaper converts better; price barely moves raw demand.</b> The <b>${cheap.key} ₹</b> tier adds to cart at <b>${pct(cheap.cart)}</b> and converts at <b>${pct(cheap.sale)}</b>, versus <b>${exp.key} ₹</b> at ${pct(exp.cart)} / ${pct(exp.sale)}. Volume clusters in the mid ₹601–1000 band.`);

 const std=V.type.find(t=>t.key==='STANDARD'), off=V.type.find(t=>t.key==='OFFLINE');
 if(off){
   ins('ins-type',`<b>Online (STANDARD) is more efficient than OFFLINE.</b> Offline draws higher median demand (${Math.round(off.PV_median)} vs ${Math.round(std.PV_median)} PV) but converts <b>${pct(off.sale)} vs ${pct(std.sale)}</b>. Offline is a small, premium slice (${off.n} sessions).`);
 }else{
   ins('ins-type',`<b>Online sessions only in this view.</b> OFFLINE sessions are excluded here. Across all data, offline draws higher median demand but converts worse than online — see the “All sessions” tab for the comparison.`);
 }

 const bestDayCart=maxBy(V.dow,r=>r.cart||0), bestDaySale=maxBy(V.dow,r=>r.sale||0);
 const wk=V.dow.filter(r=>['Saturday','Sunday'].includes(r.key)), wd=V.dow.filter(r=>!['Saturday','Sunday'].includes(r.key));
 const ws=wk.reduce((a,r)=>a+r.PV_total*r.sale,0)/wk.reduce((a,r)=>a+r.PV_total,0);
 const wds=wd.reduce((a,r)=>a+r.PV_total*r.sale,0)/wd.reduce((a,r)=>a+r.PV_total,0);
 const idxRows=V.dow.filter(r=>r.demand_index!=null);
 const topIdx=idxRows.length?maxBy(idxRows,r=>r.demand_index):null;
 const idxTxt=topIdx?` <b>Normalized by site traffic</b>, <b>${topIdx.key}</b>-scheduled sessions capture the most demand per unit of site traffic (index ${topIdx.demand_index.toFixed(0)}) — partly because the site is quieter that day (low denominator), so read it alongside the raw numbers.`:'';
 ins('ins-dow',`<b>Weekdays convert better; weekends draw browsing.</b> Weekday conversion ≈ <b>${wds.toFixed(2)}%</b> vs weekend ≈ <b>${ws.toFixed(2)}%</b>. Best add-to-cart is <b>${bestDayCart.key}</b> (${pct(bestDayCart.cart)}); best conversion is <b>${bestDaySale.key}</b> (${pct(bestDaySale.sale)}).${idxTxt}`);

 const volTime=maxBy(V.time,r=>r.PV_total), bestTimeSale=maxBy(V.time,r=>r.sale||0);
 let timeNorm='';
 if(V.site_time){
   const tIdx=V.time.filter(r=>r.demand_index!=null);
   const topT=tIdx.length?maxBy(tIdx,r=>r.demand_index):null;
   const sitePeak=[...V.site_time.by_bucket].sort((a,b)=>b.pv-a.pv)[0];
   if(topT) timeNorm=` <b>Normalized by site traffic</b>, the <b>${cleanKey(topT.key)}</b> window is the most efficient (index ${topT.demand_index.toFixed(0)}) — even though the site is busiest in the <b>${cleanKey(sitePeak.key)}</b> window (browse hour ≠ scheduled slot).`;
 }
 ins('ins-time',`<b>${cleanKey(volTime.key)} drives volume; ${cleanKey(bestTimeSale.key)} converts hardest.</b> The ${cleanKey(volTime.key)} window holds the most demand (${fmt(volTime.PV_total)} PV), while <b>${cleanKey(bestTimeSale.key)}</b> has the best conversion (${pct(bestTimeSale.sale)}) — a smaller, high-intent audience.${timeNorm}`);

 const shortW=V.wordq[0], longW=V.wordq[V.wordq.length-1];
 const topKw=[...V.keywords].filter(k=>k.n>=15).sort((a,b)=>b.sale-a.sale).slice(0,5).map(k=>k.key).join(', ');
 ins('ins-name',`<b>Short, concrete names convert better.</b> Shortest names (${wordLab(shortW)}) convert at <b>${pct(shortW.sale)}</b> vs longest (${wordLab(longW)}) at <b>${pct(longW.sale)}</b>. Highest-converting themes: <b>${topKw}</b>.`);
}

// ---- Month-on-month tab ----
const MONTHS_JS=['Apr 2026','May 2026','Jun 2026','Jul 2026'];
const DOW_FULL=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
const DOW_ABBR=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const pct1=v=>v.toFixed(1)+'%';
const MOM_METRICS=[
 {k:'platform_pv',label:'Platform PVs',get:r=>r.platform_pv,f:fmt},
 {k:'session_pv', label:'Session PVs', get:r=>r.session_pv, f:fmt},
 {k:'cart_pct',   label:'Add-to-cart %',get:r=>r.session_pv?100*r.carts/r.session_pv:0,f:pct1},
 {k:'sale_pct',   label:'Purchase %',   get:r=>r.session_pv?100*r.sales/r.session_pv:0,f:pct1},
 {k:'capture',    label:'Capture % (sess PV ÷ platform PV)',get:r=>r.platform_pv?100*r.session_pv/r.platform_pv:0,f:v=>v.toFixed(0)+'%'},
];
let momCohort='all', momMetric='session_pv';

const MONTH_COLORS=['var(--s1)','var(--s2)','var(--s3)','var(--s4)'];
// one line per month; single y-axis (metric), x = weekday/hour categories
function lineChart(el, catLabels, series, yfmt){
 const W=720,H=280,pl=54,pr=14,pt=14,pb=30;
 const iw=W-pl-pr, ih=H-pt-pb, n=catLabels.length;
 const maxV=Math.max(1,...series.flatMap(s=>s.values.filter(v=>v!=null)));
 const X=i=> pl+(n<=1?iw/2:iw*i/(n-1));
 const Y=v=> pt+ih*(1-v/maxV);
 let g='';
 [0,.25,.5,.75,1].forEach(t=>{const yy=pt+ih*(1-t);
   g+=`<line x1="${pl}" y1="${yy}" x2="${W-pr}" y2="${yy}" stroke="var(--grid)" stroke-width="1"/>`
     +`<text x="${pl-7}" y="${yy+3}" text-anchor="end" font-size="9" fill="var(--muted)">${yfmt(maxV*t)}</text>`;});
 let xl=''; const step=n>12?3:1;
 catLabels.forEach((c,i)=>{ if(i%step===0||i===n-1) xl+=`<text x="${X(i)}" y="${H-9}" text-anchor="middle" font-size="9" fill="var(--muted)">${c}</text>`;});
 let paths='';
 series.forEach(s=>{
   const pts=s.values.map((v,i)=>`${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' ');
   paths+=`<polyline points="${pts}" fill="none" stroke="${s.color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
   s.values.forEach((v,i)=>{paths+=`<circle cx="${X(i).toFixed(1)}" cy="${Y(v).toFixed(1)}" r="2.6" fill="${s.color}"><title>${s.name} · ${catLabels[i]}: ${yfmt(v)}</title></circle>`;});
 });
 const legend=series.map(s=>`<span style="margin-right:14px;font-size:12px;color:var(--text-secondary);white-space:nowrap"><span style="display:inline-block;width:12px;height:3px;border-radius:2px;background:${s.color};margin-right:5px;vertical-align:middle"></span>${s.name}</span>`).join('');
 el.innerHTML=`<div class="legend" style="margin-bottom:8px">${legend}</div>`
   +`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto" preserveAspectRatio="xMidYMid meet">${g}${xl}${paths}</svg>`;
}
function renderMoM(){
 // controls
 document.getElementById('mom-cohort').innerHTML=[['all','Overall'],['no4','Without 4 + offline']]
   .map(c=>`<button class="pill ${momCohort===c[0]?'on':''}" data-c="${c[0]}">${c[1]}</button>`).join('');
 document.getElementById('mom-metric').innerHTML=MOM_METRICS
   .map(m=>`<button class="pill ${momMetric===m.k?'on':''}" data-m="${m.k}">${m.label.split(' (')[0]}</button>`).join('');
 document.querySelectorAll('#mom-cohort .pill').forEach(b=>b.onclick=()=>{momCohort=b.dataset.c;renderMoM();});
 document.querySelectorAll('#mom-metric .pill').forEach(b=>b.onclick=()=>{momMetric=b.dataset.m;renderMoM();});
 const met=MOM_METRICS.find(x=>x.k===momMetric);
 const M=DATA.mom[momCohort];
 document.getElementById('mom-note').innerHTML=`Showing <b>${met.label}</b> for the <b>${momCohort==='all'?'overall':'excl. 4 leaders + offline'}</b> cohort — one line per month. `
   +(momMetric==='platform_pv'?'Platform = total course-page page views (browse day/hour).'
     :momMetric==='capture'?'Capture can exceed 100% — a session scheduled that day/hour draws views across many browse days (scheduled ≠ browse axis).'
     :'Session metric = sessions <b>scheduled</b> in that month & weekday/hour (from 1 Apr).');
 const dowSeries=MONTHS_JS.map((m,i)=>({name:m.replace(' 2026',''),color:MONTH_COLORS[i],
   values:DOW_FULL.map(d=>{const r=M.dow.find(x=>x.month===m&&x.day===d);return r?met.get(r):0;})})).filter(s=>monthsOn.has(s.name));
 lineChart(document.getElementById('mom-dow'), DOW_ABBR, dowSeries, met.f);
 const hours=[...Array(24).keys()];
 const hourSeries=MONTHS_JS.map((m,i)=>({name:m.replace(' 2026',''),color:MONTH_COLORS[i],
   values:hours.map(h=>{const r=M.hour.find(x=>x.month===m&&x.hour===h);return r?met.get(r):0;})})).filter(s=>monthsOn.has(s.name));
 lineChart(document.getElementById('mom-hour'), hours.map(h=>String(h).padStart(2,'0')), hourSeries, met.f);
}

// ---- global month selector (month-series charts only) ----
const MONTH_KEYS=['Apr','May','Jun','Jul'];
let monthsOn=new Set(MONTH_KEYS);
const shortOf=s=>{ if(/^\d{4}-\d{2}/.test(s)){return ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+s.slice(5,7)];} return String(s).split(' ')[0]; };
const monthOK=label=>monthsOn.has(shortOf(label));
function renderMonthSel(){
 document.getElementById('monthsel').innerHTML=MONTH_KEYS
   .map(m=>`<button class="pill ${monthsOn.has(m)?'on':''}" data-mo="${m}">${m}</button>`).join('');
 document.querySelectorAll('#monthsel .pill').forEach(b=>b.onclick=()=>{
   const m=b.dataset.mo;
   if(monthsOn.has(m)){ if(monthsOn.size>1) monthsOn.delete(m); } else monthsOn.add(m);
   renderMonthSel(); refresh();
 });
}
function refresh(){ if(cur==='mom') renderMoM(); else render(DATA[cur], cur==='all'?null:DATA.all); }

// tabs
let cur='all';
function setTab(k){
 cur=k;
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.k===k));
 const sv=document.getElementById('std-view'), mv=document.getElementById('mom-view');
 const b=document.getElementById('banner');
 const n=x=>DATA[x].overall.sessions.toLocaleString();
 if(k==='mom'){
   sv.style.display='none'; mv.style.display=''; renderMoM();
   b.innerHTML=`<b>Month-on-month funnel</b> by weekday and hour, Apr–Jul 2026. Toggle cohort and metric below. Platform PVs are browse-time; session metrics are by scheduled start.`;
 }else{
   sv.style.display=''; mv.style.display='none';
   render(DATA[k], k==='all'?null:DATA.all);   // deltas baselined to All sessions
   const BAN={
    all:`Showing <b>all ${n('all')}</b> sessions (page-view sections from 1 Apr) — <b>every leader and type</b> included. Each session is filed under its <b>single main theme</b>.`,
    online_single:`Showing <b>${n('online_single')}</b> sessions — <b>online only (OFFLINE removed) and excluding the 4 outlier leaders</b> (${EXCL.join(', ')}). The clean baseline: what a standard online session by a non-star leader does. Each session under its <b>single main theme</b>.`,
   };
   b.innerHTML=BAN[k];
 }
 window.scrollTo({top:0,behavior:'instant'});
}
document.getElementById('tabs').innerHTML=[
 ['all','All sessions',DATA.all.overall.sessions+' sessions'],
 ['online_single','Without 4 leaders + offline',DATA.online_single.overall.sessions+' sessions'],
 ['mom','Month-on-month','weekday & hour funnel'],
].map(t=>`<button class="tab" data-k="${t[0]}">${t[1]}<span class="c">${t[2]}</span></button>`).join('');
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>setTab(t.dataset.k)));
renderMonthSel();
setTab('all');
</script>
</body>
</html>'''

for fn in ('Session Demand Dashboard.html', 'index.html'):  # index.html = GitHub Pages root
    open(fn,'w').write(HTML)
print('wrote Session Demand Dashboard.html + index.html', len(HTML), 'bytes')
