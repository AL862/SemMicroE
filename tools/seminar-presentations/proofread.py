"""Check authored Romanian slide text and speaker notes with a local LanguageTool CLI."""
from pathlib import Path
import argparse, json, subprocess, concurrent.futures
ROOT=Path(__file__).resolve().parent

def strings(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,list):
        for item in value:yield from strings(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key not in ['kind','refs','source']:yield from strings(item)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--jar',type=Path,required=True);args=parser.parse_args()
    plan=json.loads((ROOT/'plan.json').read_text())
    for folder in ['plain','language']:(ROOT/folder).mkdir(exist_ok=True)
    def check(deck):
        n=deck['seminar'];file=ROOT/'plain'/f'{n}.txt'
        file.write_text('\n\n'.join(strings(deck)),encoding='utf-8')
        run=subprocess.run(['java','-Xmx384m','-jar',str(args.jar),'-l','ro','-c','utf-8','--json',str(file)],capture_output=True,text=True)
        if run.returncode not in [0,1]:raise RuntimeError(run.stderr)
        result=json.loads(run.stdout)
        (ROOT/'language'/f'{n}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        return {'seminar':n,'matches':len(result.get('matches',[])),'exit_code':run.returncode}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(check,plan))
    (ROOT/'language'/'summary.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(json.dumps(results))

if __name__=='__main__':main()
