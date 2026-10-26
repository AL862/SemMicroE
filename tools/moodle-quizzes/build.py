"""Build Realtime Quiz activity backups and ordinary Moodle question-bank XML.
Python standard library only. Run from a repository checkout or use --repo-root.
"""
from pathlib import Path
import argparse,base64,copy,csv,gzip,hashlib,html,io,json,random,re,tarfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
FOLDER='[2] Teste interactive pentru Moodle'
EPOCH=1793021264

def xmlbytes(root):
    ET.indent(root,space='  ')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)
def put(parent,name,text=None,**attrs):
    node=ET.SubElement(parent,name,attrs)
    if text is not None:node.text=str(text)
    return node
def format_question(text):
    text=html.escape(text)
    for base,index in [('Q','da'),('Q','sa'),('Q','d'),('Q','s'),('Q','x'),('Q','y'),('Q','c'),('Q','m'),('Q','r'),('P','c'),('P','v'),('P','a'),('P','b'),('E','d'),('E','s'),('E','i'),('E','xy')]:
        text=re.sub(r'\b'+base+index+r'\b',base+'<sub>'+index+'</sub>',text)
    text=re.sub(r'\b(MR|MC|TC|TR|[QPKLR])([0123])\b',r'\1<sub>\2</sub>',text)
    return text

def card(n,i,text):
    return ('<div lang="ro" style="background:#eaf7ec;border:1px solid #b7ddb9;border-left:6px solid #2e7d32;border-radius:12px;padding:20px 22px;margin:18px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.5;color:#17351b;">'
    f'<div style="font-size:13px;font-weight:bold;letter-spacing:0.08em;text-transform:uppercase;color:#2e7d32;margin-bottom:8px;">SEMINARUL {n} · ÎNTREBAREA {i}/25</div>'
    '<p style="font-size:24px;line-height:1.35;font-weight:bold;margin:0;color:#17351b;">'+format_question(text)+'</p></div>')

def bank(n,title):
    rows=[l.strip().split('|') for l in (ROOT/'bank'/f'{n}.txt').read_text().splitlines() if l.strip()]
    assert len(rows)==25
    rng=random.Random(20261026+n)
    labels=[0,1,2,3]*6+[n%4]
    for _ in range(100000):
        rng.shuffle(labels)
        if all(a!=b for a,b in zip(labels,labels[1:])):break
    else:raise ValueError('Could not arrange answer keys')
    result=[]
    for i,(parts,key) in enumerate(zip(rows,labels),1):
        assert len(parts)==6,(n,i)
        basis,text,correct,*wrong=parts
        assert len(set([correct,*wrong]))==4,(n,i)
        rng.shuffle(wrong);answers=wrong[:];answers.insert(key,correct)
        if basis.startswith('p'):
            source={'section':'Exerciții și probleme rezolvate','json_pointer':'/solved/'+str(int(basis[1:])-1)}
        elif basis=='r':source={'section':'Subiecte de recapitulare','json_fields':['questions','tf','tests']}
        elif basis=='c':source={'section':'Concluzii esențiale','json_pointer':'/conclusions'}
        else:source={'section':'Extindere aplicată','kind':'original scenario using course concepts'}
        source['file']=f'tools/moodle-course/data/{n}.json'
        result.append(dict(number=i,text=text,question_html=card(n,i,text),answers=answers,correct_index=key,time=60 if re.search(r'\d',text) else 30,source=source))
    return result

