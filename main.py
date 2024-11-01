# Importing necessary libraries
from dotenv import load_dotenv
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import openai
import logging

# Load the OpenAI API key and bot token
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = OPENAI_API_KEY  # Set OpenAI API key

# Set up logging
logging.basicConfig(level=logging.INFO)

# Temporary memory class
class Reference:
    """A class to store the previous response from the OpenAI API."""
    def __init__(self) -> None:
        self.response = ""

# Initialize the reference
reference = Reference()
model_name = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Function to clear previous conversation
def clear_past():
    """Clears the previous conversation and context."""
    reference.response = ""

# Handlers
async def clear(message: Message):
    """Clear the previous conversation and context."""
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

async def welcome(message: Message):
    """Handle /start command to start the conversation."""
    await message.reply(r"Hi\nI am Tele Bot!\nCreated by Puja. How can I assist you?")

async def helper(message: Message):
    """Display the help menu."""
    help_command = """
    Hi there! I'm a Telegram bot created by Puja! Here are the commands:
    /start - Start the conversation
    /clear - Clear past conversation and context
    /help - Display this help menu
    """
    await message.reply(help_command)

async def chatgpt(message: Message):
    """Process user input and generate a response using the ChatGPT API."""
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "assistant", "content": reference.response},  # Assistant's previous response
            {"role": "user", "content": message.text}               # User's query
        ]
    )
    reference.response = response['choices'][0]['message']['content']  # Store the response
    print(f">>> ChatGPT: \n\t{reference.response}")  # Print response to terminal
    await bot.send_message(chat_id=message.chat.id, text=reference.response)  # Send response to Telegram

# Main function to start polling
async def main():
    # Register the handlers
    dp.message.register(welcome, Command(commands=["start"]))
    dp.message.register(clear, Command(commands=["clear"]))
    dp.message.register(helper, Command(commands=["help"]))
    dp.message.register(chatgpt)

    # Start polling
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
