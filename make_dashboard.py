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
  --s1:#2a78d6; --s2:#1baf7a; --s3:#eb6834; --good:#0ca30c; --warn:#fab219;
}
@media (prefers-color-scheme: dark){
  :root{
    --surface-1:#1a1a19; --page:#0d0d0d;
    --text-primary:#fff; --text-secondary:#c3c2b7; --muted:#898781;
    --grid:#2c2c2a; --baseline:#383835; --border:rgba(255,255,255,0.10);
    --s1:#3987e5; --s2:#199e70; --s3:#d95926; --good:#0ca30c;
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
.row .name{width:150px;flex:0 0 150px;color:var(--text-secondary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.row .track{flex:1;display:flex;align-items:center;gap:8px;}
.bar{height:16px;border-radius:0 4px 4px 0;min-width:2px;}
.row .val{font-variant-numeric:tabular-nums;color:var(--text-primary);font-size:12px;}
.legend{display:flex;gap:16px;font-size:12px;color:var(--text-secondary);margin:2px 0 10px;flex-wrap:wrap;}
.legend .sw{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:middle;}
.dual .name{width:130px;flex-basis:130px;}
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
  Page views concentrate on upcoming sessions open for enrollment.</p>
</header>

<div class="tabs" id="tabs"></div>
<div class="banner" id="banner"></div>

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

<h2>3 · Day of week</h2>
<div id="ins-dow"></div>
<div class="grid2">
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV)</span></div><div id="dow-pv"></div></div>
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s2)"></span>Add-to-cart %</span><span><span class="sw" style="background:var(--s3)"></span>Conversion %</span></div><div id="dow-rate" class="dual"></div></div>
</div>

<h2>4 · Time of day <span class="sub">IST · session start time</span></h2>
<div id="ins-time"></div>
<div class="grid2">
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV)</span></div><div id="time-pv"></div></div>
  <div class="card"><div class="legend"><span><span class="sw" style="background:var(--s2)"></span>Add-to-cart %</span><span><span class="sw" style="background:var(--s3)"></span>Conversion %</span></div><div id="time-rate" class="dual"></div></div>
</div>

<h2>5 · Session name <span class="sub">length & theme keywords</span></h2>
<div id="ins-name"></div>
<div class="card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:6px">Name length (words) vs conversion — volume-weighted</div>
  <div id="word-rate" class="dual"></div>
</div>
<div class="card">
  <div style="font-size:12px;color:var(--muted);margin-bottom:6px">Top theme keywords by total demand — <b>click a row</b> to see its top 5 sessions</div>
  <div id="kw-tbl"></div>
</div>

<h2>6 · Session leaders <span class="sub">sort any column · search by name · min 3 sessions</span></h2>
<div class="card"><div id="leader-tbl"></div></div>

<h2>7 · Demand trend over time <span class="sub">monthly, by session start month (IST)</span></h2>
<div class="card"><div id="month-chart"></div></div>

<div class="foot">Sheet1 (funnel) + Sheet2 (course info), joined on instance id · rates are PV-weighted</div>
</div>

<script>
const DATA = ''' + DATA_JS + r''';
const EXCL = DATA.excluded_leaders;
const fmt=n=>n>=1000?(n/1000).toFixed(n>=10000?0:1)+'k':(''+Math.round(n));
const pct=n=>n==null?'—':n.toFixed(2)+'%';
function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim();}
const cleanKey=k=>k.replace(/^\d+\s/,'').replace(/\(.*?\)/,'').trim()||k;

