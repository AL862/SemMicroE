"""Independent exact-arithmetic audit of numerical multiple-choice answer keys."""
from fractions import Fraction as F
from pathlib import Path
import json,re,argparse

def check(repo):
 cases={
 1:{16:1000-800,17:F(1000-900,100),18:F(150,100),19:50-5*4,20:F(50,5),21:5,23:max(240,300)},
 2:{16:F(120,3),17:100-40,18:70-40,19:4+2,20:4-2,21:4-2,22:65+30,23:40+55,24:min(35,60),25:4*36},
 3:{16:F(-3,10)*(-10),17:40-2*10,18:-2*F(10,20),19:320-4*40,22:6-2,23:F(-10,5),24:27*230,25:F(6,10)},
 4:{16:47-25,18:20*2+10*3,19:70+80,23:F(120,20),24:20+2*5},
 5:{9:F(3000,125),10:65-48,25:84-90},
 6:{16:50*10+100*15,17:F(2000,200),18:50**2,19:5*20,20:F(100,40),22:30*3+50*5,23:F(160,80),24:12000-8500},
 7:{16:300*150-150**2,17:300-2*150,18:100-20,19:F(60000,100-20),20:F(4000,80-40),21:F(50+10**2,10),22:F(26000+40000,600),23:4000-3000,24:25-32},
 8:{18:100*40,19:400-243,20:20*F(1,3),21:45*4,22:35,23:800-(25-20)*100,24:(40-32)*60,25:F(4000,80)},
 9:{16:20*22,17:440-240,19:F(110-100,110),20:-1/F(-11),21:F(661,6)-F(649,6),22:F(2000,3)*20,23:11*48-10*50,24:100-20,25:1400-1000},
 10:{16:130-2*16,17:(2*16+2)*16,20:100-2*5,21:(52-44)*6,23:(40-40)*60,24:100-70,25:30*20-400},
 11:{16:206-3*40,17:20+20,18:30-F(20,2),19:F(9,4)+F(45,4),21:140-F(140,2),22:300-140-70,23:60**2+40**2}}
 data=json.loads((repo/'docs/moodle-tests/question-bank.json').read_text());checked=[]
 def number(s):
  match=re.search(r'-?\d+(?:/\d+)?',s.replace('−','-'));return F(match[0]) if match else None
 for unit in data:
  n=unit['seminar']
  for qno,expected in cases[n].items():
   q=unit['questions'][qno-1];actual=number(q['answers'][q['correct_index']]);assert actual==expected,(n,qno,actual,expected)
   assert sum(number(a)==expected for a in q['answers'])==1,(n,qno,'multiple numeric matches')
   checked.append({'seminar':n,'question':qno,'exact_result':str(expected)})
 return {'passed':len(checked),'checks':checked}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,required=True);args=p.parse_args();print(json.dumps(check(args.repo_root),ensure_ascii=False,indent=2))
