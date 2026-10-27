"""Build the course bibliography, glossary exports and searchable teacher solutions."""
from pathlib import Path
import argparse,json,html,re,sys,tarfile,io,gzip,hashlib,time
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
COURSE_FOLDER='[5] Materiale pentru curs'
TEACHER_FOLDER='[6] Materiale și informații pentru profesor'
INK='#123B5D';TEXT='#24313D';BORDER='#E2E8EF';SOFT='#F6F8FB'
def esc(s):return html.escape(str(s),quote=True)
def fmt(s):
    s=esc(html.unescape(str(s)))
    for tag in ['strong','em','b','i','sub','sup']:
        s=s.replace('&lt;'+tag+'&gt;','<'+tag+'>').replace('&lt;/'+tag+'&gt;','</'+tag+'>')
    for base,index in [('MRTS','lk'),('MRS','xy'),('MU','x'),('MU','y'),('MP','l'),('MP','k'),('Q','d'),('Q','s'),('Q','x'),('Q','y'),('Q','m'),('Q','a'),('Q','b'),('P','x'),('P','y'),('P','a'),('P','b'),('P','c'),('P','v'),('E','d'),('E','s'),('E','i'),('E','xy')]:
        s=re.sub(r'\b'+base+index+r'\b',base+'<sub>'+index+'</sub>',s)
    s=re.sub(r'\b(MR|MC|TR|TC|VC|FC|TU|MU|AP|MP|ATC|AVC|AFC|[QPKLR])([0123])\b',r'\1<sub>\2</sub>',s)
    return re.sub(r'\^([234])',r'<sup>\1</sup>',s)
def p(s):return '<p style="margin:0 0 12px;max-width:75ch;">'+fmt(s)+'</p>'
def h(s,level=3):return f'<h{level} style="color:{INK};font-size:{24 if level==2 else 20}px;line-height:1.4;margin:0 0 12px;">'+fmt(s)+f'</h{level}>'
def box(body,green=False):return '<div style="padding:16px 20px;background:'+('#F0F8EC;border-left:5px solid #3F8F1F' if green else SOFT)+';border-radius:12px;margin:12px 0;">'+body+'</div>'
def ol(items):return '<ol style="padding-left:24px;margin:0 0 16px;">'+''.join('<li style="margin:0 0 8px;">'+fmt(x)+'</li>' for x in items)+'</ol>'
def records_card(id,n,kind,title,body,plain):
    search=' '.join([id,str(n),kind,title,plain])
    return '<details class="record" id="'+id+'" data-seminars="'+str(n)+'" data-kind="'+kind+'" data-search="'+esc(search)+'" style="border:1px solid '+BORDER+';border-radius:12px;margin:0 0 12px;background:#FFFFFF;min-width:0;"><summary style="padding:14px 16px;cursor:pointer;font-size:18px;font-weight:700;line-height:1.4;min-height:48px;color:'+INK+';">'+fmt(title)+'</summary><div style="padding:4px 16px 16px;min-width:0;">'+body+'</div></details>'
def controls(titles,kinds):
    field='font:inherit;font-size:16px;line-height:1.45;padding:10px 12px;min-height:48px;width:100%;border:1px solid '+BORDER+';border-radius:8px;background:#FFFFFF;color:'+TEXT+';'
    out='<div data-controls style="display:none;padding:16px;border:1px solid '+BORDER+';border-radius:12px;background:'+SOFT+';margin:24px 0;"><div style="display:flex;flex-wrap:wrap;gap:12px;"><label style="flex:2 1 240px;min-width:0;">Căutare<input data-search-input type="search" placeholder="Cuvânt sau identificator" style="'+field+'"/></label><label style="flex:1 1 240px;min-width:0;">Seminar<select data-seminar style="'+field+'"><option value="">Toate seminarele</option>'+''.join('<option value="'+str(n)+'">'+str(n)+'. '+esc(t)+'</option>' for n,t in titles.items())+'</select></label>'
    if kinds:out+='<label style="flex:1 1 200px;min-width:0;">Tip<select data-kind-select style="'+field+'"><option value="">Toate tipurile</option>'+''.join('<option value="'+k+'">'+esc(v)+'</option>' for k,v in kinds.items())+'</select></label>'
    out+='</div><div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0;">'
    for attr,label in [('data-reset','Resetează filtrele'),('data-open','Deschide rezultatele'),('data-close','Închide rezultatele')]:out+='<button type="button" '+attr+' style="font:inherit;font-size:16px;min-height:48px;padding:10px 16px;border:1px solid '+BORDER+';border-radius:12px;background:#FFFFFF;color:'+INK+';cursor:pointer;">'+label+'</button>'
    return out+'</div><p data-status role="status" aria-live="polite" style="font-size:16px;margin:12px 0 0;"></p><p data-empty hidden style="font-size:18px;margin:12px 0 0;">Nu există rezultate. Schimbați cuvântul sau filtrele.</p></div>'
