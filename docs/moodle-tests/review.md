# Moodle tests: build and review record

Date:2026-10-26. Course baseline:69f4f6982ec08330cab956cc263343977b423a65.

The release contains11 Realtime Quiz activity backups and11 ordinary Moodle question-bank XML files. Each format contains the same25 questions per seminar. Files and activity names follow the user's final naming instruction: `Test interactiv - Seminarul N. Titlul temei`.

The template is the user's uploaded `backup-moodle2-activity-142277-realtimequiz142277-20261026-1525-nu (1).mbz`. It declares Moodle 5.2.2 and module version 2026042400. Seminar5 preserves 21 questions from this example unchanged, adapts one numerical question and adds three applied replacements; source metadata for the retained numerical question points to the current solved seminar problem. Other tests adapt the current seminar's review concepts and solved problems. Each test has three applied extension questions.

Question provenance is recorded in `question-bank.json`: review sections are identified as a block rather than a claim of verbatim copying. For solved exercises the JSON pointer identifies the numbered problem. Author-created situations are marked as extensions. The source books and provenance are absent from student question HTML.

## Checks

- 275 questions;1100 answer choices; exactly one correct answer for each.
- Each test has25unique question texts and four distinct options per question.
- Each letter is correct6 or 7 times; adjacent correct letters differ. Seeded shuffling is reproducible. XML answer shuffling is disabled.
- MBZ and XML question texts and keys agree exactly. Question and answer IDs are unique within each activity backup.
- All XML parses. Every MBZ contains the expected Moodle backup paths. Archive index counts and byte lengths match the actual members. Activity/module references and names agree.
- User data are disabled. The template has no user responses or grades to copy.
- 81 numeric keys checked using independent exact-arithmetic calculations, including opportunity costs, market quantities, elasticities, cost identities, profits and HHI.
- Romanian LanguageTool6.6 CLI completed for all11 sets. Findings were inspected; names and mathematical abbreviations produce dictionary warnings. Zero grammatical errors is not claimed.
- HTML question cards checked at 320/390/768/1150px with Chromium. The question HTML has no external images or scripts.

Timing:30 seconds by default;60 seconds for questions containing numeric data. Realtime Quiz exports store per-question overrides. Standard Moodle XML does not transfer those timers.

No authenticated restore/import on moodle.ase.md was performed. Validation of archive/schema parity and local rendering is not a claim of successful server restoration. The top-level instructions distinguish restoring an activity from importing questions into the standard question bank.

## Rebuild

From the repository root with Python 3:

```bash
python3 tools/moodle-quizzes/build.py
python3 tools/moodle-quizzes/validate.py --repo-root .
python3 tools/moodle-quizzes/check_arithmetic.py --repo-root .
```

Authoring sources are `tools/moodle-quizzes/bank/N.txt`; format: basis marker, question, correct answer, three distractors separated by `|`. The builder reads current topic titles from `tools/moodle-course/data/N.json`. Template XML is retained under `tools/moodle-quizzes/template/` for reproducible packing. Existing source seminar HTML and PDF files are not replaced.
