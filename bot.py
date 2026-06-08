import asyncio
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from content_generation import get_content
from ai import generate_summary

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing or empty in the .env file!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Send me the link to your article and I will summarize it for you!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        url = update.message.text
        parsed = urlparse(url)
    
        if not parsed.scheme or not parsed.netloc:
            await update.message.reply_text("Send me only the link to the article, not a text!")
            return
        
        await update.message.reply_text("Thinking...")

        content = await get_content(url)
        if "Error: " in content:
            await update.message.reply_text("There was some error during content generation, please try again!")
            return
        summary = await generate_summary(content)
        await update.message.reply_text(summary)
    except Exception as e:
        await update.message.reply_text("There was an unexpected error! Sorry for the issue, try again later.")
        print(f"Error: {e}")
        return

def main():
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()