SCRIPT='''<script>(function(){const root=document.currentScript.closest('[data-material]');
const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
const cards=[...root.querySelectorAll('.record')].map(el=>({el,text:norm(el.dataset.search),seminars:el.dataset.seminars.split(' ')}));
const controls=root.querySelector('[data-controls]');controls.style.display='block';
const input=root.querySelector('[data-search-input]'),sem=root.querySelector('[data-seminar]'),kind=root.querySelector('[data-kind-select]');
function apply(){const words=norm(input.value.trim()).split(/\\s+/).filter(Boolean);let count=0;
for(const item of cards){const visible=(!sem.value||item.seminars.includes(sem.value))&&(!kind||!kind.value||item.el.dataset.kind===kind.value)&&words.every(w=>item.text.includes(w));item.el.hidden=!visible;if(visible)count++;}
root.querySelector('[data-status]').textContent=count+' din '+cards.length+' rezultate';root.querySelector('[data-empty]').hidden=count!==0;}
input.addEventListener('input',apply);sem.addEventListener('change',apply);if(kind)kind.addEventListener('change',apply);
root.querySelector('[data-reset]').addEventListener('click',()=>{input.value='';sem.value='';if(kind)kind.value='';apply();input.focus();});
root.querySelector('[data-open]').addEventListener('click',()=>cards.forEach(x=>{if(!x.el.hidden)x.el.open=true;}));
root.querySelector('[data-close]').addEventListener('click',()=>cards.forEach(x=>{if(!x.el.hidden)x.el.open=false;}));apply();})();</script>'''
def page(title,intro,body,titles,kinds=None):
    root='<div data-material lang="ro" style="width:100%;max-width:1050px;margin:0 auto;padding:12px;box-sizing:border-box;font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.6;color:'+TEXT+';overflow-wrap:break-word;background:#FFFFFF;">'
    root+='<style>[data-material] *{box-sizing:border-box}[data-material] [hidden]{display:none!important}[data-material] :focus-visible{outline:3px solid #1F6388;outline-offset:3px}[data-material] sub,[data-material] sup{font-size:75%;line-height:0}[data-material] p:last-child{margin-bottom:0!important}[data-material] details{scroll-margin-top:16px}</style>'
    root+='<header style="background:linear-gradient(135deg,#123B5D,#1F6388);padding:16px 20px;border-radius:12px;color:#FFFFFF;margin-bottom:24px;"><p style="font-size:14px;margin:0 0 6px;letter-spacing:1.2px;text-transform:uppercase;">Microeconomie · ASEM</p><h1 style="font-size:24px!important;line-height:1.3;margin:0;color:#FFFFFF;">'+esc(title)+'</h1></header>'+box(p(intro))+controls(titles,kinds or {})+body+'<footer style="font-size:14px;color:#556374;margin-top:24px;">ASEM · Microeconomie</footer>'+SCRIPT+'</div>'
    full='<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title></head><body style="margin:0">'+root+'</body></html>'
    return full,root
def xmlbytes(node):return b'<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(node,encoding='utf-8')
def put(parent,name,value=None,**attrs):
    el=ET.SubElement(parent,name,attrs)
    if value is not None:el.text=str(value)
    return el
def definition(e):return p(e['definition'])+box(p(e['example']))

