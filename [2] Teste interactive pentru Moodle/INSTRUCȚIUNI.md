# Teste interactive pentru Moodle

11 teste × 25 de întrebări = 275 de întrebări. Fiecare întrebare are patru variante și un singur răspuns corect. Numele activităților și fișierelor urmează modelul `Test interactiv - Seminarul 6. Costurile de producție`.

## Realtime Quiz: fișierele MBZ

Fișierele `.mbz` sunt copii de siguranță ale unor activități Realtime Quiz. Ele nu se importă în banca de întrebări a testului standard.

1. Descărcați fișierul MBZ al seminarului.
2. În cursul Moodle deschideți `Reutilizarea cursului → Restaurare` / `Course reuse → Restore` și încărcați fișierul.
3. Alegeți restaurarea în cursul existent cu păstrarea conținutului existent. Adăugați activitatea nouă; nu selectați ștergerea conținutului cursului.
4. Verificați destinația și confirmați restaurarea. Mutați activitatea în secțiunea seminarului dacă este necesar.
5. Deschideți activitatea și verificați cele 25 de întrebări și timpul înainte de folosirea cu studenții.

Este necesar modulul `mod_realtimequiz` instalat. Șablonul provine din copia de siguranță furnizată de utilizator pentru Moodle 5.2.2 și Realtime Quiz cu versiunea de modul 2026042400. Pachetul nu instalează acest modul.

Fiecare întrebare Realtime Quiz are 25 de secunde. Nu există excepții pentru întrebările numerice. Eticheta are forma „Întrebarea 3 / 25”. Ordinea întrebărilor și variantelor este pregătită în fișier.

## Testul standard Moodle: fișierele XML

Subfolderul `Import întrebări Moodle XML` conține aceleași275 de întrebări în format Moodle XML.

1. În curs deschideți `Banca de întrebări → Import` / `Question bank → Import`.
2. Selectați formatul `Moodle XML` și încărcați XML-ul seminarului.
3. Verificați categoria `Microeconomie / Seminarul N. Titlul temei`. Sunt25 de întrebări de tip alegere multiplă cu un singur răspuns corect.
4. Creați un test standard cu numele seminarului. Din banca de întrebări adăugați toate cele25 de întrebări în ordinea lor numerică.
5. Păstrați dezactivată amestecarea întrebărilor și variantelor pentru a păstra distribuția pregătită a literelor corecte.

Importul XML adaugă întrebări în bancă. Nu creează singur activitatea Test. Timpul individual al întrebărilor Realtime Quiz nu se transferă prin acest format; configurați limita generală de timp în testul standard dacă este necesar.

## Conținut și verificări

Baza principală: `Subiecte de recapitulare`, exercițiile rezolvate și concluziile seminarului. Fiecare test include și trei situații aplicate de extindere. Întrebările sunt adaptate pentru răspuns scurt. Răspunsurile corecte vecine au litere diferite; fiecare literă apare de 6–7 ori într-un test.

Cheile și legăturile de lucru cu secțiunile cursului sunt în `docs/moodle-tests/` din rădăcina depozitului. Ele nu sunt introduse în HTML-ul întrebării. Răspunsul corect este înregistrat în câmpurile Moodle pentru evaluare.

Arhivele, XML-ul, cheile și calculele au fost verificate local. Restaurarea pe serverul Moodle al utilizatorului nu a fost executată din acest mediu. Verificați prima activitate restaurată înainte de folosirea la curs.

## Dacă apare „Format necunoscut de backup”

Fișierele MBZ au fost corectate după identificarea unei incompatibilități a declarației XML cu detectorul Moodle. Actualizați depozitul și selectați din nou fișierul local actualizat. Înlocuiți fișierul vechi deja încărcat în selectorul Moodle. Pentru XML folosiți Import în banca de întrebări și nu Restaurare.
