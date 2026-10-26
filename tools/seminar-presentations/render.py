from pathlib import Path
import html,re,base64,math,json
ROOT=Path(__file__).parent
ASSET=ROOT/'assets'
C={'ink':'#123B5D','text':'#24313D','muted':'#556374','blue':'#1080E4','orange':'#FF650B','green':'#3F8F1F','border':'#E2E8EF','soft':'#F6F8FB'}
def fmt(s):
 s=html.escape(str(s));s=re.sub(r'\b(Q|MU|TU|AP|MP)\s+([dsxykl])\b',r'\1\2',s)
 for base,index in [('MRTS','lk'),('MRS','xy'),('MU','x'),('MU','y'),('MP','l'),('MP','k'),('AP','l'),('AP','k'),('Q','d'),('Q','s'),('Q','x'),('Q','y'),('P','x'),('P','y'),('E','d'),('E','s')]:s=re.sub(r'\b'+base+index+r'\b',base+'<sub>'+index+'</sub>',s)
 s=re.sub(r'\b(MR|MC|TR|TC|[QPR])([0123])\b',r'\1<sub>\2</sub>',s);s=re.sub(r'\^([234])',r'<sup>\1</sup>',s)
 return s
def icon(name):
 f=ASSET/name
 return 'data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()
def pictogram(kind):
 paths={
 'clock':'<circle cx="32" cy="32" r="23"/><path d="M32 16v17l12 8"/>',
 'wallet':'<path d="M8 18h48v36H8zM8 18l34-9v9M39 31h17v13H39z"/><circle cx="46" cy="37" r="1"/>',
 'chart':'<path d="M10 8v46h46M16 42l12-18 11 9 17-20"/>',
 'factory':'<path d="M8 54V30l16 8V24l16 11V12h12v42zM18 46h4m11 0h4m10 0h4"/>',
 'check':'<circle cx="32" cy="32" r="23"/><path d="M19 32l9 9 18-20"/>',
 'switch':'<path d="M10 20h40l-9-9m9 9l-9 9M54 44H14l9 9m-9-9l9-9"/>',
 'tag':'<path d="M8 12h24l24 24-20 20L8 28z"/><circle cx="20" cy="23" r="3"/>',
 'person':'<circle cx="32" cy="19" r="10"/><path d="M13 56v-8c0-21 38-21 38 0v8M24 43v13m16-13v13"/>',
 'pin':'<path d="M32 57S11 36 11 23a21 21 0 1142 0c0 13-21 34-21 34z"/><circle cx="32" cy="23" r="7"/>',
 'box':'<path d="M9 19l23-11 23 11v28L32 59 9 47zM9 19l23 12 23-12M32 31v28"/>',
 'cup':'<path d="M10 24h34v21c0 15-34 15-34 0zM44 27h8c12 0 12 17 0 17h-8M15 15v-7m13 7v-7m13 7v-7"/>',
 'heart':'<path d="M32 54L10 33C-6 12 22 1 32 19 43 1 70 12 54 33z"/>'}
 return '<svg viewBox="0 0 64 64" aria-hidden="true" style="width:94px;height:94px;fill:none;stroke:#123B5D;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;margin-bottom:20px;">'+paths.get(kind,paths['chart'])+'</svg>'
CONTEXT_ICONS={1:['clock','switch','check'],2:['wallet','tag','factory'],3:['switch','wallet','clock'],4:['heart','tag','wallet'],5:['person','factory','box'],6:['factory','box','chart'],7:['tag','factory','chart'],8:['person','tag','chart'],9:['factory','chart','tag'],10:['pin','cup','switch'],11:['factory','factory','chart']}
def cards(rows,cls='',icons=None):
 return '<div class="cards '+cls+'">'+''.join('<article class="card"><div class="accent"></div>'+(pictogram(icons[i]) if icons else '')+'<h2>'+fmt(a)+'</h2><p>'+fmt(b)+'</p></article>' for i,(a,b) in enumerate(rows))+'</div>'
