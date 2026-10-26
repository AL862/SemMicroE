# Generarea prezentărilor

Sursele sunt păstrate separat de fișierele PPTX și DOCX pentru încărcare. `specs.py` definește cele 11 exemple și textele vizibile. `make_plan.py` preia explicații din datele seminarului și construiește notele lectorului. `render.py` construiește infografice HTML/SVG. `build.py` integrează imaginile și notele în PPTX și generează DOCX.

Din rădăcina proiectului:

```bash
python -m pip install -r tools/seminar-presentations/requirements.txt
python tools/seminar-presentations/make_plan.py
python tools/seminar-presentations/build.py
python tools/seminar-presentations/finalize_and_validate.py
```

Generatorul folosește Chromium la `/usr/bin/chromium` și fontul Arial disponibil în mediul de construire. Dacă executabilul este instalat în alt loc modificați `executable_path` în `build.py`. Rezultatele sunt scrise în `[3] Prezentări pentru seminare`. Copiile PNG pentru verificare rămân în `tools/seminar-presentations/rendered` și sunt excluse din Git.

Pentru verificarea lingvistică locală cu distribuția LanguageTool 6.6:

```bash
python tools/seminar-presentations/proofread.py --jar /cale/LanguageTool-6.6/languagetool-commandline.jar
```

Nu se trimit texte către un serviciu extern. Rezultatele lingvistice necesită interpretare manuală. Formulele și numele economiștilor pot produce avertizări de dicționar.

După modificări verificați vizual fiecare diapozitiv și actualizați rapoartele din `docs/seminar-presentations`. Verificarea structurală nu înlocuiește proba în PowerPoint pe calculatorul de prezentare.
