# Revizia prezentărilor 1–11

## Rezultat

11 fișiere PPTX în limba română. Fiecare are 10 diapozitive în format 16:9 și un plan orientativ de 11 minute. Toate cele 110 diapozitive au note integrate. Cele 11 conspecte DOCX reproduc aceleași note în aceeași ordine.

Structura comună: titlu și întrebare centrală → situație → concepte → mecanism → relație → grafic → confuzie frecventă → aplicație → soluție → idei de reținut. Nu există un diapozitiv separat pentru obiective. Fiecare prezentare deschide seminarul și lasă rezolvarea extinsă pentru activitatea de seminar.

| Seminar | Ideea centrală | Rezultatul aplicației |
|---|---|---|
| 1 | Costul de oportunitate | Încă 2 X sacrifică 10 Y |
| 2 | Echilibrul cererii și ofertei | P = 40 și Q = 60 |
| 3 | Elasticitatea punctuală | E d = −1 la P = 10 |
| 4 | Preferințe și buget | Coșul A oferă TU = 18 față de TU = 16 |
| 5 | Produs mediu și marginal | AP = 10 și MP = 2 |
| 6 | Total și medie | TC = 200 și ATC = 10 |
| 7 | Maximizarea profitului | Q = 20 și profit = 300 |
| 8 | Continuare sau oprire pe termen scurt | Pierdere 75 față de 100 prin oprire |
| 9 | Alegerea cantității și a prețului în monopol | Q = 20 și P = 60 |
| 10 | Diferențiere și profit | Q = 15 și profit = 250 |
| 11 | Răspunsuri optime simultane | Q1 = Q2 = 20 și profit 400 pentru fiecare |

## Metodă și surse de lucru

Conținutul pornește de la cele 11 seminare curente din `tools/moodle-course/data` și de la sursele deja verificate în etapa de reconstrucție a cursului. Exemplele au condiții complete. Nu sunt reproduse pagini dintr-un manual. Explicațiile și graficele sunt compuse în limba română pentru acest curs.

Au fost consultate prezentările anterioare 1–4 și catalogul `Microeconomie_Imagini_Comune.zip`. Pictogramele portofelului și fabricii sunt reutilizate fără regenerare. Fișierele sursă și amprentele lor se află în `tools/seminar-presentations/assets/catalog.json`.

Au fost aplicate regulile locale de seminar și prezentare și recomandările relevante din:

- `scientific-agent-skills`: scientific-slides și scientific-critical-thinking la versiunea fixată în submodul.
- `academic-research-skills`: verificarea afirmațiilor și separarea ipotezelor de concluzii.
- `ui-ux-pro-max-skill`: slides și ui-ux-pro-max la commitul `28b3b8dee8c976df4fa3e94aed4e092ad43fcb03`.
- LanguageTool 6.6 rulat local cu limba `ro` asupra textului sursă al diapozitivelor și asupra tuturor notelor.

Repere pedagogice consultate:

- [Gregory Mankiw — Teaching the Principles of Economics](https://mankiw.scholars.harvard.edu/publications/teaching-principles-economics)
- [Federal Reserve Bank of St. Louis — Keep Things Simple](https://www.stlouisfed.org/education/teach-economics-podcast-series/introducing-economics-to-students-keep-things-simple-greg-mankiw)
- [University of Michigan CRLT — Presentation Technology](https://crlt.umich.edu/tech-tools/presentation-technology)

Aplicare: explicație intuitivă înainte de formulă. Un singur exemplu numeric coerent leagă graficul de calcul. Întrebările scurte din note invită studenții să explice mecanismul. Stilul este original. Referințele rămân în documentația de lucru.

## Verificări efectuate

- 110 compoziții randate la 1920 × 1080 în Chromium. Verificări de geometrie pentru margini și depășiri. Toate au fost inspectate vizual în planșe de contact. Exemplele cu indici au fost reverificate separat după ajustarea spațierii.
- 88 imagini integrate comparate octet cu octet cu PNG-urile revizuite. Graficele au axe și unități. Exemplele folosesc aceleași funcții în grafic și în soluție.
- Diapozitivele 8 și 9 din fiecare PPTX conțin text și forme editabile. Conținutul lor a fost comparat cu planul.
- 110 pagini de note și 11 DOCX verificate față de planul sursă. Verificare ZIP/XML pentru fiecare PPTX și absența dependențelor externe.
- 31 calcule exacte verificate independent. Pentru Seminarul 11 sunt explicite alegerea simultană și costul fix zero. Pentru Seminarul 8 este precizat caracterul pe termen scurt al deciziei.
- LanguageTool: 11 rulări finalizate. După corectarea punctuației duble rămân 65 de avertizări de dicționar pentru simboluri și termeni precum Qd și Cournot și 5 sugestii stilistice privind repetarea începuturilor de propoziție. Au fost revizuite manual. Repetițiile care compară definiții au fost păstrate intenționat. Nu sunt erori de punctuație dublă rămase.
- Verificări ale regulilor locale pentru virgule și atribuiri de surse în notele lectorului.

`manifest.json` înregistrează SHA256 pentru cele 22 de fișiere finale. Celelalte rapoarte păstrează rezultatele verificărilor structurale și numerice.

## Limitele verificării

Nu a fost disponibilă aplicația Microsoft PowerPoint în mediul de construire. Cele 22 de diapozitive editabile au o previzualizare HTML cu aceeași geometrie și au fost verificate structural în PPTX. Randarea lor efectivă în PowerPoint și conexiunea HDMI trebuie probate pe calculatorul de prezentare. Cele 88 de diapozitive raster păstrează exact imaginea revizuită.

Vizualizarea prezentatorului necesită activarea funcției în PowerPoint și ecrane configurate în modul Extindere. F5 nu modifică setările ecranelor. Procedura este documentată în instrucțiunile pentru lector pe baza documentației Microsoft.
