# Fix: Moodle reports unknown backup format

The user reported `Format necunoscut de backup` for the generated backups.

## Confirmed cause

The original generator used Python ElementTree's declaration:

```xml
<?xml version='1.0' encoding='utf-8'?>
```

It is valid XML. However Moodle's `convert_helper::detect_moodle2_format` searches the first200bytes for a literal XML declaration with double quotes, plus `<moodle_backup>` and `<information>`. Encoding case is ignored; the quote style is not.

Source inspected: [Moodle convert_helper.class.php](https://github.com/moodle/moodle/blob/main/public/backup/util/helper/convert_helper.class.php), method `detect_moodle2_format`. The normal Moodle backup detector delegates to this method.

The generator now writes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

All11MBZ and11question-bank XML files have been rebuilt. Archive indexes and their byte lengths were regenerated. Questions, answer keys and timings are unchanged.

## Validation

- The uploaded original passes the ported Moodle signature algorithm.
- All11previous generated metadata documents fail it despite being well-formed XML.
- All11rebuilt activity backups pass it.
- Five regression tests cover the generated header, old valid-but-unrecognized XML, original-style header, ordinary question XML rejection as a backup and the200byte read limit.
- Full archive/index/ID validation and XML-to-MBZ question/answer parity checks pass again for all275questions.
- This is a faithful port of the inspected signature algorithm. PHP Moodle restore itself was not executed on the user's server; successful activity restoration is not claimed.

## Correct upload screen

- Realtime Quiz MBZ: `Restaurare / Restore` in the course.
- Ordinary question-bank XML: `Banca de întrebări → Import → Moodle XML`. Ordinary `<quiz>` XML is not an activity backup and must not be sent to Restore.

After pulling the fix, upload the new local MBZ. A file that was selected or uploaded before the update can still refer to the previous backup in Moodle's file picker; replace it with the new file.

Regression command:

```bash
python3 tools/moodle-quizzes/test_format_detection.py
```
