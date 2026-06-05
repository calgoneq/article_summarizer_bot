import asyncio

from content_generation import get_content
from ai import generate_summary

def main():
    url = "https://www.artificialintelligence-news.com/"
    url_quotes="https://quotes.toscrape.com/"
    url_exception = "https://www.artificialintelligence-news.com/news/microsofts-autopilot-scout-is-the-agentic-autopilot-that-works-across-m365/"
    data = asyncio.run(get_content(url_quotes))
    ai_summary = asyncio.run(generate_summary(data))
    print(ai_summary)

if __name__ == "__main__":
    main()