def make_mbz(n,name,questions):
    activity_id=27000+n;module_id=142277+n;context_id=219297+n
    directory=f'activities/realtimequiz_{module_id}'
    files={}
    for f in (ROOT/'template').rglob('*'):
        if f.is_file():
            relative=f.relative_to(ROOT/'template').as_posix()
            path=directory+'/'+relative.split('/',1)[1] if relative.startswith('activity/') else relative
            files[path]=f.read_bytes()
    activity=ET.Element('activity',id=str(activity_id),moduleid=str(module_id),modulename='realtimequiz',contextid=str(context_id))
    quiz=put(activity,'realtimequiz',id=str(activity_id))
    for key,value in [('name',name),('intro',''),('introformat',1),('timecreated',EPOCH),('timemodified',EPOCH),('questiontime',30)]:put(quiz,key,value)
    qs=put(quiz,'questions')
    for q in questions:
        elem=put(qs,'question',id=str(n*1000+q['number']))
        for key,value in [('questionnum',q['number']),('questiontext',q['question_html']),('questiontextformat',1),('questiontime',0 if q['time']==30 else q['time'])]:put(elem,key,value)
        ans=put(elem,'answers')
        for j,text in enumerate(q['answers']):
            answer=put(ans,'answer',id=str(n*10000+q['number']*4+j))
            put(answer,'answertext',text);put(answer,'correct',int(j==q['correct_index']))
    files[directory+'/realtimequiz.xml']=xmlbytes(activity)
    mod=ET.fromstring(files[directory+'/module.xml']);mod.set('id',str(module_id));mod.find('sectionnumber').text=str(n)
    files[directory+'/module.xml']=xmlbytes(mod)
    backup=ET.fromstring(files['moodle_backup.xml']);info=backup.find('information')
    info.find('name').text=name+'.mbz';info.find('backup_date').text=str(EPOCH)
    detail=info.find('details/detail');detail.set('backup_id',hashlib.md5(name.encode()).hexdigest())
    act=info.find('contents/activities/activity');act.find('moduleid').text=str(module_id);act.find('title').text=name;act.find('directory').text=directory
    for setting in info.findall('settings/setting'):
        for child in setting:
            if child.text:child.text=child.text.replace('realtimequiz_142277',f'realtimequiz_{module_id}')
        if setting.findtext('name')=='filename':setting.find('value').text=name+'.mbz'
    files['moodle_backup.xml']=xmlbytes(backup)
    order=['activities/',directory+'/']+list(files)
    index=[f'Moodle archive file index. Count: {len(order)}']
    for path in order:index.append(path+('\td\t0\t?' if path.endswith('/') else f'\tf\t{len(files[path])}\t{EPOCH}'))
    indexbytes=('\n'.join(index)+'\n\n').encode()
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w',format=tarfile.USTAR_FORMAT) as tar:
        for path,content in [('.ARCHIVE_INDEX',indexbytes)]+[(p,b'' if p.endswith('/') else files[p]) for p in order]:
            entry=tarfile.TarInfo(path);entry.mtime=EPOCH;entry.mode=0o755 if path.endswith('/') else 0o644
            if path.endswith('/'):entry.type=tarfile.DIRTYPE
            else:entry.size=len(content)
            tar.addfile(entry,io.BytesIO(content))
    return gzip.compress(raw.getvalue(),compresslevel=9,mtime=0)

def make_xml(n,title,questions):
    root=ET.Element('quiz');category=put(root,'question',type='category')
    put(put(category,'category'),'text',f'$course$/top/Microeconomie/Seminarul {n}. {title}')
    for q in questions:
        item=put(root,'question',type='multichoice')
        put(put(item,'name'),'text',f'Seminarul {n}. Întrebarea {q["number"]:02}')
        put(put(item,'questiontext',format='html'),'text',q['question_html'])
        for key,value in [('defaultgrade',1),('penalty',0),('hidden',0),('idnumber',f'semmicroe-s{n}-q{q["number"]:02}'),('single','true'),('shuffleanswers','false'),('answernumbering','abc')]:put(item,key,value)
        for j,text in enumerate(q['answers']):
            answer=put(item,'answer',fraction='100' if j==q['correct_index'] else '0',format='html')
            put(answer,'text',html.escape(text))
    return xmlbytes(root)

def build(repo):
    out=repo/FOLDER;out.mkdir(parents=True,exist_ok=True);xmlout=out/'Import întrebări Moodle XML';xmlout.mkdir(exist_ok=True)
    teacher=repo/'docs/moodle-tests';teacher.mkdir(parents=True,exist_ok=True)
    manifest=[];complete=[]
    for n in range(1,12):
        data=json.loads((repo/'tools/moodle-course/data'/f'{n}.json').read_text());title=data['title'];name=f'Test interactiv - Seminarul {n}. {title}'
        questions=bank(n,title);complete.append(dict(seminar=n,name=name,questions=questions))
        for f,content in [(out/(name+'.mbz'),make_mbz(n,name,questions)),(xmlout/(name+'.xml'),make_xml(n,title,questions))]:
            f.write_bytes(content);manifest.append(dict(path=f.relative_to(repo).as_posix(),sha256=hashlib.sha256(content).hexdigest(),bytes=len(content),questions=25))
    (teacher/'question-bank.json').write_text(json.dumps(complete,ensure_ascii=False,indent=2))
    (teacher/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    with (teacher/'answer-key.csv').open('w',newline='') as stream:
        w=csv.writer(stream);w.writerow(['Seminar','Întrebare','Răspuns','Text corect','Secunde','Bază'])
        for unit in complete:
            for q in unit['questions']:w.writerow([unit['seminar'],q['number'],'ABCD'[q['correct_index']],q['answers'][q['correct_index']],q['time'],q['source']['section']])
    return manifest
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,default=ROOT.parents[1]);args=parser.parse_args()
    print(json.dumps({'generated':len(build(args.repo_root)),'questions':275},ensure_ascii=False))
