from pathlib import Path
import json, re, html as H
from components import intro,objectives,contents,navigation,STYLE,action_button,back_link
ROOT=Path(__file__).parent
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
TITLES={1:'Obiectul de studiu și metodologia microeconomiei',2:'Cererea și oferta. Echilibrul și dezechilibrul pieței',3:'Elasticitatea cererii și ofertei',4:'Teoria comportamentului consumatorului',5:'Teoria producției',6:'Costurile de producție',7:'Maximizarea profitului și pragul de rentabilitate al firmei',8:'Comportamentul firmelor pe piața cu concurență perfectă',9:'Comportamentul firmelor pe piața de monopol',10:'Comportamentul firmelor pe piața cu concurență monopolistică',11:'Comportamentul firmelor pe piața oligopolistă'}
def save(n,**data):
    data.update(number=n,title=TITLES[n]);(DATA/f'{n}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
def pairs(text):
    return [line.split('|',1) for line in text.strip().splitlines() if line.strip()]
def table(headers,rows):return {'headers':headers,'rows':rows}
def problem(title,condition,requirements,steps,conclusion,tables=None,charts=None):
    return dict(title=title,condition=condition,requirements=requirements,steps=steps,conclusion=conclusion,tables=tables or [],charts=charts or [])
def new(title,condition,requirements,hints,question,answer):
    return dict(title=title,condition=condition,requirements=requirements,hints=hints,question=question,answer=answer)
def test(q,options,answer):return dict(q=q,options=options.split('|'),answer=answer)
def graph(title,xlabel,ylabel,series,xmax=None,ymax=None):
    return dict(title=title,xlabel=xlabel,ylabel=ylabel,series=series,xmax=xmax,ymax=ymax)
def line(label,points,color='#1080E4',dash=False):return dict(label=label,points=points,color=color,dash=dash)
def fmt(t):
    t=str(t).replace('ş','ș').replace('ţ','ț').replace('Ş','Ș').replace('Ţ','Ț')
    t=re.sub(r'\b(Q|MU|TU|AP|MP)\s+([dsxykl])\b',r'\1\2',t)
    for base,index in [('MRTS','lk'),('MRS','xy'),('MU','x'),('MU','y'),('TU','x'),('TU','y'),('MP','l'),('MP','k'),('AP','l'),('AP','k'),('CO','x'),('CO','y'),('Q','da'),('Q','sa'),('Q','d'),('Q','s'),('Q','x'),('Q','y'),('Q','c'),('Q','m'),('Q','r'),('P','x'),('P','y'),('P','a'),('P','b'),('P','c'),('P','v'),('P','r'),('Q','a'),('Q','b'),('E','d'),('E','s'),('E','i'),('E','xy')]:
        t=re.sub(r'\b'+base+index+r'\b',base+'<sub>'+index+'</sub>',t)
    t=re.sub(r'\b(MR|MC|TR|TC|VC|FC|TU|MU|AP|MP|ATC|AVC|AFC|[QPKLR])([0123])\b',r'\1<sub>\2</sub>',t)
    t=re.sub(r'\^([234])',r'<sup>\1</sup>',t)
    return t
def p(t):return '<p style="margin:0 0 12px;max-width:75ch;">'+fmt(t)+'</p>'
def list_html(items):return '<ol style="padding-left:24px;margin:8px 0 16px;">'+''.join('<li style="margin-bottom:6px;">'+fmt(x)+'</li>' for x in items)+'</ol>'
def h3(t):return '<h3 style="font-size:20px;line-height:1.4;color:#123B5D;margin:0 0 12px;">'+fmt(t)+'</h3>'
def card(t):return '<div style="box-sizing:border-box;min-width:0;padding:20px 22px;border:1px solid #E2E8EF;border-radius:12px;margin:0 0 16px;background:#FFFFFF;">'+t+'</div>'
def green(t):return '<div style="padding:12px 16px;border-left:5px solid #3F8F1F;background:#F0F8EC;border-radius:8px;margin:12px 0;">'+t+'</div>'
def details(title,body,answer=False):return '<details style="border:1px solid #E2E8EF;border-radius:12px;margin:0 0 12px;min-width:0;'+('background:#F0F8EC;' if answer else '')+'"><summary style="cursor:pointer;padding:14px 16px;font-size:18px;font-weight:700;line-height:1.4;min-height:44px;box-sizing:border-box;">'+fmt(title)+'</summary><div style="padding:4px 16px 16px;min-width:0;">'+body+'</div></details>'
def tbl(t):
    cell='padding:12px 14px;border:1px solid #E2E8EF;text-align:left;vertical-align:top;'
    return '<div style="width:100%;max-width:100%;overflow-x:auto;margin:12px 0 20px;" tabindex="0" role="region" aria-label="Tabel"><table style="border-collapse:collapse;width:100%;font-size:16px;line-height:1.45;"><thead><tr>'+''.join('<th scope="col" style="'+cell+'background:#F6F8FB;">'+fmt(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td style="'+cell+'">'+fmt(x)+'</td>' for x in r)+'</tr>' for r in t['rows'])+'</tbody></table></div>'
def svg(g):
    pts=[pt for s in g['series'] for pt in s['points']]
    xmax=g.get('xmax') or max(x for x,y in pts)*1.1 or 1;ymax=g.get('ymax') or max(y for x,y in pts)*1.15 or 1
    xmin=min(0,min(x for x,y in pts));ymin=min(0,min(y for x,y in pts))
    X=lambda x:70+(x-xmin)/(xmax-xmin)*560
    Y=lambda y:330-(y-ymin)/(ymax-ymin)*280
    s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 410" role="img" aria-label="'+H.escape(g['title'],quote=True)+'" style="display:block;width:100%;max-width:720px;height:auto;font:16px Arial;color:#24313D;">'
    s+='<title>'+H.escape(g['title'])+'</title><rect width="720" height="410" fill="#FFFFFF"/>'
    for i in range(5):
        x=xmin+(xmax-xmin)*i/4;y=ymin+(ymax-ymin)*i/4
        s+=f'<path d="M {X(x):.2f} 50 V 330 M 70 {Y(y):.2f} H 630" stroke="#E2E8EF" fill="none"/>'
        if not g.get('schematic'):
            s+=f'<text x="{X(x):.2f}" y="354" text-anchor="middle">{x:.0f}</text><text x="60" y="{Y(y)+5:.2f}" text-anchor="end">{y:.0f}</text>'
    s+='<path d="M70 40 V330 H650" fill="none" stroke="#24313D" stroke-width="2"/>'
    s+=f'<text x="360" y="388" text-anchor="middle">{H.escape(g["xlabel"])}</text><text x="18" y="30">{H.escape(g["ylabel"])}</text>'
    for series in g['series']:
        points=' '.join(f'{X(x):.2f},{Y(y):.2f}' for x,y in series['points'])
        s+=f'<polyline points="{points}" fill="none" stroke="{series["color"]}" stroke-width="3"'+(' stroke-dasharray="8 5"' if series.get('dash') else '')+'/>'
        for x,y in series['points']:
            s+=f'<circle cx="{X(x):.2f}" cy="{Y(y):.2f}" r="3" fill="{series["color"]}"/>'
    s+='</svg>'
    legend='<div style="font-size:16px;line-height:1.45;">'+''.join('<span style="display:inline-block;border-left:5px solid '+x['color']+';padding-left:8px;margin:4px 16px 4px 0;">'+fmt(x['label'])+(' · linie întreruptă' if x.get('dash') else '')+'</span>' for x in g['series'])+'</div>'
    return h3(g['title'])+'<div style="overflow-x:auto;max-width:100%;"><div style="min-width:720px;">'+s+'</div></div>'+legend
def render(n,output_root=None):
    d=json.loads((DATA/f'{n}.json').read_text());assert len(d['new'])==10
    titles=['Obiectivele seminarului','Bazele teoretice ale seminarului','Formule principale și algoritmi','Exerciții și probleme rezolvate','Probleme pentru rezolvare','Subiecte de recapitulare','Concluzii esențiale','Materiale seminarului']
    root='<div data-course-seminar="'+str(n)+'" lang="ro" style="max-width:1050px;margin:0 auto;padding:12px;box-sizing:border-box;font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.6;color:#24313D;background:#FFFFFF;overflow-wrap:break-word;">'
    root+='<style>'+STYLE+'[data-course-seminar] sub,[data-course-seminar] sup{font-size:75%;line-height:0}[data-course-seminar] :focus-visible{outline:3px solid #1F6388;outline-offset:3px}[data-course-seminar] *{box-sizing:border-box}[data-course-seminar] p:last-child{margin-bottom:0!important}</style>'
    root+='<div data-course-header="compact" style="background:linear-gradient(135deg,#123B5D,#1F6388);color:#FFFFFF;padding:16px 20px;border-radius:12px;margin-bottom:24px;"><div style="font-size:14px;line-height:1.5;letter-spacing:1.2px;text-transform:uppercase;margin:0 0 6px;">Microeconomie · ASEM</div><h1 style="margin:0;font-size:24px!important;font-weight:700;line-height:1.3;color:#FFFFFF;">Seminarul '+str(n)+' — '+d['title']+'</h1></div>'
    root+=intro(fmt(d['description']))
    root+=contents(titles,h3)
    sections=[]
    sections.append(objectives(d['objectives'],fmt))
    from interactive import widget
    sections.append(''.join(card(h3(t)+''.join(p(x) for x in paragraphs)) for t,paragraphs in d['theory'])+''.join(card(svg(g)) for g in d.get('graphs',[]))+widget(n,d.get('model_fallback')))
    sections.append((details('Notații și unități',tbl(table(['Simbol','Semnificație'],d['notation']))) if d.get('notation') else '')+tbl(table(['Instrument','Cum îl folosim'],d['formulas'])))
    solved=''
    for i,pr in enumerate(d['solved'],1):
        body=h3('Problemă')+p(pr['condition'])
        for t in pr.get('tables',[]):body+=tbl(t)
        body+=h3('Cerințe')+list_html(pr['requirements'])+h3('Indicații pentru rezolvare')+p(pr.get('hint','Identificați mărimile cunoscute. Alegeți relația potrivită pentru fiecare cerință. Verificați rezultatul în condițiile problemei.'))
        body+=h3('Rezolvare')+list_html(pr['steps'])
        for t in pr.get('result_tables',[]):body+=tbl(t)
        for g in pr.get('charts',[]):body+=svg(g)
        if pr.get('check'):body+=h3('Verificarea rezultatului')+p(pr['check'])
        body+=green(h3('Concluzie economică')+p(pr['conclusion']))
        if pr.get('practical'):body+=card(h3('Exemplu practic')+p(pr['practical']))
        solved+=details(f'{i}. {pr["title"]}',body)
    sections.append(solved)
    sections.append(''.join(details(f'{i}. {pr["title"]}',h3('Problemă')+p(pr['condition'])+h3('Cerințe')+list_html(pr['requirements'])+h3('Indicații pentru rezolvare')+p(pr['hints'])+h3('Concluzie economică cerută')+p(pr['question'])) for i,pr in enumerate(d['new'],1)))
    recap=h3('Întrebări de verificare')
    for i,(q,a) in enumerate(d['questions'],1):recap+=card(p(f'<strong>{i}. {q}</strong>')+details('Vezi răspunsul și explicația',p(a),True))
    recap+=h3('Enunțuri adevărat–fals')
    for i,(q,a) in enumerate(d['tf'],1):recap+=card(p(f'<strong>{i}. {q}</strong>')+details('Vezi răspunsul și explicația',p(a),True))
    recap+=h3('Teste-grilă')
    for i,t in enumerate(d['tests'],1):
        opts='<ol type="a" style="padding-left:24px;">'+''.join('<li style="margin-bottom:6px;">'+fmt(o)+'</li>' for o in t['options'])+'</ol>'
        recap+=card(p(f'<strong>{i}. {t["q"]}</strong>')+''.join(tbl(tb) for tb in t.get('tables',[]))+''.join(svg(g) for g in t.get('charts',[]))+opts+details('Vezi răspunsul și explicația',p(t['answer']),True))
    sections.append(recap)
    sections.append(green(''.join(p(x) for x in d['conclusions'])))
    sections.append('')
    for i,(title,body) in enumerate(zip(titles,sections),1):
        root+=f'<section id="s{i}" style="margin:32px 0;min-width:0;"><h2 style="font-size:24px;line-height:1.3;color:#123B5D;margin:0 0 16px;">{i}. {title}</h2>'
        if i in (4,5,6):root+='<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">'+action_button('Deschide toate',True,True)+action_button('Închide toate',False)+'</div>'
        root+=body+back_link()+'</section>'
    root+=navigation(n,TITLES)
    root+='<script>(function(){const r=document.currentScript.closest("[data-course-seminar]");r.querySelectorAll("button[data-expand]").forEach(function(b){b.addEventListener("click",function(){b.closest("section").querySelectorAll("details").forEach(function(d){d.open=b.dataset.expand==="true";});});});})();</script></div>'
    out=(Path(output_root) if output_root is not None else ROOT/'output')/'[1] Fișiere HTML ale cursului pentru încărcare pe Moodle';out.mkdir(parents=True,exist_ok=True)
    f=out/f'{n}. Seminarul - {d["title"]}.html';f.write_text('<!DOCTYPE html><html lang="ro"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seminarul '+str(n)+' — '+d['title']+'</title></head><body style="margin:0;">'+root+'</body></html>')
    return f
