"""Validate XML/MBZ parity, activity links, archive indexes and answer keys."""
from pathlib import Path
import collections,gzip,hashlib,io,json,re,tarfile,xml.etree.ElementTree as E
import argparse

def detect_moodle2_metadata(data):
    """Port of convert_helper::detect_moodle2_format signature checks, not a restore."""
    first=data[:200]
    return (b'<?xml version="1.0" encoding="utf-8"?>' in first.lower()
            and b'<moodle_backup>' in first and b'<information>' in first)

def validate(repo):
    folder=repo/'[2] Teste interactive pentru Moodle';bank=json.loads((repo/'docs/moodle-tests/question-bank.json').read_text());report=[]
    for unit in bank:
        n=unit['seminar'];name=unit['name'];rows=unit['questions'];assert len(rows)==25
        assert [q['number'] for q in rows]==list(range(1,26))
        keys=[q['correct_index'] for q in rows];assert all(a!=b for a,b in zip(keys,keys[1:]));counts=collections.Counter(keys);assert sorted(counts.values())==[6,6,6,7]
        assert len({q['text'].strip().casefold() for q in rows})==25
        with tarfile.open(folder/(name+'.mbz')) as archive:
            files={m.name:m for m in archive.getmembers()};index=archive.extractfile('.ARCHIVE_INDEX').read().decode().splitlines()
            declared=int(index[0].split(': ')[1]);listed=[x for x in index[1:] if x];assert declared==len(listed)==len(files)-1
            for line in listed:
                path,kind,length,mtime=line.split('\t');member=files[path.rstrip('/')]
                assert member.isdir()==(kind=='d');assert member.size==int(length)
            metadata=archive.extractfile('moodle_backup.xml').read()
            # Same first-200-byte signature tests as Moodle's format detector.
            assert detect_moodle2_metadata(metadata),(n,'Moodle format signature')
            backup=E.fromstring(metadata);activity=backup.find('information/contents/activities/activity')
            directory=activity.findtext('directory');mid=activity.findtext('moduleid')
            content=E.fromstring(archive.extractfile(directory+'/realtimequiz.xml').read());quiz=content.find('realtimequiz')
            assert content.get('moduleid')==mid
            assert quiz.findtext('name')==name==activity.findtext('title')
            assert E.fromstring(archive.extractfile(directory+'/module.xml').read()).get('id')==mid
            questions=quiz.findall('questions/question');assert len(questions)==25
            assert all(s.findtext('value')=='0' for s in backup.findall('information/settings/setting') if s.findtext('name') in ['users','realtimequiz_'+mid+'_userinfo'])
            assert int(quiz.findtext('questiontime'))==30
            qids=[q.get('id') for q in questions];aids=[a.get('id') for q in questions for a in q.findall('answers/answer')];assert len(set(qids))==25 and len(set(aids))==100
        xml=E.parse(folder/'Import întrebări Moodle XML'/(name+'.xml'));multichoice=xml.findall("question[@type='multichoice']");assert len(multichoice)==25
        for q,element,item in zip(rows,questions,multichoice):
            assert element.findtext('questiontext')==q['question_html']==item.findtext('questiontext/text')
            assert ',' not in q['text'];assert not re.search(r'Tom[șşs]a|Mankiw|Томша|Мэнкью',q['text'],re.I)
            assert len(set(a.strip().casefold() for a in q['answers']))==4
            answers=element.findall('answers/answer');assert len(answers)==4
            assert [a.findtext('answertext') for a in answers]==q['answers']
            assert [a.findtext('correct') for a in answers]==['1' if i==q['correct_index'] else '0' for i in range(4)]
            assert [int(a.get('fraction')) for a in item.findall('answer')]==[100 if i==q['correct_index'] else 0 for i in range(4)]
            assert item.findtext('shuffleanswers')=='false'
            time=int(element.findtext('questiontime')) or 30;assert time==q['time'] in [30,60]
            assert 'correct_index' not in q['question_html'] and 'Răspuns corect' not in q['question_html']
            src=q['source'];data=json.loads((repo/src['file']).read_text())
            if src.get('json_pointer','').startswith('/solved/'):
                assert int(src['json_pointer'].split('/')[-1])<len(data['solved'])
        report.append({'seminar':n,'questions':25,'answers':100,'one_correct_per_question':True,'adjacent_keys_different':True,'key_counts':{chr(65+k):v for k,v in sorted(counts.items())},'xml_mbz_key_parity':True,'archive_index_valid':True,'moodle_format_signature_valid':True,'seconds':dict(collections.Counter(q['time'] for q in rows))})
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,required=True);args=p.parse_args();print(json.dumps(validate(args.repo_root),ensure_ascii=False,indent=2))