def svg_graph(n):
 blue=C['blue'];orange=C['orange'];gray=C['muted'];green=C['green'];seq=lambda a,b,f,step=0.5:[(a+i*step,f(a+i*step)) for i in range(int((b-a)/step)+1)]
 cfg={
1:(10,55,'X · unități','Y · unități',[('CPP',[(0,50),(10,0)],blue,False)],(4,30),None),
2:(120,110,'Q · produse pe zi','P · u.m./produs',[('Cerere',[(0,100),(100,0)],blue,False),('Ofertă',[(0,10),(120,70)],orange,True)],(60,40),None),
3:(40,22,'Q · produse pe perioadă','P · u.m./produs',[('Cerere',[(0,20),(40,0)],blue,False)],(20,10),None),
4:(6.5,13,'X · unități','Y · unități',[('Buget',[(0,12),(6,0)],blue,False),('TU = 18',seq(1.5,6,lambda x:18/x,0.05),orange,True)],(3,6),None),
5:(4.4,35,'L · lucrători','TP · pâini/coacere',[('Producție totală',[(0,0),(1,20),(2,28),(3,30),(4,30)],blue,False),('Capacitatea tăvii',[(0,30),(4.4,30)],gray,True)],(3,30),None),
6:(40,30,'Q · produse pe zi','Lei pe produs',[('ATC',seq(4,40,lambda q:100/q+5),blue,False),('MC = 5',[(0,5),(40,5)],orange,True)],(20,10),None),
7:(40,2400,'Q · produse','Lei pentru întregul lot',[('TR',[(0,0),(40,2000)],blue,False),('TC',seq(0,40,lambda q:100+10*q+q*q),orange,True)],(20,1000),(20,700)),
8:(20,60,'Q · produse','Lei pe produs',[('MC',[(0,10),(20,50)],orange,False),('AVC',[(0,10),(20,30)],gray,True),('P = 20',[(0,20),(20,20)],blue,False)],(5,20),None),
9:(50,110,'Q · produse','Lei pe produs',[('Cerere',[(0,100),(50,0)],blue,False),('MR',[(0,100),(25,0)],orange,True),('MC = 20',[(0,20),(50,20)],gray,False)],(20,60),(20,20)),
10:(35,100,'Q · produse','Lei pe produs',[('Cerere',[(0,80),(35,45)],blue,False),('MR',[(0,80),(35,10)],gray,True),('MC',[(0,20),(35,90)],orange,False)],(15,65),(15,50)),
11:(60,65,'Cantitatea firmei 1','Cantitatea firmei 2',[('Reacția firmei 1',[(0,60),(30,0)],blue,False),('Reacția firmei 2',[(0,30),(60,0)],orange,True)],(20,20),None)
 }[n]
 xmax,ymax,xlabel,ylabel,series,point,second=cfg;X=lambda x:110+x/xmax*950;Y=lambda y:540-y/ymax*420
 # Round only grid labels; marked economic coordinates are always exact.
 ticksx={1:[0,5,10],2:[0,60,120],3:[0,20,40],4:[0,3,6],5:[0,2,4],6:[0,20,40],7:[0,20,40],8:[0,10,20],9:[0,20,40],10:[0,15,30],11:[0,20,40,60]}[n]
 ticksy={1:[0,25,50],2:[0,40,80],3:[0,10,20],4:[0,6,12],5:[0,15,30],6:[0,10,20,30],7:[0,1000,2000],8:[0,20,40,60],9:[0,20,60,100],10:[0,50,100],11:[0,20,40,60]}[n]
 s='<svg viewBox="0 0 1200 680" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Graficul seminarului '+str(n)+'" style="width:100%;height:auto;font:36px Arial;overflow:visible;">'
 for v in ticksx:
  s+=f'<path d="M{X(v)} 100 V540" stroke="#E2E8EF" stroke-width="2"/><text x="{X(v)}" y="592" text-anchor="middle" fill="#24313D">{v}</text>'
 for v in ticksy:
  s+=f'<path d="M110 {Y(v)} H1080" stroke="#E2E8EF" stroke-width="2"/><text x="92" y="{Y(v)+12}" text-anchor="end" fill="#24313D">{v}</text>'
 s+='<path d="M110 85 V540 H1090" fill="none" stroke="#123B5D" stroke-width="4"/>'
 s+=f'<text x="110" y="48" fill="#123B5D">{html.escape(ylabel)}</text><text x="600" y="650" text-anchor="middle" fill="#123B5D">{html.escape(xlabel)}</text>'
 for label,pts,color,dash in series:
  s+='<polyline points="'+' '.join(f'{X(x):.2f},{Y(y):.2f}' for x,y in pts)+'" fill="none" stroke="'+color+'" stroke-width="6"'+(' stroke-dasharray="14 10"' if dash else '')+'/>'
 px,py=point;s+=f'<path d="M{X(px)} 540 V{Y(py)} H110" fill="none" stroke="{green}" stroke-width="3" stroke-dasharray="7 7"/>'
 if second:
  sx,sy=second;s+=f'<path d="M{X(px)} {Y(py)} L{X(sx)} {Y(sy)}" stroke="{green}" stroke-width="5"/><circle cx="{X(sx)}" cy="{Y(sy)}" r="10" fill="{green}" stroke="#FFFFFF" stroke-width="3"/>'
 s+=f'<circle cx="{X(px)}" cy="{Y(py)}" r="12" fill="{green}" stroke="#FFFFFF" stroke-width="4"/>'
 s+=f'<text x="{X(px)+22}" y="{Y(py)-22}" font-weight="700" fill="#123B5D">({px}; {py})</text></svg>'
 legend='<div class="legend">'+''.join('<span><i style="background:'+color+';"></i>'+fmt(label)+(' · întreruptă' if dash else '')+'</span>' for label,_,color,dash in series)+'</div>'
 return s+legend

