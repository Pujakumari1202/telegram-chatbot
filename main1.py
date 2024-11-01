# importing the library
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types
import openai
import sys


#load the openai api key and bot token
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

# Temporary memory
class Reference:
    '''
    A class to store previously response from the openai API

    '''

    def __init__(self)->None:
        self.reference=""

# initialize the reference
reference=Reference()
model_name="gpt-3.5-turbo"


# Initialize bot and dispatcher
bot =Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher=Dispatcher(bot)

# clear the previous conversation
def clear_past():
    """
    A function to clear the previous conversation and context.
    """

    reference.response=""


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """

    #call the clear function
    clear_past()
    await message.reply("I've cleared the past conversation and context.")




# create the first function
@dispatcher.message_handler(commands=['start'])
async def welcom(message: types.Message):
    
    """
    This handler receives message with '/start' or '/help' command
    """

    await message.reply("hi\nI an Tele Bot ! \Created by Puja. How can i assist you? ")





@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Telegram bot created by Puja! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


# main funtionality of the function



@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = model_name,
        messages = [
            # check it has any previous response or not
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content']  #getting the response
    print(f">>> chatGPT: \n\t{reference.response}")  # printing in my terminal
    await bot.send_message(chat_id = message.chat.id, text = reference.response)  #printing in my ui that means in my telegram


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)



#error