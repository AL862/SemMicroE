"""Render the Moodle instruction with the course's shared inline components."""
from pathlib import Path
import argparse,json,html,sys
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent
FOLDER='[4] Lucrări individuale pentru studenți'
HTML_NAME='Instrucțiune — Lucrări individuale pentru studenți.html'
PPTX_NAME='Șablon — Lucrare individuală la Microeconomie.pptx'
INK='#123B5D';TEXT='#24313D';MUTED='#556374';BORDER='#E2E8EF';SURFACE='#F6F8FB'

def fmt(text):
    return html.escape(text)

def p(text):
    return '<p style="margin:0 0 12px;max-width:75ch;font-size:18px;line-height:1.6;">'+fmt(text)+'</p>'

def h2(text):return '<h2 style="font-size:24px;line-height:1.3;font-weight:700;color:'+INK+';margin:0 0 16px;">'+fmt(text)+'</h2>'
def h3(text):return '<h3 style="font-size:20px;line-height:1.4;font-weight:700;color:'+INK+';margin:0 0 12px;">'+fmt(text)+'</h3>'
def card(body,green=False):
    return '<div style="padding:20px 22px;border:1px solid '+BORDER+';border-radius:12px;margin:0 0 16px;min-width:0;background:'+('#F0F8EC;border-left:5px solid #3F8F1F' if green else '#FFFFFF')+';">'+body+'</div>'
def listing(items,ordered=False):
    tag='ol' if ordered else 'ul'
    return '<'+tag+' style="padding-left:24px;margin:0;">'+''.join('<li style="margin:0 0 6px;">'+fmt(x)+'</li>' for x in items)+'</'+tag+'>'
