# Article Summarizer Bot

A Python web-scraping pipeline that extracts article content from arbitrary URLs and produces a short summary via Google's Gemini API. A Telegram interface is being added next so users can drop a link into a chat and get a summary back.

## What it does

1. **Scrape** — fetches the page with `httpx` (async, with retries) and pulls the main text using BeautifulSoup. Falls back from `<article>` tags to `<p>` paragraphs when the page has no semantic markup.
2. **Normalize** — trims content over 100 000 characters and surfaces explicit warnings when a page has nothing extractable.
3. **Summarize** — sends the cleaned text to Gemini with a fixed prompt: 3–5 sentence summary plus a short bullet list, in the article's original language.
4. **Deliver** *(in progress)* — a Telegram bot wrapper so summaries can be requested from a chat.

## Stack

- Python 3.13, [uv](https://github.com/astral-sh/uv) for dependency management
- `httpx` (async HTTP client) + `beautifulsoup4` (HTML parsing)
- `google-genai` (Gemini API)
- `python-telegram-bot` *(integration in progress)*

## Running locally

```bash
# 1. install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. install deps
uv sync

# 3. set your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. run
uv run main.py
```

Edit `url` in `main.py` to point at the article you want summarized.

## Project layout

```
content_generation.py   # web scraper (httpx + BeautifulSoup, with retries)
ai.py                   # Gemini client + prompt
main.py                 # entry point — wires scraper -> summarizer
```

## Status

- [x] Web scraper with retries and content-length guard
- [x] Gemini summarization with language preservation
- [ ] Telegram bot interface
- [ ] Persistent storage of summaries