def glossary_exports(entries,titles,target):
    title='Glosar de microeconomie — Curs complet'
    intro='Definiții și exemple pentru toate cele 11 seminare. Căutați un concept sau selectați tema.'
    # The glossary import schema is GLOSSARY/INFO/ENTRIES/ENTRY.
    root=ET.Element('GLOSSARY');info=put(root,'INFO')
    for key,val in [('NAME',title),('INTRO',p(intro)),('INTROFORMAT',1),('ALLOWDUPLICATEDENTRIES',0),('DISPLAYFORMAT','dictionary'),('SHOWSPECIAL',1),('SHOWALPHABET',1),('SHOWALL',1),('ALLOWCOMMENTS',0),('USEDYNALINK',0),('DEFAULTAPPROVAL',1),('GLOBALGLOSSARY',0),('ENTBYPAGE',20)]:put(info,key,val)
    export_entries=put(info,'ENTRIES')
    for e in entries:
        item=put(export_entries,'ENTRY')
        for key,val in [('CONCEPT',e['concept']),('DEFINITION',definition(e)),('FORMAT',1),('DEFINITIONTRUST',0),('USEDYNALINK',0),('CASESENSITIVE',0),('FULLMATCH',1),('TEACHERENTRY',1)]:put(item,key,val)
        categories=put(item,'CATEGORIES')
        for n in e['seminars']:
            category=put(categories,'CATEGORY');put(category,'NAME',f'Seminarul {n} — {titles[n]}');put(category,'USEDYNALINK',0)
    (target/'Glosar de microeconomie — Import XML.xml').write_bytes(xmlbytes(root))
    source=ROOT/'template/glossary-source.mbz'
    with tarfile.open(source) as archive:files={m.name:archive.extractfile(m).read() for m in archive.getmembers() if m.isfile() and m.name!='.ARCHIVE_INDEX'}
    path='activities/glossary_134746/glossary.xml';activity=ET.fromstring(files[path]);g=activity.find('glossary');g.find('name').text=title;g.find('intro').text=p(intro);g.find('usedynalink').text='0';g.find('timemodified').text='1793060000'
    ge=g.find('entries');ge.clear();categories=g.find('categories');categories.clear();links={n:[] for n in titles}
    for i,e in enumerate(entries,1):
        item=put(ge,'entry',id=str(i))
        # No personal account is included. Moodle maps the anonymous author to userid 0.
        values=[('userid',0),('concept',e['concept']),('definition',definition(e)),('definitionformat',1),('definitiontrust',0),('attachment',0),('timecreated',1793060000),('timemodified',1793060000),('teacherentry',1),('sourceglossaryid',0),('usedynalink',0),('casesensitive',0),('fullmatch',1),('approved',1)]
        for key,val in values:put(item,key,val)
        put(item,'aliases');put(item,'ratings')
        for n in e['seminars']:links[n].append(i)
    link_id=0
    for n in titles:
        cat=put(categories,'category',id=str(n));put(cat,'name',f'Seminarul {n} — {titles[n]}');put(cat,'usedynalink',0);ce=put(cat,'category_entries')
        for entryid in links[n]:
            link_id+=1;put(put(ce,'category_entry',id=str(link_id)),'entryid',entryid)
    files[path]=xmlbytes(activity)
    backup=ET.fromstring(files['moodle_backup.xml']);information=backup.find('information');name='Glosar de microeconomie — Curs complet.mbz';information.find('name').text=name;information.find('backup_date').text='1793060000';information.find('contents/activities/activity/title').text=title;information.find('details/detail').set('backup_id',hashlib.md5(name.encode()).hexdigest())
    for setting in information.findall('settings/setting'):
        if setting.findtext('name')=='filename':setting.find('value').text=name
        if setting.findtext('name') in ['users','glossary_134746_userinfo']:setting.find('value').text='1'
    files['moodle_backup.xml']=xmlbytes(backup);files['users.xml']=xmlbytes(ET.Element('users'))
    order=['activities/','activities/glossary_134746/']+list(files)
    index=[f'Moodle archive file index. Count: {len(order)}']+[path+('\td\t0\t?' if path.endswith('/') else f'\tf\t{len(files[path])}\t1793060000') for path in order]
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w',format=tarfile.USTAR_FORMAT) as archive:
        for path,data in [('.ARCHIVE_INDEX',('\n'.join(index)+'\n\n').encode())]+[(p,b'' if p.endswith('/') else files[p]) for p in order]:
            item=tarfile.TarInfo(path);item.mtime=1793060000;item.mode=0o644
            if path.endswith('/'):item.type=tarfile.DIRTYPE;item.mode=0o755
            else:item.size=len(data)
            archive.addfile(item,io.BytesIO(data))
    (target/name).write_bytes(gzip.compress(raw.getvalue(),mtime=0))