CSS='''*{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:#24313D;background:#fff} .slide{position:relative;width:1920px;height:1080px;padding:72px 80px 68px;background-color:#f8fbfd;background-image:linear-gradient(#123b5d07 1px,transparent 1px),linear-gradient(90deg,#123b5d07 1px,transparent 1px);background-size:40px 40px;overflow:hidden}.meta{font-size:26px;letter-spacing:3px;text-transform:uppercase;color:#556374;margin-bottom:20px}h1{font-size:68px;line-height:1.12;letter-spacing:-1px;color:#123B5D;margin:0 0 38px;font-weight:700;max-width:1730px}h2{font-size:48px;line-height:1.18;color:#123B5D;margin:0 0 22px}p{font-size:46px;line-height:1.35;margin:0}.footer{position:absolute;left:80px;right:80px;bottom:28px;display:flex;justify-content:space-between;font-size:24px;color:#556374}.lead{max-width:1640px;font-size:46px;margin-bottom:48px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}.card{position:relative;background:white;border:2px solid #E2E8EF;border-radius:24px;padding:38px 32px;min-width:0;box-shadow:0 10px 25px #123b5d08}.accent{width:72px;height:8px;border-radius:8px;background:#1080E4;margin-bottom:30px}.card:nth-child(2) .accent{background:#FF650B}.card:nth-child(3) .accent{background:#3F8F1F}.card p{font-size:48px}.cover h1{font-size:74px;max-width:1180px}.cover .hook{font-size:48px;color:#123B5D;font-weight:700;max-width:1100px;line-height:1.3}.cover .promise{font-size:39px;line-height:1.4;max-width:1060px;margin-top:28px}.cover-visual{position:absolute;right:68px;top:310px;width:490px;display:flex;align-items:center;flex-direction:column;gap:10px}.cover-visual img{width:260px;height:260px;object-fit:contain}.cover-visual .arrow{font-size:64px;line-height:1;color:#123B5D}.cover .route{position:absolute;left:80px;bottom:120px;display:flex;gap:14px}.route span{font-size:30px;line-height:1.4;padding:14px 24px;background:#fff;border:2px solid #E2E8EF;border-radius:50px;color:#123B5D}.cover .meta{margin-bottom:28px}.process-flow{display:grid;grid-template-columns:1fr 58px 1fr 58px 1fr;gap:18px;align-items:stretch}.process-flow .arrow{align-self:center;font-size:64px;color:#123B5D}.process-flow .card{padding:38px 28px}.equation{background:#fff;border:2px solid #E2E8EF;border-left:12px solid #1080E4;border-radius:24px;padding:46px 44px;font-size:62px;line-height:1.3;color:#123B5D;font-weight:700;margin:30px 0 40px}.formula-lines{display:grid;grid-template-columns:1fr 1fr;gap:28px}.formula-lines .card p{font-size:42px}.compare{grid-template-columns:1fr 1fr;gap:36px}.compare .card{padding:44px}.compare .card p{font-size:46px}.graph-layout{display:grid;grid-template-columns:1200px 1fr;gap:32px;align-items:center;margin-top:-10px}.graph-panel{background:white;border:2px solid #E2E8EF;border-radius:24px;padding:18px}.graph-side{padding:26px 8px}.graph-side p{font-size:46px;line-height:1.35;margin-bottom:34px}.legend{display:flex;flex-wrap:wrap;gap:16px 30px;font-size:36px;color:#123B5D;padding:0 25px 18px}.legend span{display:flex;align-items:center;gap:10px}.legend i{display:inline-block;width:40px;height:7px}.end-list{display:grid;gap:22px}.end-row{display:flex;gap:28px;align-items:center;padding:26px 32px;background:#fff;border:2px solid #E2E8EF;border-radius:18px;font-size:48px;line-height:1.25}.end-row b{font-size:48px;color:#1080E4}.check{margin-top:34px;color:#123B5D;font-size:39px;line-height:1.35;max-width:1670px}sub,sup{font-size:70%;line-height:0}.native-box{position:absolute;display:flex;align-items:center;white-space:normal;line-height:1.25;overflow:visible}'''

