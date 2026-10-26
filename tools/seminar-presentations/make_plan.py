from pathlib import Path
import re,json
from specs import SPECS
ROOT=Path(__file__).parent;COURSE=ROOT.parents[1]/'tools/moodle-course/data'
# Every deck uses a compact 11-minute plan, not an automatic slide advance.
DURATIONS=[45,60,60,60,75,75,60,90,90,45]
PROMPTS=[
('Ce alternativă nu mai putem realiza cu aceeași resursă?','Valoarea celei mai bune alternative abandonate este reperul.'),
('Care mărime se referă la un preț și nu la întreaga relație?','Cantitatea cerută sau oferită la acel preț.'),
('De ce nu comparăm doar semnul coeficientului?','Semnul arată direcția. Valoarea absolută arată intensitatea.'),
('Poate un coș preferat să nu fie ales?','Da. El poate depăși bugetul disponibil.'),
('Înseamnă MP mai mic că TP scade?','Nu cât timp MP rămâne pozitiv.'),
('Sunt media și costul următoarei unități același lucru?','Nu. Media repartizează totalul. MC descrie sporul.'),
('Dovedesc încasările mai mari un profit mai mare?','Nu fără comparația cu costul suplimentar.'),
('De ce mai contează FC după oprirea de astăzi?','În exemplu acest cost nu poate fi evitat pe termen scurt.'),
('De unde citim prețul monopolist?','De pe cerere după ce am ales cantitatea.'),
('Garantează un produs diferit profit pozitiv?','Nu. Încasările trebuie să acopere costurile.'),
('Este suficient să verificăm numai alegerea firmei 1?','Nu. Ambele alegeri trebuie să fie răspunsuri optime.')]