function barChart(el,rows,valFn,labFn,color,fmtFn){
 const max=Math.max(...rows.map(valFn));
 el.innerHTML=rows.map(r=>{
   const v=valFn(r); const w=max>0?Math.max(0.5,100*v/max):0;
   return `<div class="row"><div class="name" title="${labFn(r)}">${labFn(r)}</div>
   <div class="track"><div class="bar" style="width:${w}%;background:${color}"></div>
   <span class="val">${fmtFn(v)}</span></div></div>`;
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
  ['Tracked sessions', o.sessions.toLocaleString(), 'joined to course info', op?delta(o.sessions,op.sessions,''):''],
  ['Total demand (PV)', fmt(o.PV_total), 'cumulative page views', ''],
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
 barChart(document.getElementById('dow-pv'),V.dow,r=>r.PV_total,r=>r.key,css('--s1'),fmt);
 dualChart(document.getElementById('dow-rate'),V.dow,r=>r.key.slice(0,3));
 barChart(document.getElementById('time-pv'),V.time,r=>r.PV_total,r=>cleanKey(r.key),css('--s1'),fmt);
 dualChart(document.getElementById('time-rate'),V.time,r=>cleanKey(r.key));
 dualChart(document.getElementById('word-rate'),V.wordq,wordLab);

 tableize(document.getElementById('type-tbl'),V.type,[
  ['Type',r=>r.key],['Sessions',r=>r.n],['Total PV',r=>fmt(r.PV_total)],
  ['Median PV',r=>Math.round(r.PV_median)],['Add-to-cart',r=>pct(r.cart)],['Conversion',r=>pct(r.sale)]]);

 makeTable(document.getElementById('kw-tbl'),{
   rows:V.keywords, cols:RATE_COLS('Keyword'), searchGet:r=>r.key,
   placeholder:'Search keywords…', noun:'keywords', sortCol:2, sortDir:-1,
   expandGet:r=>drillHtml((V.keyword_sessions||{})[r.key]) });

 makeTable(document.getElementById('leader-tbl'),{
   rows:V.leaders, cols:RATE_COLS('Leader'), searchGet:r=>r.key,
   placeholder:'Search leaders…', noun:'leaders (≥3 sessions)', sortCol:2, sortDir:-1 });

 // monthly
 const rows=V.monthly; const mmax=Math.max(...rows.map(r=>r.PV_total));
 let h='<div style="display:flex;align-items:flex-end;gap:3px;height:160px;border-bottom:1px solid var(--baseline)">';
 h+=rows.map(r=>{const ht=mmax>0?Math.max(1,100*r.PV_total/mmax):1;
   return `<div title="${r.key}: ${fmt(r.PV_total)} PV, cart ${pct(r.cart)}, sale ${pct(r.sale)}" style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:100%">
     <div style="background:var(--s1);height:${ht}%;border-radius:3px 3px 0 0;min-height:1px"></div></div>`;}).join('');
 h+='</div><div style="display:flex;gap:3px;margin-top:4px">';
 h+=rows.map(r=>`<div class="axis" style="flex:1;text-align:center;font-size:9px">${r.key.slice(2)}</div>`).join('');
 h+='</div><div class="legend" style="margin-top:10px"><span><span class="sw" style="background:var(--s1)"></span>Total demand (PV) per month — step-change from 2026 (open-enrollment sessions)</span></div>';
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
 ins('ins-dow',`<b>Weekdays convert better; weekends draw browsing.</b> Weekday conversion ≈ <b>${wds.toFixed(2)}%</b> vs weekend ≈ <b>${ws.toFixed(2)}%</b>. Best add-to-cart is <b>${bestDayCart.key}</b> (${pct(bestDayCart.cart)}); best conversion is <b>${bestDaySale.key}</b> (${pct(bestDaySale.sale)}).`);

 const volTime=maxBy(V.time,r=>r.PV_total), bestTimeSale=maxBy(V.time,r=>r.sale||0);
 ins('ins-time',`<b>${cleanKey(volTime.key)} drives volume; ${cleanKey(bestTimeSale.key)} converts hardest.</b> The ${cleanKey(volTime.key)} window holds the most demand (${fmt(volTime.PV_total)} PV), while <b>${cleanKey(bestTimeSale.key)}</b> has the best conversion (${pct(bestTimeSale.sale)}) — a smaller, high-intent audience.`);

 const shortW=V.wordq[0], longW=V.wordq[V.wordq.length-1];
 const topKw=[...V.keywords].filter(k=>k.n>=15).sort((a,b)=>b.sale-a.sale).slice(0,5).map(k=>k.key).join(', ');
 ins('ins-name',`<b>Short, concrete names convert better.</b> Shortest names (${wordLab(shortW)}) convert at <b>${pct(shortW.sale)}</b> vs longest (${wordLab(longW)}) at <b>${pct(longW.sale)}</b>. Highest-converting themes: <b>${topKw}</b>.`);
}

// tabs
let cur='all';
function setTab(k){
 cur=k;
 document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on',t.dataset.k===k));
 render(DATA[k], k==='all'?null:DATA.all);   // deltas baselined to All sessions
 const b=document.getElementById('banner');
 const n=x=>DATA[x].overall.sessions.toLocaleString();
 const BAN={
  all:`Showing <b>all ${n('all')}</b> tracked sessions — every type and leader included.`,
  filtered:`Showing <b>${n('filtered')}</b> sessions — <b>excluding 4 high-volume leaders</b> (${EXCL.join(', ')}) who together drove ~30% of all page views. The "typical session" view, undistorted by the biggest names.`,
  online_clean:`Showing <b>${n('online_clean')}</b> sessions — <b>online only (OFFLINE removed) and excluding the 4 outlier leaders</b>. The most conservative baseline: what a standard online session, run by a non-star leader, actually does.`,
 };
 b.innerHTML=BAN[k];
 window.scrollTo({top:0,behavior:'instant'});
}
document.getElementById('tabs').innerHTML=[
 ['all','All sessions',DATA.all.overall.sessions+' sessions'],
 ['filtered','Excluding 4 outlier leaders',DATA.filtered.overall.sessions+' sessions'],
 ['online_clean','Online only, excl. 4 leaders',DATA.online_clean.overall.sessions+' sessions'],
].map(t=>`<button class="tab" data-k="${t[0]}">${t[1]}<span class="c">${t[2]}</span></button>`).join('');
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>setTab(t.dataset.k)));
setTab('all');
</script>
</body>
</html>'''

open('Session Demand Dashboard.html','w').write(HTML)
print('wrote Session Demand Dashboard.html', len(HTML), 'bytes')
