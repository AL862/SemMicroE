---
name: microeconomics-moodle
description: Создание и редактирование Moodle HTML для семинаров Microeconomie ASEM. Использовать для страниц NN_Seminarul_N_Moodle.html, задач, SVG-графиков, раскрывающихся блоков и навигации курса.
metadata:
  version: "1.0"
---

# Moodle-страница семинара

Сначала прочитать [общие правила](../microeconomics-seminar/SKILL.md) и разделы 0–11, 14–15, «Единая структура построения задач», «Пагинация» и 17.9 в [полном справочнике](../microeconomics-seminar/references/course-rules.txt).

1. Прочитать текущий HTML и соответствующие источники. За основу оформления брать Seminarul 2 / MASTER Moodle template. Имя файла строго NN_Seminarul_N_Moodle.html.
2. Сохранять начало: Microeconomie · ASEM → Seminarul N → тема → Descrierea seminarului.
3. Разделы 1–5: Obiectivele seminarului; Bazele teoretice ale seminarului; Formule principale și algoritmi; Exemple de probleme rezolvate în cadrul seminarului; Probleme pentru rezolvare.
4. Далее сохранять имеющиеся разрешённые Întrebări de verificare, Adevărat/Fals и Teste grilă. Не добавлять их ради одинакового числа разделов. Не включать studii de caz, sarcini analitice или темы рефератов.
5. Завершение: Concluzii esențiale → Materiale seminarului → навигация. Нумеровать разделы последовательно. В Materiale seminarului разрешена только подтверждённая ссылка скачивания финальной презентации текущего семинара. Если ссылки нет — оставить заголовок и пустое содержимое.
6. Решённая задача: Problemă → Date → Cerințe → Indicații pentru rezolvare → Rezolvare → Concluzie economică → при необходимости Tabel-sinteză и Exemplu practic. Каждое вычисление объяснить и интерпретировать.
7. Студенческая задача: Problemă → Date → Cerințe → Indicații pentru rezolvare → Concluzie economică cerută. Подсказки: 2–3 логических шага без числовых подстановок и ответов. При изменении задач синхронно обновить отдельный файл решений преподавателя.
8. В исходных проверочных блоках сохранять формулировки, порядок и визуальные задания. Ответы для самопроверки давать с объяснениями в зелёных раскрывающихся блоках. Это не разрешает решения в разделе 5.
9. Использовать настоящие sub/sup. Интерактивы — SVG + JavaScript с addEventListener, без inline onclick. Ключевые точки должны достигаться точно; при необходимости добавить кнопку точного значения. Проверить каждый элемент управления и динамический текст.
10. Раскрытие обычных информационных блоков: нативные details/summary; кнопки Deschide toate / Închide toate. Для прямой вставки в TinyMCE важные стили задавать inline внутри корневого div. Не полагаться только на style/head или внешние библиотеки. Для обычного раскрытия JS не нужен.
11. Проверять узкую колонку и телефон. Локальный предпросмотр не подтверждает отображение после сохранения в Moodle.
12. Навигация: предыдущий N−1 → единая страница курса → следующий N+1. Проверить подписи и взаимные переходы. Неизвестный адрес не угадывать: переход неактивен. Реестр подтверждённых URL находится в разделе 14 справочника. Авторизованный просмотр Moodle подтверждать только после реальной проверки.