EXPLAIN={
1:'Pentru această frontieră păstrăm aceleași resurse și aceeași tehnologie. Interceptările sunt X = 10 și Y = 50. Punctul cu X = 4 și Y = 30 folosește întreaga posibilitate a modelului. Un punct aflat sub frontieră lasă capacitate nefolosită. Nu îl confundăm cu o tehnologie mai slabă. O altă alegere pe dreaptă nu mută dreapta.',
2:'Pentru funcțiile acestui seminar comparăm cererea Qd = 100 − P cu oferta Qs = −20 + 2P. În desen oferta pozitivă începe de la prețul10. Intersecția este la Q = 60 și P = 40. Numerele sunt aceleași în exercițiu. Nu calculăm aici impozite sau subvenții. Acestea sunt aplicații ulterioare ale modelului și nu schimbă sensul egalității de echilibru.',
3:'În acest desen panta funcției Qd = 40 − 2P este −2. La P = 10 cantitatea este20. Raportul dintre preț și cantitate este1/2. În alte puncte se schimbă acel raport chiar dacă dreapta are aceeași pantă. Reamintim că elasticitatea punctuală descrie o reacție locală. Pentru o schimbare mare a prețului am verifica separat noile încasări.',
4:'Linia bugetară folosește venitul de120de lei și prețurile20și10. În exemplu TU = X × Y reprezintă preferințele și nu bani primiți de consumator. Cele două coșuri pe care le comparăm au același cost. Ele nu au aceeași utilitate. La întrebarea despre coșul preferat trebuie folosită funcția de utilitate și nu doar suma de bani rămasă.',
5:'În toate echipele păstrăm aceeași pregătire:30de minute pentru amestecarea ingredientelor și frământarea aluatului. Dospirea înseamnă timpul în care aluatul crește. Dospirea și pregătirea pentru cuptor au aceeași durată între echipe. O coacere durează o oră iar cuptorul primește o singură tavă de cel mult30de pâini. Nu introducem o a doua tavă simultan pentru a explica sporul.',
6:'Pentru funcția TC = 100 + 5Q fiecare produs suplimentar adaugă5lei. Costul fix de100de lei nu se modifică în comparație. La20de produse costul total este200iar media este10. Pe măsură ce producția crește componenta fixă pe produs se reduce. Aceasta explică de ce media se poate apropia de5în timp ce totalul continuă să crească.',
7:'În această situație prețul de50de lei este constant. Firma nu pierde încasări pe produsele vândute deja când adaugă încă o unitate. Costul marginal însă crește. La Q = 20 el ajunge la50. Profitul poate fi rescris300 − (Q−20)². Această formă confirmă maximul fără o demonstrație lungă cu derivate. Nu confundăm vârful profitului cu vârful încasărilor.',
8:'Folosim numai tehnologia TC = 100 + 10Q + Q² și prețul de20. La cantitatea5încasările sunt100iar costul este175. Costul variabil este75. Producția aduce o contribuție de25la costul fix. Prin oprire am pierde întregul cost fix de100. Decizia de continuare este pentru termenul scurt precizat și nu o promisiune că firma ar trebui să rămână permanent în ramură.',
9:'În acest desen cererea este P = 100 − 2Q iar costul marginal este20. Linia MR coboară mai repede decât cererea. Găsim cantitatea20la întâlnirea MR cu MC. Ridicăm apoi aceeași cantitate până la cerere pentru prețul60. Aceste două puncte sunt distincte. Profitul de700ține cont și de costul fix de100. Puterea asupra prețului nu elimină acel cost.',
10:'Aceeași tehnologie și aceeași cerere sunt folosite în desen și în exercițiu. La Q = 15 avem P = 65 iar MR = MC = 50. Prețul peste costul marginal nu este întreaga marjă de profit pe produs. Pentru profit folosim costul total de725și încasările de975. O altă cerere după intrarea rivalilor ar cere o alegere nouă.',
11:'Ambele firme au cost marginal30și cost fix zero. La cantitatea20a rivalei cel mai bun răspuns este tot20. Graficul arată o alegere simultană și nu o succesiune cronologică. Un echilibru Cournot este un echilibru Nash în acest model de cantități. Modelul nu spune că aceleași două firme ar avea obligatoriu același rezultat dacă ar alege prețuri sau dacă una s-ar angaja prima.'}
# Separate numerals from ordinary words without changing formula coefficients.
for _key,_value in EXPLAIN.items():
 EXPLAIN[_key]=re.sub(r'(\d)(de|iar|și|la|ține|a |în|pentru)',r'\1 \2',_value)
 EXPLAIN[_key]=re.sub(r'(?<=[a-zăâîșț])(\d)',r' \1',EXPLAIN[_key])
 EXPLAIN[_key]=re.sub(r'(\d)(lei|pâini|unități)\b',r'\1 \2',EXPLAIN[_key])

def clean(s):
 s=re.sub('<[^>]+>','',s);return re.sub(r'\.{2,}', '.',s.replace('&gt;','>').replace('&lt;','<'))
