# Academic Research Skills

В проект подключён запрошенный [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills), версия3.23.2, коммит`1ec249df98728682dfbbdfb940a658338bfd6f80`.

Автор: Cheng-I Wu. Лицензия: [Creative Commons Attribution-NonCommercial4.0 International](../third-party/academic-research-skills/LICENSE). Исходные файлы не изменены. Подмодуль сохраняет автора, лицензию, справочники, скрипты и историю выбранной версии.

## Что подключено

- `.agents/skills/academic-paper-reviewer` → `../../third-party/academic-research-skills/academic-paper-reviewer`
- `.agents/skills/academic-paper` → `../../third-party/academic-research-skills/academic-paper`
- `.agents/skills/academic-pipeline` → `../../third-party/academic-research-skills/academic-pipeline`
- `.agents/skills/deep-research` → `../../third-party/academic-research-skills/deep-research`
- `.agents/skills/sr-screener` → `../../third-party/academic-research-skills/sr-screener`

Имена не пересекаются с существующими навыками. Общие правила курса остаются в microeconomics-seminar. Перед использованием импортированного навыка читать его SKILL.md и указанные справочники. Подключение не означает, что все пять процедур применялись к уже опубликованным семинарам.

## Инициализация

Из корня локального клона:

```bash
git submodule update --init third-party/academic-research-skills
```

Затем переоткрыть проект в агенте с поддержкой .agents/skills. Нужна поддержка символических ссылок в Git/ОС; на Windows можно использовать WSL. Проверка:

```bash
git -C third-party/academic-research-skills rev-parse HEAD
python3 -c 'from pathlib import Path; names=["academic-paper-reviewer","academic-paper","academic-pipeline","deep-research","sr-screener"]; [print(n, (Path(".agents/skills")/n/"SKILL.md").is_file()) for n in names]'
```

## Границы подключения

Это исходная сборка для Claude Code. В текущем подключении доступны файлы методик, а Claude Code hooks, slash-команды, ограничения инструментов и многoагентная координация автоматически не запускаются. Upstream [CONTROL_AVAILABILITY.md](../third-party/academic-research-skills/docs/CONTROL_AVAILABILITY.md) описывает различия каналов установки. Upstream также рекомендует отдельную [сборку для Codex CLI](https://github.com/Imbad0202/academic-research-skills-codex); она не подменяет здесь запрошенный репозиторий.

Новый MCP-сервер или встроенный плагин ChatGPT этим коммитом не зарегистрирован. Зависимости и внешние API на этапе подключения не запускались. Подключение проверено по зафиксированному дереву и разрешению всех пяти ссылок.
