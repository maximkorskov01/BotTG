# Проект: Квиз-бот + AI обработка текста

В репозитории добавлен модуль `ai_text` для простой обработки текста на Python:
- суммаризация (extractive)
- анализ тональности (VADER)

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Использование CLI

Суммаризация (из файла):
```bash
python -m ai_text.cli summarize --file input.txt --max-sentences 3 --min-chars 30
```

Суммаризация (через stdin):
```bash
echo "Ваш текст..." | python -m ai_text.cli summarize
```

Анализ тональности:
```bash
echo "Этот текст мне очень нравится!" | python -m ai_text.cli sentiment
```

## Встраивание в код

```python
from ai_text import TextProcessingPipeline

pipeline = TextProcessingPipeline(max_summary_sentences=3, min_sentence_characters=30)
summary = pipeline.summarize("Длинный текст для суммаризации ...")
sentiment = pipeline.sentiment("Текст для анализа тональности ...")
```

## Прежняя функциональность бота

Команды бота для квиза остаются без изменений:
- /start — запуск квиза
- /help — помощь
- /quiz — начало игры

Бот проводит интерактивный квиз с 15 вопросами, по итогам показывает результат и сохраняет его.