def notes_for(n,slide,i,data,spec,used):
 text=[]
 if i==0:
  text=[data['description'], 'Întrebarea care ne conduce este aceasta: '+spec['hook'], 'Nu urmărim să refacem întreaga lecție. Alegem mecanismul central al temei și îl folosim într-un singur exemplu. La final trecem la problemele seminarului. Invităm studenții să observe cine alege și ce restricție întâlnește.']
 elif 1<=i<=6:
  ref=spec['refs'][i-1];title,paras=data['theory'][ref]
  relevant=[p for p in paras if not re.search(r'\d',p) and not (n==3 and re.search(r'perfect elastic|perfect inelastic|elasticitatea de arc',p,re.I))]
  available=[p for p in relevant if p not in used]
  selected=available[:2] if available else relevant[:1]
  used.update(selected)
  text=['Ideea acestui moment este: '+slide['title']+'.']+selected
  if slide.get('cards'):
   text+=['Pe schemă urmărim următoarea legătură: '+'. '.join(label+'. '+value for label,value in slide['cards'])+'.']
  if slide.get('steps'):
   text+=['Citim mecanismul în această ordine: '+'. '.join(a+'. '+b for a,b in slide['steps'])+'.']
  if i==4:text+=['Citim formula înainte de a introduce numerele. Precizăm ce măsoară fiecare simbol și folosim aceeași perioadă pentru toate mărimile. Separăm datele problemei de rezultatul pe care vrem să îl obținem.']
  if i==5:text+=[EXPLAIN[n]]
  if i==5:text+=['Începem cu axele și unitățile. Urmărim apoi liniile și punctul marcat. Graficul nu este o a doua problemă. El explică aceeași situație numerică pe care o vom calcula. '+spec['graph'][2]]
  if i==6:text+=['Verificare orală: '+PROMPTS[n-1][0]+' Răspuns așteptat: '+PROMPTS[n-1][1]]
  if i in [2,3]:text+=['Facem o pauză scurtă și cerem reformularea ideii în cuvinte proprii. Dacă răspunsul amestecă două noțiuni revenim la diferența dintre ele înaintea formulei.']
 elif i==7:
  text=[spec['example'][1], 'Cerințele sunt: '+'. '.join(spec['example'][2])+'.', 'Le oferim studenților timp să scrie relația necesară și să identifice datele. Nu afișăm încă soluția. Îi rugăm să explice ce caută și de ce formula aleasă răspunde cerinței. Păstrăm aceeași perioadă și aceeași unitate pe parcursul calculului. Corectăm întâi alegerea relației și abia apoi operațiile aritmetice.']
 elif i==8:
  text=['Parcurgem soluția în ordinea cerințelor.']+[a+'. '+b+'.' for a,b in spec['solution'][1]]+[spec['solution'][2], 'Verificăm prin înlocuire în relațiile inițiale și explicăm semnul rezultatului. O valoare negativă nu este automat o eroare de calcul. Ea poate exprima o pierdere sau o reducere a indicatorului. Cerem unui student să spună rezultatul împreună cu unitatea și sensul economic.']
 else:
  text=['Reținem trei idei. '+ ' '.join(spec['end']), 'Întrebarea de verificare este: '+PROMPTS[n-1][0], 'Răspuns: '+PROMPTS[n-1][1], 'În continuare deschidem exercițiile seminarului. Folosim aceeași succesiune: identificăm datele și restricția. Alegem relația potrivită. Calculăm și verificăm. Încheiem cu o explicație economică în cuvinte proprii.']
 return '\n\n'.join(clean(s).replace('volumul pozitiv minimizant','volumul pozitiv care minimizează AVC') for s in text)

def build_plan():
 decks=[]
 for n,spec in SPECS.items():
  data=json.loads((COURSE/f'{n}.json').read_text());title=data['title'];slides=[]
  def add(kind,title,**kwargs):slides.append(dict(kind=kind,title=title,**kwargs))
  add('cover',title,hook=spec['hook'],promise=spec['promise'])
  t,lead,cards=spec['context'];add('context',t,lead=lead,cards=cards)
  t,cards=spec['concepts'];add('concepts',t,cards=cards)
  t,steps=spec['mechanism'];add('flow',t,steps=steps)
  t,f,a,b=spec['formula'];add('formula',t,formula=f,lines=[a,b])
  t,a,b=spec['graph'];add('graph',t,lines=[a,b])
  t,a,b,c,d=spec['pitfall'];add('compare',t,cards=[(a,b),(c,d)])
  t,condition,requirements=spec['example'];add('exercise',t,condition=condition,requirements=requirements)
  t,steps,conclusion=spec['solution'];add('solution',t,steps=steps,conclusion=conclusion)
  add('end','De aici încep exercițiile seminarului',points=spec['end'],check=PROMPTS[n-1][0])
  used=set()
  for i,slide in enumerate(slides):
   slide['number']=i+1;slide['planned_seconds']=DURATIONS[i];slide['notes']=notes_for(n,slide,i,data,spec,used)
   assert ',' not in slide['notes'],(n,i,'comma in notes')
  decks.append({'seminar':n,'title':title,'duration_minutes':sum(DURATIONS)/60,'source':spec['source'],'slides':slides})
 return decks
if __name__=='__main__':
 decks=build_plan();(ROOT/'plan.json').write_text(json.dumps(decks,ensure_ascii=False,indent=2))
 for d in decks:print(d['seminar'],len(d['slides']),d['duration_minutes'],'minutes; notes words',sum(len(s['notes'].split()) for s in d['slides']))