def build(repo,course):
    sys.path.insert(0,str(course));import course as course_renderer
    data={n:json.loads((course/'data'/f'{n}.json').read_text()) for n in range(1,12)};titles={n:d['title'] for n,d in data.items()}
    out=repo/COURSE_FOLDER;out.mkdir(parents=True,exist_ok=True);teacher=repo/TEACHER_FOLDER;teacher.mkdir(parents=True,exist_ok=True)
    glossary=json.loads((ROOT/'glossary.json').read_text());bibliography=json.loads((ROOT/'bibliography.json').read_text());solutions=json.loads((ROOT/'new-solutions.json').read_text())
    body=''
    for i,e in enumerate(glossary,1):
        body+=records_card(f'g{i:03}',e['seminars'][0],'termen',e['concept'],definition(e),e['definition']+' '+e['example'])
    full,_=page('Glosar de microeconomie — Curs complet','Definiții și exemple pentru toate cele 11 seminare. Căutarea funcționează și fără diacritice.',body,titles)
    (out/'Glosar de microeconomie.html').write_text(full);glossary_exports(glossary,titles,out)
    body=''
    for i,b in enumerate(bibliography['books'],1):
        content=p(b['authors'])+p(b['publication'])+p('Seminare: '+' · '.join(map(str,b['seminars'])))
        if b['isbn']:content+='<span style="display:inline-block;padding:6px 12px;border-radius:8px;background:'+SOFT+';font-size:16px;">ISBN '+esc(b['isbn'])+'</span>'
        if b['verification'].startswith('https://'):content+='<p style="font-size:16px;margin:12px 0 0;"><a href="'+esc(b['verification'])+'" target="_blank" rel="noopener noreferrer" style="color:'+INK+';">Fișa ediției sau sursa bibliografică ↗</a></p>'
        record=records_card(f'b{i:02}',0,b['group'],str(i).zfill(2)+'. '+b['title'],content,' '.join([b['authors'],b['publication'],b['isbn']]))
        record=record.replace('data-seminars="0"','data-seminars="'+' '.join(map(str,b['seminars']))+'"');body+=record
    for i,b in enumerate(bibliography['historical_norms'],1):body+=records_card('norma'+str(i),7,'norma',b['title'],p(b['publication'])+p('Pentru aplicare juridică sau contabilă verificați forma în vigoare în sursa oficială. Această listă păstrează referința istorică a lecturii.'),b['publication'])
    kinds={'baza':'Lucrări de bază','recomandata':'Lecturi recomandate','suplimentara':'Resurse suplimentare','norma':'Referințe normative istorice'}
    full,fragment=page('Bibliografie pentru cursul de Microeconomie','Lucrări de bază și lecturi recomandate pentru toate temele cursului. Lista reunește recomandările capitolelor fără repetarea aceleiași ediții. ISBN este afișat numai când a fost identificat pentru ediția indicată.',body,titles,kinds)
    (out/'Bibliografie_Microeconomie_Moodle.html').write_text(full);(out/'Bibliografie_Microeconomie_Moodle_FRAGMENT.html').write_text(fragment)
    body='';counts={'solved':0,'new':0}
    for n,d in data.items():
        for kind,problems in [('solved',d['solved']),('new',d['new'])]:
            for i,pr in enumerate(problems,1):
                counts[kind]+=1;sol=pr if kind=='solved' else solutions[str(n)][i-1]
                content=h('Problemă')+p(pr['condition'])
                for t in pr.get('tables',[]):content+=course_renderer.tbl(t)
                content+=h('Cerințe')+ol(pr['requirements'])+h('Rezolvare pas cu pas')+ol(sol['steps'])
                for t in pr.get('result_tables',[]):content+=course_renderer.tbl(t)
                for g in pr.get('charts',[]):content+=course_renderer.svg(g)
                if pr.get('check'):content+=h('Verificare')+p(pr['check'])
                content+=box(h('Concluzie economică')+p(sol['conclusion'].replace('Profitele','Profiturile')),True)
                label='Problemă rezolvată' if kind=='solved' else 'Problemă pentru rezolvare'
                title=f'Seminarul {n} · {label} {i} — {pr["title"]}'
                plain=' '.join([pr['condition'],*pr['requirements'],*sol['steps'],sol['conclusion']])
                id=f's{n:02}-'+('r' if kind=='solved' else 'p')+f'{i:02}'
                body+=records_card(id,n,kind,title,content,plain)
    full,_=page('Rezolvări și explicații pentru profesor',f'{counts["solved"]} de probleme rezolvate în seminar și {counts["new"]} probleme pentru rezolvare. Căutați după cuvinte sau identificatori precum s06-p05. Filtrați după seminar și tipul problemei. Fișierul funcționează local fără internet.',body,titles,{'new':'Probleme pentru rezolvare','solved':'Probleme rezolvate în seminar'})
    (teacher/'Rezolvări — Toate seminarele.html').write_text(full)
    print(json.dumps({'glossary':len(glossary),'books':len(bibliography['books']),**counts}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,default=ROOT.parents[1]);parser.add_argument('--course-tools',type=Path);args=parser.parse_args()
    build(args.repo_root,args.course_tools or args.repo_root/'tools/moodle-course')
