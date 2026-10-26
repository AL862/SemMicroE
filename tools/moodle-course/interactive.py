def widget(n, fallback=None):
    labels={1:('Alegere pe o frontieră liniară','Cantitatea X',0,10,4),2:('Preț și dezechilibru','Prețul · u.m.',0,60,40),3:('Elasticitate și încasări pe aceeași cerere','Prețul · u.m.',1,19,10),4:('Buget și utilitate: TU = X × Y','Cantitatea X',0,6,3),5:('Producția unei tăvi de pâine','Numărul de angajați',0,4,2),6:('Cost mediu și cost marginal','Cantitatea Q',1,20,10),7:('Cantitate și profit total','Cantitatea Q',0,45,20),8:('Firma concurentă la un preț dat','Prețul pieței · lei',0,50,30),9:('Cantitate și preț de monopol','Cantitatea Q',0,45,20),10:('Alegerea unei firme cu produs diferențiat','Cantitatea Q',0,35,15),11:('Două firme și răspunsurile lor','Cantitatea firmei 1',0,60,20)}
    title,label,lo,hi,val=labels[n]
    button='font:inherit;font-size:16px;padding:10px 16px;min-height:44px;border:1px solid #E2E8EF;border-radius:8px;background:#FFFFFF;color:#123B5D;cursor:pointer;'
    h=f'<div data-model="{n}" style="border:1px solid #E2E8EF;padding:20px 22px;border-radius:12px;margin:24px 0;min-width:0;"><h3 style="font-size:20px;line-height:1.4;color:#123B5D;margin:0 0 16px;">Model interactiv · {title}</h3><p style="margin:0 0 12px;">Modificați valoarea și comparați rezultatul cu explicația. Datele acestui model rămân aceleași în toate comparațiile sale.</p><label style="display:block;margin:12px 0;">{label}: <output data-value style="font-weight:700;">{val}</output><input data-main type="range" min="{lo}" max="{hi}" step="1" value="{val}" style="display:block;width:100%;max-width:100%;min-height:44px;" aria-label="{label}"></label>'
    if n==11:h+='<label style="display:block;margin:12px 0;">Cantitatea firmei 2: <output data-other-value style="font-weight:700;">20</output><input data-other type="range" min="0" max="60" step="1" value="20" style="display:block;width:100%;min-height:44px;" aria-label="Cantitatea firmei 2"></label>'
    names={1:'Reper: X = 4',2:'Echilibru exact',3:'Elasticitate unitară',4:'Coș optim',5:'Limita unei tăvi',6:'Minimul ATC',7:'Profit maxim',8:'Preț cu profit zero',9:'Profit maxim',10:'Profit maxim',11:'Cournot'}
    h+=f'<div style="display:flex;flex-wrap:wrap;gap:8px;"><button type="button" data-reset style="{button}">{names[n]}</button>'
    if n==11:h+=f'<button type="button" data-stack style="{button}">Stackelberg</button><button type="button" data-cartel style="{button}">Cartel cu împărțire egală</button>'
    h+='</div><div data-result aria-live="polite" style="padding:12px 16px;border-left:5px solid #3F8F1F;background:#F0F8EC;border-radius:8px;margin:16px 0;"></div><div style="max-width:100%;overflow-x:auto;" tabindex="0" role="region" aria-label="Grafic interactiv"><div data-plot style="min-width:720px;"></div></div><div data-legend style="font-size:16px;line-height:1.45;margin-top:12px;"></div>'
    if fallback:
        h=h.replace('margin:16px 0;"></div>', 'margin:16px 0;">'+fallback['result']+'</div>')
        h=h.replace('data-plot style="min-width:720px;"></div>', 'data-plot style="min-width:720px;">'+fallback['plot']+'</div>')
        h=h.replace('margin-top:12px;"></div>', 'margin-top:12px;">'+fallback['legend']+'</div>')
    code=r'''
(function(){
 const r=document.currentScript.closest('[data-model]'), n=Number(r.dataset.model), input=r.querySelector('[data-main]'), other=r.querySelector('[data-other]');
 const colors=['#1080E4','#FF650B','#556374','#3F8F1F'];
 function f(x){if(!Number.isFinite(x))return 'nedefinit';if(Math.abs(x-Math.round(x))<1e-8)return String(Math.round(x));for(let d=2;d<=10000;d++){const a=Math.round(x*d);if(Math.abs(a/d-x)<1e-8)return a+'/'+d;}return 'aproximativ '+String(Math.round(x*100)/100).replace('.', ' și ')+' sutimi';}
 const seq=(a,b,step,fn)=>{let out=[];for(let x=a;x<=b+1e-9;x+=step)out.push([x,fn(x)]);return out;};
 function chart(series,point,xname,yname){
  const all=series.flatMap(s=>s[1]).concat(point?[point]:[]), xmax=Math.max(...all.map(p=>p[0]),1)*1.06,ymax=Math.max(...all.map(p=>p[1]),1)*1.12,ymin=Math.min(0,...all.map(p=>p[1]));
  const X=x=>70+x/xmax*560,Y=y=>330-(y-ymin)/(ymax-ymin)*280;
  let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 410" role="img" aria-label="Model economic interactiv" style="width:100%;max-width:720px;height:auto;display:block;font:16px Arial;"><title>Model economic interactiv</title><rect width="720" height="410" fill="#FFFFFF"/>';
  for(let i=0;i<=4;i++){let x=xmax*i/4,y=ymin+(ymax-ymin)*i/4;s+='<path d="M'+X(x)+' 50 V330 M70 '+Y(y)+' H630" stroke="#E2E8EF" fill="none"/><text x="'+X(x)+'" y="354" text-anchor="middle">'+Math.round(x)+'</text><text x="60" y="'+(Y(y)+5)+'" text-anchor="end">'+Math.round(y)+'</text>';}
  s+='<path d="M70 40 V330 H650" fill="none" stroke="#24313D" stroke-width="2"/><text x="360" y="390" text-anchor="middle">'+xname+'</text><text x="18" y="28">'+yname+'</text>';
  series.forEach((item,i)=>{s+='<polyline points="'+item[1].map(p=>X(p[0])+','+Y(p[1])).join(' ')+'" fill="none" stroke="'+colors[i%4]+'" stroke-width="3"'+(i===2?' stroke-dasharray="8 5"':'')+'/>';});
  if(point)s+='<circle cx="'+X(point[0])+'" cy="'+Y(point[1])+'" r="7" fill="#3F8F1F" stroke="#123B5D" stroke-width="2"/>';
  r.querySelector('[data-plot]').innerHTML=s+'</svg>';
  r.querySelector('[data-legend]').innerHTML=series.map((x,i)=>'<span style="display:inline-block;border-left:5px solid '+colors[i%4]+';padding-left:8px;margin:4px 16px 4px 0;">'+x[0]+'</span>').join('')+'<span style="display:inline-block;">● Punctul curent</span>';
 }
 function update(){
  let a=Number(input.value),b=other?Number(other.value):0;r.querySelector('[data-value]').textContent=f(a);if(other)r.querySelector('[data-other-value]').textContent=f(b);
  let text='',s=[],pt=null,xname='Q · unități',yname='Valoare';
  if(n===1){let y=50-5*a;text='Qx = '+f(a)+' și Qy = '+f(y)+'. Încă o unitate X sacrifică 5 unități Y. Resursele și tehnologia rămân constante.';s=[['CPP',[[0,50],[10,0]]]];pt=[a,y];xname='X · unități';yname='Y · unități';}
  if(n===2){let qd=100-a,qs=Math.max(0,-20+2*a);text='P = '+f(a)+' · Qd = '+f(qd)+' · Qs = '+f(qs)+'. '+(qd===qs?'Echilibru.':qd>qs?'Deficit = '+f(qd-qs)+'.':'Exces de ofertă = '+f(qs-qd)+'.');s=[['Cerere',[[0,100],[100,0]]],['Ofertă',[[0,10],[100,60]]],['Preț curent',[[0,a],[100,a]]]];pt=[qd,a];yname='P · u.m.';}
  if(n===3){let q=40-2*a,e=-2*a/q,tr=a*q;text='Q = '+f(q)+' · Ed = '+f(e)+' · TR = '+f(tr)+'. '+(Math.abs(e)===1?'Elasticitate unitară și încasări maxime.':Math.abs(e)>1?'Cerere elastică.':'Cerere inelastică.');s=[['Cerere: Q = 40 − 2P',[[0,20],[40,0]]]];pt=[q,a];yname='P · u.m.';}
  if(n===4){let y=12-2*a,u=a*y;text='I = 120 lei · Px = 20 lei · Py = 10 lei. X = '+f(a)+' și Y = '+f(y)+' · TU = '+f(u)+'. Optim: X = 3 și Y = 6 cu TU = 18.';s=[['Buget',[[0,12],[6,0]]],['Indiferență TU = 18',seq(1.5,6,.1,x=>18/x)]];pt=[a,y];xname='X · unități';yname='Y · unități';}
  if(n===5){let tp=[0,20,28,30,30],mp=a?tp[a]-tp[a-1]:null;text='TP = '+tp[a]+' pâini. AP = '+(a?f(tp[a]/a):'nedefinit la zero angajați')+'. MP = '+(a?mp:'nu există o unitate anterioară')+'. Aceeași tavă are maximum 30 pâini.';s=[['TP',tp.map((q,i)=>[i,q])]];pt=[a,tp[a]];xname='L · angajați';yname='Pâini / coacere';}
  if(n===6){let tc=100+10*a+a*a,atc=tc/a,mc=10+2*a;text='TC = 100 + 10Q + Q². Q = '+a+' · TC = '+f(tc)+' · ATC = '+f(atc)+' · MC punctual = '+f(mc)+'. Minimul ATC este 30 la Q = 10.';s=[['ATC',seq(1,20,.25,q=>100/q+10+q)],['MC',[[0,10],[20,50]]]];pt=[a,atc];yname='Lei / unitate';}
  if(n===7){let tr=50*a,tc=100+10*a+a*a,profit=tr-tc;text='P = 50 · TC = 100 + 10Q + Q². TR = '+f(tr)+' · TC = '+f(tc)+' · Profit = '+f(profit)+'. Maximul este 300 la Q = 20. MR = 50 și MC = '+f(10+2*a)+'.';s=[['TR',[[0,0],[45,2250]]],['TC',seq(0,45,1,q=>100+10*q+q*q)]];pt=[a,tr];yname='Lei';}
  if(n===8){let q=Math.max(0,(a-10)/2),vc=10*q+q*q,profit=a*q-vc-100;text='P = '+a+' · TC = 100 + 10Q + Q². Q optim = '+f(q)+' · Profit = '+f(profit)+'. '+(a<=10?'Oprire: prețul nu depășește pragul de 10 lei.':a<30?'Continuare cu pierdere mai mică decât FC.':a===30?'Profit economic zero.':'Profit economic pozitiv.');s=[['MC',[[0,10],[20,50]]],['AVC',[[0,10],[20,30]]],['P',[[0,a],[20,a]]],['ATC',seq(2,20,.25,q=>100/q+10+q)]];pt=[q,a];yname='Lei / unitate';}
  if(n===9){let p=100-2*a,mr=100-4*a,profit=(p-20)*a-100;text='P = 100 − 2Q · TC = 100 + 20Q. P = '+f(p)+' · MR = '+f(mr)+' · MC = 20 · Profit = '+f(profit)+'. Maximul este 700 la Q = 20 și P = 60.';s=[['Cerere',[[0,100],[45,10]]],['MC',[[0,20],[45,20]]],['MR',[[0,100],[45,-80]]]];pt=[a,p];yname='Lei / unitate';}
  if(n===10){let p=80-a,mc=20+2*a,mr=80-2*a,profit=p*a-(200+20*a+a*a);text='P = 80 − Q · TC = 200 + 20Q + Q². P = '+f(p)+' · MR = '+f(mr)+' · MC = '+f(mc)+' · Profit = '+f(profit)+'. Maxim: Q = 15 și P = 65 și profit = 250.';s=[['Cerere',[[0,80],[35,45]]],['MC',[[0,20],[35,90]]],['MR',[[0,80],[35,10]]]];pt=[a,p];yname='Lei / unitate';}
  if(n===11){if(a+b>90){b=90-a;other.value=b;r.querySelector('[data-other-value]').textContent=f(b);}let p=90-a-b,r1=Math.max(0,30-b/2),r2=Math.max(0,30-a/2);text='P = 90 − Q1 − Q2 · MC = 30 pentru ambele firme. Q total = '+f(a+b)+' · P = '+f(p)+' · Profit 1 = '+f((p-30)*a)+' · Profit 2 = '+f((p-30)*b)+'. Cele mai bune răspunsuri: Q1 = '+f(r1)+' și Q2 = '+f(r2)+'. '+(a===r1&&b===r2?'Ambele sunt răspunsuri optime simultan: Cournot.':'Punctul curent nu este echilibru Cournot.');s=[['Reacția firmei 1',[[0,60],[30,0]]],['Reacția firmei 2',[[0,30],[60,0]]]];pt=[a,b];xname='Firma 1 · unități';yname='Firma 2 · unități';}
  r.querySelector('[data-result]').innerHTML=text.replace(/\b(Q|P)([12dsvxy])\b/g,'$1<sub style="font-size:75%;line-height:0;">$2</sub>');chart(s,pt,xname,yname);
 }
 input.addEventListener('input',update);if(other)other.addEventListener('input',update);
 r.querySelector('[data-reset]').addEventListener('click',function(){input.value=({1:4,2:40,3:10,4:3,5:3,6:10,7:20,8:30,9:20,10:15,11:20})[n];if(other)other.value=20;update();});
 if(n===11){r.querySelector('[data-stack]').addEventListener('click',function(){input.value=30;other.value=15;update();});r.querySelector('[data-cartel]').addEventListener('click',function(){input.value=15;other.value=15;update();});}update();
})();
'''
    return h+'<script>'+code+'</script></div>'
