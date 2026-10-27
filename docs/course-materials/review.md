# Reorganizare și materiale comune

Resursele sunt în `[0] ★ Resurse`. Cele 12 scanuri sunt în `Tomșa/Manual`. Cartea Mankiw este în `Cărți`. Mutările reutilizează obiectele Git originale fără recomprimarea PDF-urilor.

`[5] Materiale pentru curs` reunește bibliografia și glosarul complet. `[6] Materiale și informații pentru profesor` conține HTML-ul soluțiilor și cele 11 conspecte Word mutate din folderul prezentărilor. Vechile PDF/DOCX de soluții sunt păstrate într-o arhivă separată. Cele 11 foldere vechi ale seminarelor sunt eliminate. Directorul vechi al imaginilor era format din instrucțiuni și directoare goale. Instrucțiunile lui sunt arhivate în Resurse. Pictogramele folosite efectiv de generatoare rămân în `tools/seminar-presentations/assets`.

## Bibliografie

Au fost consultate listele de lecturi de la finalul scanurilor disponibile. `scan-bibliographies.json` păstrează textul OCR și pagina PDF pentru fiecare listă. Pagina finală a seminarului 9 și cea a seminarului 11 au fost verificate și vizual. Lista consolidată conține 40 de cărți și trei referințe contabile istorice. Pentru edițiile cu informație incompletă nu s-a inventat un ISBN.

ISBN-urile afișate au trecut verificarea sumei de control. Metadatele au fost confruntate cu surse editoriale și universitare și cu pagina de copyright a cărții locale Mankiw. Câteva exemple:

- [Publicațiile ASEM](https://old.ase.md/facultatea/egd/departament/tpe/cadre-didactice/publicatii.html)
- [Publicațiile Tatianei Bucos](https://tpe.ase.md/files/tpe/profi/Bucos_CV_en.pdf)
- [Catalogul Editurii Sedcom Libris](https://editurasedcomlibris.ro/carte/micro-si-macroeconomie-concepte-fundamentale-si-aplicatii-9789736700330)
- [Ștefan și Dogaru — pagina editorului](https://www.editurauniversitara.ro/stiinte-economice-3/microeconomie-teorie-si-aplicatii-practice.html)
- [OpenStax — pagina de copyright și ISBN digital](https://assets.openstax.org/oscms-prodcms/media/documents/Microeconomics3e-WEB.pdf)

Corecții de identificare: autorii Ignat și Lutac sunt indicați împreună. Pentru Stratan și Cucu s-a folosit descrierea ASEM din 2011 în locul anului 2010 din lista scanată. Cartea Vîrjan nu este atribuită lui Varian. Pentru Mankiw ediția din 2007 este a patra și nu a cincea. Cartea Friedman a fost identificată cu anul 1986. Pentru Stiglitz și Walsh s-a păstrat ediția românească din 2005 și nu combinația inconsistentă „fifteenth edition — McGraw-Hill — 1995”. La Ștefan și Dogaru s-a folosit lista de autori publicată de editor. ISBN nu este transferat unei alte ediții. Titlurile bibliografice păstrează semnele lor de punctuație chiar dacă explicațiile didactice ale cursului sunt redactate fără virgule.

Unele date editoriale din vechile liste rămân confirmate numai prin sursa scanată. Lipsa unui ISBN la acele poziții este intenționată. Lista nu prezintă toate metadatele drept verificate în catalogul editurii.

## Glosar

Copia încărcată conținea trei categorii și zero termeni. Au fost redactate 141 de definiții cu exemple pentru 11 seminare. HTML și XML și MBZ folosesc același set de înregistrări. Structura importului și a restaurării a fost confruntată cu codul public Moodle:

- [Export și import glosar](https://github.com/moodle/moodle/blob/main/public/mod/glossary/lib.php)
- [Structura backup](https://github.com/moodle/moodle/blob/main/public/mod/glossary/backup/moodle2/backup_glossary_stepslib.php)
- [Restaurarea activității](https://github.com/moodle/moodle/blob/main/public/mod/glossary/backup/moodle2/restore_glossary_stepslib.php)

Înregistrările sunt procesate de restaurare numai cu setarea `userinfo`. Arhiva generată o activează și nu include conturi personale. XML-ul este varianta recomandată pentru importul în glosarul deja existent. Nu a fost executată restaurarea efectivă în instanța Moodle autentificată.

## Soluții și verificare

HTML-ul profesorului conține condițiile și cerințele curente pentru 52 de probleme rezolvate și 110 probleme noi. Soluțiile problemelor noi au trei pași explicativi și concluzie economică. S-au verificat relațiile și ipotezele economice. Verificatorul independent existent a trecut cele 59 de calcule și optime ale problemelor-sursă. Condițiile curente au fost comparate cu cele 11 fișiere JSON publicate în GitHub înainte de construire.

Paginile folosesc stilul comun al cursului și nu încarcă fonturi sau biblioteci externe. Codul JavaScript efectiv generat a fost executat în Node cu metadatele tuturor înregistrărilor: căutare fără diacritice și filtru pe seminar și resetare și deschidere/închidere. Au fost verificate și căutarea după `s06-p05` și starea fără rezultate.

Verificarea vizuală Chromium a fost blocată de restricția `setsockopt EPERM` a mediului. Nu se afirmă o verificare vizuală la patru lățimi sau testarea paginilor după inserarea în Moodle. Verificarea JavaScript este separată de randarea browserului.

LanguageTool 6.6 a fost rulat local în limba română pe textul celor trei pagini. Marcajele HTML inline și entitățile matematice sunt păstrate corect. Avertizările despre formule și nume bibliografice au fost revizuite separat de gramatică. Rapoartele consemnează rezultatele efective și limitele verificării.

Generatorul PPTX și manifestul prezentărilor au fost actualizate pentru noua locație a DOCX-urilor. Scriptul importului original păstrează fișierele actualizate și nu recreează variantele arhivate. Acest script PowerShell nu a fost executat pe calculatorul utilizatorului.
