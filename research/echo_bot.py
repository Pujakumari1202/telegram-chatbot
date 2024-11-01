# Frontend 
# Importing necessary libraries
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Ensure the bot token is loaded
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
# Initialize the dispatcher
dp = Dispatcher()

# Handler for start/help commands
async def command_start_handler(message: Message):
    """
    This handler receives messages with /start or /help command
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Puja.")

# Handler to echo messages
async def echo(message: Message):
    """
    This will return an echo of the received message
    """
    await message.answer(message.text)

# Main function to start polling
async def main():
    # Register the handlers
    dp.message.register(command_start_handler, Command(commands=["start", "help"]))
    dp.message.register(echo)

    # Start polling with the bot
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