def native_layout(slide):
 rows=[]
 def box(x,y,w,h,text,size=52,bold=False,color='#24313D',bg=None):rows.append(dict(x=x,y=y,w=w,h=h,text=text,size=size,bold=bold,color=color,bg=bg))
 if slide['kind']=='exercise':
  box(80,270,1760,330,slide['condition'],54,bg='#FFFFFF')
  box(80,615,1760,70,'Cerințe',44,True,C['ink'])
  for i,item in enumerate(slide['requirements']):box(110,705+i*110,1700,90,str(i+1)+'. '+item,52)
 else:
  for i,(label,calculation) in enumerate(slide['steps']):
   y=270+i*180;box(80,y,1760,154,'',bg='#FFFFFF');box(112,y+18,1650,44,label,36,True,C['muted']);box(112,y+72,1650,78,calculation,52,True,C['ink'])
  box(80,840,1760,150,slide['conclusion'],42,False,C['ink'],bg='#F0F8EC')
 return rows

def page(deck,slide):
 n=deck['seminar'];kind=slide['kind'];i=slide['number'];body=''
 if kind=='cover':
  body='<h1>'+fmt(deck['title'])+'</h1><div class="hook">'+fmt(slide['hook'])+'</div><p class="promise">'+fmt(slide['promise'])+'</p><div class="cover-visual"><img alt="Consumator" src="'+icon('01_Portofel_consumator_curat.png')+'"><div class="arrow" aria-hidden="true">↓</div><img alt="Producător" src="'+icon('02_Fabrica_producator.png')+'"></div><div class="route"><span>Înțelegem</span><span>Calculăm</span><span>Interpretăm</span></div>'
 elif kind=='context':body='<h1>'+fmt(slide['title'])+'</h1><p class="lead">'+fmt(slide['lead'])+'</p>'+cards(slide['cards'],icons=CONTEXT_ICONS[n])
 elif kind=='concepts':body='<h1>'+fmt(slide['title'])+'</h1>'+cards(slide['cards'])
 elif kind=='flow':body='<h1>'+fmt(slide['title'])+'</h1><div class="process-flow">'+('<div class="arrow" aria-hidden="true">→</div>').join('<article class="card"><div class="accent"></div>'+'<h2>'+fmt(a)+'</h2><p>'+fmt(b)+'</p></article>' for a,b in slide['steps'])+'</div>'
 elif kind=='formula':body='<h1>'+fmt(slide['title'])+'</h1><div class="equation">'+fmt(slide['formula'])+'</div>'+cards([(str(i+1),s) for i,s in enumerate(slide['lines'])],'formula-lines')
 elif kind=='graph':body='<h1>'+fmt(slide['title'])+'</h1><div class="graph-layout"><div class="graph-panel">'+svg_graph(n)+'</div><aside class="graph-side">'+''.join('<p>'+fmt(s)+'</p>' for s in slide['lines'])+'</aside></div>'
 elif kind=='compare':body='<h1>'+fmt(slide['title'])+'</h1>'+cards(slide['cards'],'compare')
 elif kind in ['exercise','solution']:
  body='<h1>'+fmt(slide['title'])+'</h1>'
  for box in native_layout(slide):
   style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;font-size:{size}px;color:{color};'.format(**box)
   if box['bg']:style+='background:'+box['bg']+';border:2px solid #E2E8EF;border-radius:20px;padding:20px 30px;'
   if box['bold']:style+='font-weight:700;'
   body+='<div class="native-box" data-height="'+str(box['h'])+'" style="'+style+'">'+'<span style="display:block;width:100%;">'+fmt(box['text'])+'</span></div>'
 elif kind=='end':body='<h1>'+fmt(slide['title'])+'</h1><div class="end-list">'+''.join('<div class="end-row"><b>'+str(i)+'</b><span>'+fmt(s)+'</span></div>' for i,s in enumerate(slide['points'],1))+'</div><p class="check">'+fmt(slide['check'])+'</p>'
 return '<!DOCTYPE html><html lang="ro"><meta charset="utf-8"><style>'+CSS+'</style><div class="slide '+kind+'"><div class="meta">Microeconomie · ASEM · Seminarul '+str(n)+'</div>'+body+'<footer class="footer"><span>Seminar · Idei esențiale și aplicație</span><span>'+str(i).zfill(2)+' / 10</span></footer></div></html>'
