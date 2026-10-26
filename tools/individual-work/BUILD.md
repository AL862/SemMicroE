# Actualizarea instrucțiunii pentru lucrări individuale

`topics.json` conține cele 33 de teme. Fiecare înregistrare precizează seminarul și titlul și trei paragrafe de cerință. Titlurile primelor 15 teme se păstrează la actualizările de stil.

`build.py` aplică standardul comun al cursului și reutilizează componentele de buton din `tools/moodle-course/components.py`. În rădăcina proiectului:

```bash
python tools/individual-work/build.py
```

Rezultatul este scris în `[4] Lucrări individuale pentru studenți/Instrucțiune — Lucrări individuale pentru studenți.html`. Generatorul nu modifică șablonul PPTX. Păstrați instrucțiunea și șablonul împreună în acest dosar.

Fișierul HTML este un fragment pentru inserare în conținutul paginii Moodle. Stilurile esențiale sunt inline. Temele folosesc elemente native `details`. Butoanele de deschidere generală apar numai dacă scriptul paginii poate rula. La eliminarea scriptului temele rămân accesibile individual.

La modificarea unei teme precizați cum se folosesc datele selectate în studiul de caz și în calcule sau comparații. Sursele nu se adaugă ca decor. Verificați din nou cele trei teme pentru fiecare dintre cele 11 seminare și comparați rezultatul cu șablonul și cerințele de diapozitive.