def table(headers,rows):
    cell='padding:12px 14px;border:1px solid '+BORDER+';text-align:left;vertical-align:top;'
    return '<div style="overflow-x:auto;width:100%;max-width:100%;" tabindex="0" role="region" aria-label="Exemple de utilizare a datelor"><table style="width:100%;min-width:590px;border-collapse:collapse;font-size:16px;line-height:1.45;"><caption style="text-align:left;font-weight:700;margin-bottom:12px;">Din sursă în analiză</caption><thead><tr>'+''.join('<th scope="col" style="'+cell+'background:'+SURFACE+';">'+fmt(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td style="'+cell+'">'+fmt(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

SLIDES=[
('Titlul temei',[
'Indicați tema aleasă în Moodle și numele și prenumele. Completați grupa și disciplina și profesorul și anul universitar. Alegeți o imagine sau o schemă care are legătură cu fenomenul studiat. Titlul trebuie să permită identificarea produsului sau a deciziei analizate.',
'Nu încărcați coperta cu definiții. Înlocuiți toate câmpurile dintre paranteze din șablon. Păstrați un titlu lizibil și verificați că numele fișierului corespunde lucrării.']),
('Problema economică și obiectivul',[
'Formulați o întrebare la care puteți răspunde cu datele și metoda alese. Precizați produsul sau firma ori piața și perioada. Explicați în două fraze de ce alegerea contează pentru un consumator sau pentru un producător.',
'Scrieți ce veți compara sau calcula. Un obiectiv precum „compar costul livrării proprii cu tariful unui curier” indică un rezultat verificabil. „Prezint tema” nu precizează ce veți afla. Întrebarea trebuie reluată în concluzii.']),
('Concepte fundamentale',[
'Alegeți două sau trei noțiuni necesare pentru a înțelege întrebarea. Explicați-le în cuvinte proprii și arătați legătura lor cu situația aleasă. Definiți prescurtările înainte de a le folosi.',
'Includeți numai concepte pe care le utilizați apoi în model sau în analiză. Dacă studiați pragul de rentabilitate explicați costul fix și costul variabil pe unitate și profitul. Nu copiați un capitol și nu enumerați termeni care nu mai apar în lucrare.']),
('Modelul economic și metoda',[
'Arătați relația dintre variabile și explicați ce presupuneți constant. Alegeți o schemă sau o formulă ori un grafic potrivit întrebării. Definiți simbolurile și unitățile. Un grafic trebuie să aibă axe și linii explicate în text.',
'Precizați cum veți folosi modelul asupra datelor. Pentru un cost explicați ce componente adunați. Pentru elasticitate precizați convenția de calcul al variațiilor procentuale. Într-o comparație fără formulă prezentați criteriile după care veți evalua alternativele.']),
('Datele și rolul surselor',[
'Selectați numai date relevante pentru întrebarea de pe diapozitivul 2. Arătați sursa exactă și perioada și unitatea. Distingeți prețul pe kilogram de prețul pe ambalaj și venitul lunar de cel anual. Dacă transformați o unitate arătați regula conversiei.',
'Pentru fiecare valoare precizați unde va fi folosită în studiul de caz de pe diapozitivul 6 și în calculul sau comparația de pe diapozitivul 7. Prețul intră în cost sau în încasări. Cantitatea intră în producție sau în vânzări. Condițiile unui voucher intră în evaluarea coșurilor accesibile. Datele nu sunt un decor și nu rămân doar într-un tabel separat.',
'Separați valorile documentate de ipotezele proprii. Pentru valori inventate scrieți „Date ipotetice — exemplu didactic”. Un link general către o instituție nu înlocuiește identificarea tabelului sau a paginii folosite.']),
('Exemplul practic sau studiul de caz',[
'Definiți situația asupra căreia aplicați modelul: cine ia decizia și între ce variante. Precizați produsul și perioada. Preluați explicit valorile necesare de pe diapozitivul cu date. Arătați ce înseamnă fiecare dintre ele în situația concretă.',
'Prezentați o întrebare aplicată și condițiile comparației. De exemplu comparați două volume de producție folosind același cost fix și prețurile ingredientelor documentate. Pentru un voucher verificați coșurile folosind prețurile și regulile comerciale găsite. Nu adăugați o povestire fără legătură cu datele și cu metoda.']),
('Analiza și rezultatele',[
'Arătați pașii care duc de la date la rezultat. Pentru o temă numerică prezentați formula și valorile înlocuite și rezultatul cu unitatea sa. Pentru comparații construiți un tabel în care aceleași criterii sunt aplicate tuturor variantelor. Păstrați aceleași perioade și unități.',
'Reutilizați valorile din studiul de caz. Nu introduceți aici alte numere fără sursă sau fără explicație. Verificați operațiile și interpretați un semn negativ. Dacă tema nu cere un calcul folosiți informațiile documentate într-o comparație argumentată. O listă de surse sau un grafic fără explicație nu reprezintă analiza.']),
('Interpretarea economică',[
'Explicați ce înseamnă rezultatul pentru decizia de la început. Spuneți ce variantă este preferabilă în condițiile analizate și de ce. Legați rezultatul de noțiunile și de mecanismul economic prezentate anterior.',
'Arătați cel puțin o limită concretă: o cantitate presupusă; un cost lipsă; o diferență de calitate; o perioadă scurtă. Explicați cum ar putea afecta concluzia. Datele ipotetice arată consecințele ipotezelor. O asociere între două serii reale nu demonstrează singură o relație cauzală.']),
('Concluzii',[
'Răspundeți direct la întrebarea inițială. Formulați două sau trei concluzii susținute de rezultatele prezentate. Menționați valoarea sau comparația care justifică fiecare concluzie. Precizați pentru ce condiții este valabilă.',
'Nu adăugați date noi și nu extindeți automat rezultatul la întreaga Republică Moldova. Dacă analiza este ipotetică spuneți ce mecanism ați demonstrat. Dacă informația este insuficientă explicați ce ați putut afla și ce rămâne necunoscut.']),
('Bibliografie și surse',[
'Identificați fiecare sursă folosită efectiv. Pentru date indicați instituția și titlul tabelului sau indicatorului și perioada. Pentru pagini online adăugați adresa exactă și data consultării. În cazul materialelor de specialitate indicați autorul și titlul și anul și paginile folosite.',
'Puneți și o trimitere scurtă lângă tabelul sau graficul relevant. Bibliografia finală permite verificarea analizei și nu înlocuiește folosirea datelor în ea. Păstrați numai sursele consultate și explicați care valori sunt ipoteze proprii.'])]

SOURCES=[
('BNS și StatBank','https://statbank.statistica.md/PxWeb/pxweb/ro/','Prețuri și indici de preț. Ocupare și salarii. Producție și indicatori sectoriali. Alegeți tabelul care răspunde întrebării.'),
('ANRE','https://anre.md/','Tarife și publicații despre energie și carburanți. Verificați serviciul și categoria consumatorului și data aplicării.'),
('AIPA','https://aipa.gov.md/','Programe și condiții de sprijin agricol. Forma ajutorului stabilește modul în care poate intra în calcul.'),
('BNM','https://www.bnm.md/','Cursuri și indicatori monetari. Folosiți o conversie valutară numai când datele trebuie aduse la aceeași monedă.'),
('Portalul datelor deschise','https://date.gov.md/home/','Seturi de date publice. Verificați instituția care publică tabelul și perioada acoperită.'),
('World Bank DataBank','https://databank.worldbank.org/','Serii internaționale pentru comparații. Verificați definiția indicatorului și unitatea înainte de utilizare.'),
('Eurostat','https://ec.europa.eu/eurostat/data/database','Date comparabile pentru țări europene. Selectați aceeași definiție și aceeași perioadă.'),
('FAOSTAT','https://www.fao.org/faostat/en/','Producție agricolă și indicatori alimentari. Distingeți producția de vânzări și de cantitatea oferită într-un scenariu.'),
('ILOSTAT','https://ilostat.ilo.org/data/','Ocupare și productivitate și alți indicatori ai muncii. Citiți definițiile înainte de comparație.')]

def render(repo,course_tools):
    sys.path.insert(0,str(course_tools))
    from components import back_link,action_button
    topics=json.loads((ROOT/'topics.json').read_text())
    titles={n:json.loads((course_tools/'data'/f'{n}.json').read_text())['title'] for n in range(1,12)}
    sections=[]
    sections.append(('organizare','1. Cum organizați lucrarea',card(
        p('Alegeți o singură temă în Moodle. O temă deja ocupată nu mai poate fi selectată. Schimbarea alegerii se face numai dacă o permite profesorul.')+
        p('Prezentați lucrarea în limba română în aproximativ 10 minute. Orientativ pregătiți 8–10 diapozitive inclusiv titlul și bibliografia. Eliminați diapozitivul final de ghid din șablon. Puteți uni sau reordona diapozitivele dacă păstrați logica explicației.')+
        p('Cercetarea se realizează exclusiv online. Folosiți informații deja publicate. Nu se cer sondaje proprii sau interviuri și nici vizite la magazine ori întreprinderi. Dacă lipsesc datele necesare construiți un scenariu ipotetic și declarați ipotezele.')+
        p('Lucrarea trebuie să lege întrebarea de date și datele de analiză. O fotografie sau o cifră fără utilizare în comparație nu înlocuiește argumentul economic. Nu este obligatoriu un calcul artificial când tema se rezolvă printr-o comparație documentată.'))))
    catalog=p('Alegeți una dintre cele 33 de teme. Fiecare seminar are trei variante. Deschideți seminarul și apoi tema pentru a citi cerința completă.')
    catalog+='<div data-disclosure-controls style="display:none;flex-wrap:wrap;gap:8px;margin:0 0 16px;">'+action_button('Deschide toate temele',True,True)+action_button('Închide toate temele',False)+'</div>'
    for n in range(1,12):
        catalog+='<details class="individual-seminar" id="seminar-'+str(n)+'" style="border:1px solid '+BORDER+';border-radius:12px;margin:0 0 12px;min-width:0;background:#FFFFFF;"><summary style="cursor:pointer;font-size:18px;font-weight:700;line-height:1.4;padding:14px 16px;min-height:48px;color:'+INK+';"><span>Seminarul '+str(n)+' — '+fmt(titles[n])+'</span><span style="display:block;font-size:14px;font-weight:400;color:'+MUTED+';margin:8px 0 0;">3 teme de cercetare</span></summary><div style="padding:4px 16px 16px;min-width:0;">'
        for t in [t for t in topics if t['seminar']==n]:
            catalog+='<details class="individual-topic" id="tema-'+str(t['number']).zfill(2)+'" style="border:1px solid '+BORDER+';border-radius:12px;margin:0 0 12px;background:'+SURFACE+';min-width:0;"><summary style="cursor:pointer;font-size:18px;font-weight:700;line-height:1.4;padding:14px 16px;min-height:48px;color:'+INK+';">'+str(t['number']).zfill(2)+'. '+fmt(t['title'])+'</summary><div style="padding:4px 16px 16px;background:#FFFFFF;border-radius:0 0 12px 12px;">'+''.join(p(x) for x in t['paragraphs'])+'</div></details>'
        catalog+='</div></details>'
    sections.append(('teme','2. Teme de cercetare și cerințe practice',catalog))
    slides=p('Șablonul are zece diapozitive de lucru și un ghid care se elimină. Mai jos este explicat rolul fiecărui diapozitiv. Păstrați un singur fir al argumentului de la întrebare la concluzie.')
    slides+=card(h3('Datele trebuie să lucreze în analiză')+p('Fiecare dată selectată trebuie folosită în studiul de caz și în calculele sau comparațiile corespunzătoare. Nu o includeți doar pentru a arăta că ați găsit o sursă. Urmăriți traseul: sursă → valoare sau condiție → aplicare → rezultat → concluzie.')+table(['Date selectate','Utilizare în studiul de caz','Rezultat verificabil'],[
        ['Preț și cantitate','Calculați costul sau încasările aceleiași operații.','Suma și unitatea sunt explicate.'],
        ['Cost fix și cost pe unitate','Calculați costul pentru volumele comparate.','Cost total și mediu ori prag de rentabilitate.'],
        ['Două prețuri și două cantități comparabile','Aplicați aceeași convenție a variațiilor procentuale.','Coeficient al elasticității cu interpretare.'],
        ['Tarif și consum de energie','Înmulțiți valori exprimate în unități compatibile.','Costul energiei și contribuția sa la total.'],
        ['Regulile unui voucher sau condițiile de livrare','Verificați aceleași coșuri sau comenzi în fiecare variantă.','Comparație argumentată a opțiunilor accesibile.']]),True)
    for i,(title,paragraphs) in enumerate(SLIDES,1):slides+=card(h3('Diapozitivul '+str(i)+' — '+title)+''.join(p(x) for x in paragraphs))
    sections.append(('structura','3. Ce trebuie să conțină fiecare diapozitiv',slides))
    source=p('Alegeți sursa după informația necesară. Nu trebuie să folosiți toate portalurile. Deschideți tabelul sau documentul original și păstrați adresa exactă. Căutați numai date care vor intra în analiza temei.')
    for label,url,desc in SOURCES:
        source+='<div style="padding:16px 0;border-bottom:1px solid '+BORDER+';min-width:0;"><a href="'+html.escape(url,quote=True)+'" target="_blank" rel="noopener noreferrer" style="font-size:18px;font-weight:700;color:'+INK+';text-decoration:underline;overflow-wrap:anywhere;">'+fmt(label)+' ↗</a>'+p(desc)+'</div>'
    source+=card(h3('Surse comerciale și ipoteze proprii')+p('Meniurile și cataloagele pot furniza prețuri. Anunțurile de angajare pot oferi salarii și programul. Fișele tehnice pot indica puterea sau capacitatea utilajelor. Folosiți informația în calculul costului sau în comparația variantelor. Un preț publicat nu arată singur cantitatea vândută și o capacitate nominală nu reprezintă producția realizată.')+p('Pentru date ipotetice declarați valorile și motivul alegerii lor. Le puteți combina cu prețuri reale numai dacă fiecare origine este clară. Concluzia unui asemenea calcul descrie scenariul. Nu devine o măsurare a pieței reale.'))
    sections.append(('surse','4. Cum selectați și utilizați sursele',source))
    checks=['Am ales o singură temă și am formulat o întrebare precisă.','Am explicat conceptele și condițiile modelului.','Am identificat sursa și perioada și unitatea fiecărei date.','Am folosit datele în studiul de caz și în calculele sau comparațiile lucrării.','Am separat valorile reale de ipotezele proprii.','Am arătat pașii analizei și am verificat rezultatul.','Am răspuns la întrebarea inițială și am explicat o limită concretă.','Am indicat sursele efectiv folosite și lângă tabele sau grafice.','Am realizat cercetarea online fără sondaj propriu sau interviuri.','Am eliminat ghidul și toate câmpurile necompletate din șablon.','Am verificat încadrarea în aproximativ 10 minute.','Predau un PPTX editabil cu texte și grafice lizibile.']
    checklist='<ol style="padding-left:24px;margin:0;">'+''.join('<li style="margin:0 0 12px;"><label style="display:flex;align-items:flex-start;gap:12px;min-height:44px;padding:8px 0;cursor:pointer;"><input type="checkbox" style="width:20px;height:20px;flex:0 0 20px;margin:4px 0 0;accent-color:'+INK+';"/><span>'+fmt(x)+'</span></label></li>' for x in checks)+'</ol>'
    checklist+=p('Salvați fișierul cu numele: Lucrare individuală — [Titlul temei] — [Nume Prenume].pptx. Păstrați obiectele principale editabile. O fotografie poate fi imagine. Ea nu înlocuiește întregul diapozitiv. Predați PPTX și nu numai o copie PDF.')
    sections.append(('predare','5. Verificare înainte de prezentare',card(checklist)))
    download='https://raw.githubusercontent.com/AL862/SemMicroE/refs/heads/main/'+quote(FOLDER+'/'+PPTX_NAME,safe='/')
    sections.append(('sablon-pptx','6. Șablonul editabil pentru lucrarea individuală',p('Descărcați șablonul și completați-l conform temei alese. Modificați sau uniți diapozitivele dacă explicația devine mai clară. Eliminați ghidul de la final înainte de predare.')+'<a class="individual-download" href="'+download+'" style="display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:12px 18px;border-radius:12px;background:'+INK+';border:1px solid '+INK+';color:#FFFFFF;font-size:16px;line-height:1.4;text-decoration:none;font-weight:700;">Descarcă șablonul PPTX ↓</a>'))
    root='<div data-individual-work lang="ro" style="width:100%;max-width:1050px;margin:0 auto;padding:12px;box-sizing:border-box;font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.6;color:'+TEXT+';background:#FFFFFF;overflow-wrap:break-word;">'
    root+='<style>[data-individual-work] *{box-sizing:border-box}[data-individual-work] p:last-child{margin-bottom:0!important}[data-individual-work] :focus-visible{outline:3px solid #1F6388;outline-offset:3px}[data-individual-work] section{scroll-margin-top:20px}[data-individual-work] summary::marker{color:#123B5D}[data-individual-work] sub,[data-individual-work] sup{font-size:75%;line-height:0}</style>'
    root+='<header data-course-header="compact" style="background:linear-gradient(135deg,#123B5D,#1F6388);color:#FFFFFF;padding:16px 20px;border-radius:12px;margin-bottom:24px;"><div style="font-size:14px;letter-spacing:1.2px;text-transform:uppercase;line-height:1.5;margin:0 0 6px;">Microeconomie · ASEM</div><h1 style="margin:0;font-size:24px!important;line-height:1.3;font-weight:700;color:#FFFFFF;">Lucrări individuale pentru studenți</h1></header>'
    root+=card(p('Alegeți o întrebare economică și construiți un răspuns propriu. Folosiți informații accesibile online într-un exemplu clar. Explicați mecanismul și arătați ce susțin datele și ce depinde de ipoteze.'))
    root+='<nav id="cuprins" aria-label="Cuprins" style="padding:16px;border:1px solid '+BORDER+';background:'+SURFACE+';border-radius:12px;margin:24px 0;">'+h3('Alegeți secțiunea')+'<div style="display:flex;flex-wrap:wrap;gap:8px;">'
    for (id,title),label in zip([(x[0],x[1]) for x in sections],['Organizarea lucrării','33 de teme','Conținutul diapozitivelor','Surse și utilizarea datelor','Verificare finală','Șablon PPTX']):
        root+='<a href="#'+id+'" style="display:flex;align-items:center;flex:1 1 240px;min-width:0;min-height:48px;padding:12px;border:1px solid '+BORDER+';border-radius:12px;background:#FFFFFF;color:'+INK+';font-size:16px;line-height:1.45;text-decoration:none;">'+fmt(label)+'</a>'
    root+='</div></nav>'
    for id,title,body in sections:root+='<section id="'+id+'" style="margin:32px 0 0;min-width:0;">'+h2(title)+body+back_link()+'</section>'
    root+='<nav aria-label="Navigarea cursului" style="display:flex;flex-wrap:wrap;gap:8px;margin:32px 0 0;padding-top:20px;border-top:1px solid '+BORDER+';"><a href="https://moodle.ase.md/course/view.php?id=4708" style="display:inline-flex;align-items:center;min-height:48px;padding:12px 18px;border:1px solid '+INK+';border-radius:12px;color:#FFFFFF;background:'+INK+';font-size:16px;line-height:1.4;text-decoration:none;">Toate seminarele →</a></nav>'
    root+='<footer style="margin-top:24px;color:'+MUTED+';font-size:14px;line-height:1.5;">ASEM · Microeconomie · Lucrări individuale pentru studenți</footer>'
    root+='<script>(function(){const root=document.currentScript.closest("[data-individual-work]");const controls=root.querySelector("[data-disclosure-controls]");controls.style.display="flex";controls.querySelectorAll("[data-expand]").forEach(button=>button.addEventListener("click",()=>{const state=button.dataset.expand==="true";root.querySelectorAll("details").forEach(item=>{item.open=state;});}));})();</script></div>'
    # Native details and checkboxes remain usable when Moodle removes scripts.
    target=repo/FOLDER/HTML_NAME;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(root,encoding='utf-8')
    print(target)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,default=ROOT.parents[1]);parser.add_argument('--course-tools',type=Path);args=parser.parse_args()
    render(args.repo_root,args.course_tools or args.repo_root/'tools/moodle-course')
