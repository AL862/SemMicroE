# Навыки агента и завершение переноса материалов

## Подключённые наборы

- [AgentMemory](https://github.com/rohitg00/agentmemory/tree/c5b8ebfb32eb6a08fe301d3bb75840f3597b66c8): 17 навыков, подмодуль `third-party/agentmemory`.
- [Scientific Agent Skills](https://github.com/k-dense-ai/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62): 177 навыков, подмодуль `third-party/scientific-agent-skills`.

Версии зафиксированы коммитами в Git. Ссылки в `.agents/skills/` направлены на исходные папки навыков в подмодулях вместе с их скриптами, справочниками и лицензиями. Обновление подмодулей требует отдельного коммита; автоматического перехода на новые версии нет.

Для Codex CLI или другого агента с поддержкой `.agents/skills/` клонируйте проект с подмодулями:

```bash
git clone --recurse-submodules https://github.com/AL862/SemMicroE.git
cd SemMicroE
```

В существующем клоне:

```bash
git submodule update --init --recursive
```

Используйте Linux, macOS или WSL для символических ссылок. На Windows Git должен поддерживать создание символических ссылок; обычная загрузка ZIP с GitHub не загружает подмодули. После инициализации откройте проект заново в агенте и проверьте список навыков. Зависимости конкретных научных навыков устанавливаются по их инструкциям по мере использования.

## AgentMemory

В `.codex/config.toml` настроен MCP-мост `@agentmemory/mcp@0.9.31`. Для полноценной памяти нужен отдельный работающий сервер и Node.js 20+. В терминале той же системы, где работает агент:

```bash
npx -y @agentmemory/agentmemory@0.9.31
```

Следуйте первоначальной настройке и выберите режим без API-ключей, если внешний провайдер не требуется. Сервер по умолчанию использует REST/MCP на `localhost:3111` и интерфейс на `localhost:3113`. После запуска перезапустите агент и проверьте подключение MCP. Данные памяти хранятся отдельно от репозитория; не публикуйте секреты или базу памяти.

В текущем чате ChatGPT новый MCP-сервер не зарегистрирован и сохранение памяти не проверено. Файлы в репозитории подключают эти возможности к совместимому клиенту после локальной настройки.

## Материалы курса

Исходник: `H:\Gdisk\ASEM\Seminare la Microeconomie` (Google Drive, папка ASEM).

Снимок содержит 62 файла, 240040357 байт. Перечень, размеры и Git SHA-1 оригиналов находятся в `tools/course-files.json`. Четыре пустые папки сохранены файлами `.gitkeep`.

В момент подготовки уже опубликованы и проверены 54 файла. Ещё 8 крупных файлов требуют завершения переноса: GitHub Actions отключён на уровне аккаунта, а подключение ChatGPT ограничивает размер одного запроса. Ограничение относится к подключению; сами файлы меньше лимита GitHub 100 МиБ.

### Завершить перенос с Windows без Actions

Установите Git for Windows, откройте PowerShell и выполните в удобной папке:

```powershell
git clone https://github.com/AL862/SemMicroE.git
cd SemMicroE
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Complete-CourseImport.ps1 -SourcePath 'H:\Gdisk\ASEM\Seminare la Microeconomie'
```

Если клон уже существует, используйте актуальную ветку `main`. Скрипт сначала проверяет наличие, размер и контрольную сумму всех 62 оригиналов, затем копирует файлы с сохранением структуры, создаёт коммит и выполняет обычный `git push`. При необходимости Git откроет вход в GitHub. Скрипт не переписывает историю.

Скрипт подготовлен, но не запускался на вашем компьютере. При отличии локального файла от проверенного снимка он остановится до копирования. После успешной загрузки счётчик материалов можно проверить по `tools/course-files.json`.

Ограничение GitHub Actions снимает [поддержка GitHub](https://support.github.com/); для этого способа загрузки Actions не нужен.

## Правила формирования семинаров

Корневые README.md и README.txt заменены шестью предметными навыками: microeconomics-seminar, microeconomics-moodle, microeconomics-presentations, microeconomics-teacher-notes, microeconomics-interactive-tests и microeconomics-individual-work. Седьмой локальный навык languagetool-proofreading отвечает за языковую проверку.

Начинать с [.agents/skills/microeconomics-seminar/SKILL.md](.agents/skills/microeconomics-seminar/SKILL.md). Полный текст исходных инструкций сохранён без изменения в [.agents/skills/microeconomics-seminar/references/course-rules.txt](.agents/skills/microeconomics-seminar/references/course-rules.txt); указатель разделов находится рядом. Исторические упоминания README.txt внутри полного справочника означают это новое расположение.

Манифест переноса сохраняет 62 исходных записи. Для бывшего README.txt указан source_path; скрипт переносит его в справочник навыка и не восстанавливает корневой README.txt.

## LanguageTool

Подключён подмодуль third-party/languagetool. Настройка и команда проверки описаны в [docs/languagetool.md](docs/languagetool.md). Подключение исходников не подтверждает работающий сервер: для реальной проверки нужен локальный LanguageTool на порту 8081.
