// Site adaptation of the reviewed diagram; data and scores remain unchanged.
(()=>{
 const root=document.getElementById('explorer');
 const data=window.TEG_SIGNAL_EVIDENCE;
 const layers=['family','emotion','chemical','sensory'];
 const titles={family:'Families',emotion:'Emotions / states',chemical:'Neurochemicals',sensory:'Sensory channels'};
 const selected=root.querySelector('[data-inspect]');
 const map=new Map(data.nodes.map(n=>[n.id,n]));
 const visible=new Set(layers);
 const signals=window.TEG_SIGNALS.signals;
 const params=new URLSearchParams(location.search);
 let signal=Object.hasOwn(signals,params.get('signal'))?params.get('signal'):'';
 let reading=params.get('reading')==='chronic'?'chronic':'fluid';
 let hash='';try{hash=decodeURIComponent(location.hash.slice(1));}catch(_){}
 let focus=map.has(hash)?hash:map.has('emotion-'+signal)?'emotion-'+signal:signal?'':'family-2';
 if(map.get(focus)?.type==='emotion')signal=focus.slice(8);
 if(signal&&!signals[signal].chronic)reading='fluid';
 const missing=root.querySelector('[data-missing-signal]');
 if(signal&&!map.has('emotion-'+signal)){
  missing.hidden=false;missing.textContent=signals[signal].name+' is not included in this working diagram. Your signal record remains available through the return links.';
 }
 function route(kind){
  const path={record:'../map.html',biology:'neurochemistry.html',fluid:'../emotion/fluid.html',chronic:'../emotion/chronic.html',recovery:'recruitment-persistence-and-recovery.html',return:'../../03-model-2-gradient/return.html'}[kind];
  const url=new URL(path,location.href);
  url.searchParams.set('reading',['fluid','chronic'].includes(kind)?kind:reading);
  if(signal){
   if(kind==='record'||kind==='biology')url.hash=signal;
   else if(kind==='fluid'||kind==='chronic')url.hash='signal-'+signal;
   else url.searchParams.set('signal',signal);
  }
  if(kind==='recovery'||kind==='return'){
   url.searchParams.set('from','evidence-connections');
   if(focus)url.searchParams.set('node',focus);
  }
  return url.href;
 }
 function syncContext(save=false){
  if(map.get(focus)?.type==='emotion'){
   signal=focus.slice(8);missing.hidden=true;
  }
  document.body.dataset.signalId=signal;
  document.body.dataset.signalReading=reading;
  if(save){
   const url=new URL(location.href);url.hash=focus;
   if(signal)url.searchParams.set('signal',signal);else url.searchParams.delete('signal');
   url.searchParams.set('reading',reading);
   history.replaceState(null,'',url);
  }
  document.querySelectorAll('[data-evidence-route]').forEach(a=>{a.href=route(a.dataset.evidenceRoute);});
  dispatchEvent(new Event('signalcontextchange'));
 }
 function choose(id){focus=id;selected.value=focus;syncContext(true);draw();detail();}
 syncContext();
 const colours={family:'var(--cyan)',emotion:'var(--cyan)',chemical:'var(--violet)',sensory:'var(--evidence)'};
 function colour(n){return n.family===2?'var(--magenta)':n.family===1?'var(--amber)':colours[n.type];}
 const el=(tag,attrs={},parent)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(parent)parent.append(e);return e;};
 function words(label,width){const limit=Math.max(11,Math.floor(width/6.8));let out=[''];for(const w of label.match(/[^\s-]+-?/g)||[]){let last=out.length-1;if(out[last]&&(out[last]+' '+w).length>limit)out.push(w);else out[last]+=(out[last]?' ':'')+w;}return out;}
 layers.forEach(type=>{const group=document.createElement('optgroup');group.label=titles[type];data.nodes.filter(n=>n.type===type).forEach(n=>{const opt=document.createElement('option');opt.value=n.id;opt.textContent=n.label;group.append(opt);});selected.append(group);});
 function draw(){
  const host=root.querySelector('[data-plot]');const width=Math.max(280,host.getBoundingClientRect().width);
  const shown=layers.filter(t=>visible.has(t));const cols=width<600?Math.min(2,shown.length):shown.length;
  const positions=new Map();let totalHeight=0;const heads=[];
  if(!shown.length){host.replaceChildren();root.querySelector('[data-count]').textContent='No layers visible. Enable a layer above.';return;}
  for(let start=0;start<shown.length;start+=cols){
   const row=shown.slice(start,start+cols);const cell=width/row.length;
   const maxCount=Math.max(...row.map(t=>data.nodes.filter(n=>n.type===t).length));const rowHeight=maxCount*48+62;
   row.forEach((type,col)=>{
    const ns=data.nodes.filter(n=>n.type===type);heads.push({label:titles[type],x:col*cell+10,y:totalHeight+18});
    ns.forEach((n,i)=>{let y=totalHeight+54+i*48;if(type==='family'&&row.includes('emotion')){const all=data.nodes.filter(q=>q.type==='emotion');const memberIndices=all.map((q,j)=>q.family===n.family?j:-1).filter(j=>j>=0);y=totalHeight+54+48*memberIndices.reduce((a,b)=>a+b,0)/memberIndices.length;}positions.set(n.id,{x:col*cell+(type==='family'?cell-24:24),y,cell,labelWidth:cell-52});});
   });totalHeight+=rowHeight;
  }
  const svg=el('svg',{class:'network-svg',viewBox:`0 0 ${width} ${totalHeight}`,width,height:totalHeight,role:'img','aria-label':'Eigenvector centrality network. Use Inspect a node for keyboard access to scores, neighbours and evidence.'});
  el('title',{},svg).textContent='Families, emotions, neurochemicals and sensory channels';
  el('desc',{},svg).textContent='Node circle area encodes centrality in a 53-node audit graph. Edges include membership, candidate associations and null results. Positions are categorical, not causal. Layer switches do not recalculate scores.';
  const neighbours=new Set([focus]);data.edges.forEach(e=>{if(e.a===focus)neighbours.add(e.b);if(e.b===focus)neighbours.add(e.a);});
  let linkCount=0;
  data.edges.forEach(e=>{
   if(!positions.has(e.a)||!positions.has(e.b))return;linkCount++;
   const a=positions.get(e.a),b=positions.get(e.b),active=focus&&(e.a===focus||e.b===focus);
   const dx=b.x-a.x;const d=Math.abs(a.y-b.y)>800?`M${a.x},${a.y} C${a.x+45},${a.y+80} ${b.x-45},${b.y-80} ${b.x},${b.y}`:`M${a.x},${a.y} C${a.x+dx*.55},${a.y} ${b.x-dx*.55},${b.y} ${b.x},${b.y}`;
   const path=el('path',{d,class:'link'+(active?' active':''),opacity:focus?(active?.75:.09):.3},svg);
   if(e.status!=='Membership'&&e.status!=='Human task evidence')path.setAttribute('stroke-dasharray','3 4');
  });
  heads.forEach(h=>el('text',{x:h.x,y:h.y,class:'lane-label'},svg).textContent=h.label);
  data.nodes.forEach(n=>{
   const p=positions.get(n.id);if(!p)return;const g=el('g',{class:'network-node','data-node':n.id,opacity:focus&&!neighbours.has(n.id)?.7:1},svg);
   el('circle',{cx:p.x,cy:p.y,r:22,fill:'transparent'},g);
   el('circle',{cx:p.x,cy:p.y,r:n.score?16*Math.sqrt(n.score):3,fill:n.score?colour(n):'none','fill-opacity':.55,stroke:n.score?'none':'var(--muted)'},g);
   if(n.id===focus)el('circle',{cx:p.x,cy:p.y,r:20,fill:'none',stroke:'var(--ink)','stroke-width':1},g);
   const lines=words(n.label,p.labelWidth),labelX=n.type==='family'?p.x-23:p.x+23;const label=el('text',{x:labelX,y:p.y-(lines.length-1)*7+4,'text-anchor':n.type==='family'?'end':'start'},g);
   lines.forEach((line,i)=>el('tspan',{x:labelX,dy:i?14:0},label).textContent=line);
   el('title',{},g).textContent=`${n.label} · ${n.score.toFixed(3)} · ${n.degree} recorded links`;
   g.addEventListener('click',()=>{choose(focus===n.id?'':n.id);});
  });
  host.replaceChildren(svg);root.querySelector('[data-count]').textContent=`${positions.size} of ${data.nodes.length} nodes visible · ${linkCount} of ${data.edges.length} recorded links · Solid: membership / task evidence; dotted: conditional / indirect / unresolved / proposed`;
 }
 function addLink(parent,label,kind){
  const a=document.createElement('a');a.textContent=label;a.href=route(kind);parent.append(a);
 }
 function detail(){
  const panel=root.querySelector('[data-detail]');panel.replaceChildren();
  if(!focus){const p=document.createElement('p');p.textContent='Select a node in the diagram or use “Inspect a node” to read its connections and evidence.';panel.append(p);return;}
  const n=map.get(focus);
  const h=document.createElement('h2');h.textContent=n.label;panel.append(h);
  const score=document.createElement('p');score.className='evidence-selection-score';score.textContent=`Centrality ${n.score.toFixed(3)} · ${n.degree} recorded links`;panel.append(score);
  const d=document.createElement('p');d.textContent=n.detail;panel.append(d);
  if(n.type==='emotion'){
   const routes=document.createElement('nav');routes.className='evidence-node-routes';routes.setAttribute('aria-label','Follow '+n.label);
   addLink(routes,'Signal record','record');addLink(routes,'Biological entry','biology');
   addLink(routes,'Fluid','fluid');if(signals[signal]?.chronic)addLink(routes,'Chronic','chronic');
   panel.append(routes);
  }
  if(n.review){
   const block=document.createElement('dl');
   const rows=[['When belonging is involved',n.review.membership],['Possible pressure reduction',n.review.pressure],['Question about Return',n.review.return_question]];
   rows.forEach(([label,value])=>{const dt=document.createElement('dt');dt.textContent=label;const dd=document.createElement('dd');dd.textContent=value;block.append(dt,dd);});
   panel.append(block);
  }
  if(n.type==='emotion'){
   const routes=document.createElement('nav');routes.className='evidence-node-routes';routes.setAttribute('aria-label','Recovery and Return questions');
   addLink(routes,'Recruitment and recovery','recovery');addLink(routes,'Examine Return in Model 2','return');panel.append(routes);
  }
  const heading=document.createElement('h3');heading.textContent='Recorded connections';panel.append(heading);
  const es=data.edges.filter(e=>e.a===focus||e.b===focus);
  if(!es.length){const p=document.createElement('p');p.textContent='No chemical link is assigned here. Zero centrality does not establish the absence of a biological role.';panel.append(p);}
  es.forEach(e=>{
   const other=map.get(e.a===focus?e.b:e.a);const item=document.createElement('div');item.className='edge-record';
   const b=document.createElement('button');b.className='node-link';b.type='button';b.textContent=other.label+(visible.has(other.type)?'':' (hidden layer)');b.onclick=()=>{choose(other.id);selected.focus({preventScroll:true});};item.append(b);
   const status=document.createElement('span');status.className='edge-status';status.textContent=e.status;item.append(status);
   const p=document.createElement('p');p.textContent=e.detail;item.append(p);
   if(e.sources.length){const links=document.createElement('div');links.className='evidence-links';e.sources.forEach(s=>{const a=document.createElement('a');a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent=s.title;links.append(a);});item.append(links);}
   panel.append(item);
  });
 }
 root.querySelectorAll('[data-layer]').forEach(input=>input.addEventListener('change',()=>{if(input.checked)visible.add(input.dataset.layer);else visible.delete(input.dataset.layer);draw();detail();}));
 selected.addEventListener('change',()=>choose(selected.value));
 addEventListener('hashchange',()=>{let id='';try{id=decodeURIComponent(location.hash.slice(1));}catch(_){}if(map.has(id)){focus=id;selected.value=id;syncContext(true);draw();detail();}});
 selected.value=focus;detail();
 new ResizeObserver(draw).observe(root.querySelector('[data-plot]'));draw();
 root.dataset.ready='true';
})();
