# write the code to connect with the telgram


#not working fix this

# importing the libraries
import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
#print(TELEGRAM_BOT_TOKEN)


# Initialize the login
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


# function
@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    """
    This handler receives messages with /start or  `/help `command
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Puja.")


#return the same message
@dp.message_handler()
async def echo(message: types.Message):
    """
    This will retrun echo
    """
    await message.answer(message.text)



if _name=="main_":
    executor.start_polling(dp,skip_updates=True)
