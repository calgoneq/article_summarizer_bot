import httpx
import asyncio
from bs4 import BeautifulSoup

async def get_content(url: str, retries: int = 3) -> str:
    """
    Fetch a URL and extract its main text content.
    
    Args:
        url: link to a website from which you want to extract the content.
        retries: number of times the function will try to get the data from the website.
    
    Returns:
    Extracted text from the website.
    If the text is too long it returns first 100 000 characters.
    If there is issue connecting to the website or there is nothing to extract, returns a message with explanation of what happened.
    """
    
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                articles = soup.find_all("article")

                if len(articles) == 0:
                    paragraphs = soup.find_all("p")
                    if len(paragraphs) != 0:
                        content = [p.get_text() for p in paragraphs]
                        content = "\n".join(content)
                        if len(content) > 100000:
                            print("Warning: Content to long limiting to first 100 000 characters!")
                            content = content[:100000]
                            return content
                        else:
                            return content
                    else:
                        return "Warning: Not enough content!"
                
                else:
                    content = [article.get_text() for article in articles]
                    content = "\n".join(content)
                    if len(content) > 100000:
                        print("Warning: Content to long limiting to first 100 000 characters!")
                        content = content[:100000]
                        return content
                    else:
                        return content
         
            except httpx.HTTPError as exc:
                print(f"Error: {exc}. Try {attempt + 1}/{retries}.")
                if attempt < retries - 1:
                    print("Waiting 5 seconds before trying to get the data again!")
                    await asyncio.sleep(5)
                else:
                    return f"Error: failed to get data after {retries} retries: {exc}"