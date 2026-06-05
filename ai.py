from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_summary(article: str) -> str:
    """
    Generate summary with bullet points.
    
    Args:
        article: article we want to summarize.
    
    Returns:
    Summarized text with bullet points list.
    If there is issue connecting to the language model, returns a message with explanation of what happened.
    """


    if "Warning" in article:
        return "No content to summarize"

    prompt = f"""You are article assistant. 
Your main task is to summarize given article and make simple points from it.
You should follow a format of 3-5 sentences with a short bullet point list.
You should write the summary in the language of the article.
Article to summarize: {article}"""

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error: content did not generate. {str(e)}"
