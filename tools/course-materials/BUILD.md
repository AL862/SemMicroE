# Generarea materialelor comune

Datele sunt în `glossary.json` și `bibliography.json` și `new-solutions.json`. Condițiile problemelor provin din `tools/moodle-course/data`. Soluțiile de aici nu modifică paginile studenților.

Din rădăcina proiectului:

```bash
python tools/course-materials/build.py
```

Rezultatele sunt scrise în `[5] Materiale pentru curs` și `[6] Materiale și informații pentru profesor`. Șablonul MBZ original se află în `template/glossary-source.mbz`.

Structura XML de import este `GLOSSARY/INFO/ENTRIES/ENTRY`. Arhiva MBZ folosește structura activității `glossary` din copia furnizată și păstrează declarația XML cu ghilimele duble necesară detectării Moodle.

La schimbarea unui termen regenerați împreună HTML și XML și MBZ. La schimbarea unei probleme verificați condiția din curs și soluția și numerotarea. După reorganizare nu recreați vechile foldere Seminarul 1–11.
