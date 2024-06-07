import queue

import telegram
import requests
import json
import random
from telebot import TeleBot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Spoonacular API credentials
api_key = '780d0ac1e9ad48ae8921e4ed80444315'

# Telegram bot credentials
bot_token = '6229406413:AAGkHXGCMoXsTRRM-ILNgrZA6jgYmzZelcE'
bot = TeleBot(token=bot_token)

# Send a request to the Spoonacular API to get a random food image
def get_random_food_image():
    url = 'https://api.spoonacular.com/recipes/random?apiKey=' + api_key + '&number=1'
    response = requests.get(url)
    data = json.loads(response.text)
    return data['recipes'][0]['image']

# Send a message to the user with a food image and two inline buttons
def send_food_image_with_buttons(chat_id, photo_url):
    # Create the inline buttons
    recipe_button = InlineKeyboardButton('Recipe', callback_data='recipe')
    next_button = InlineKeyboardButton('Next', callback_data='next')
    inline_keyboard = [[recipe_button, next_button]]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    # Send the message with the food image and inline buttons
    bot.send_photo(chat_id=chat_id, photo=photo_url, reply_markup=reply_markup)

# Handle the inline button callbacks
def handle_inline_button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'recipe':
        # Send the recipe for the current food image
        recipe = get_random_food_recipe()
        bot.send_message(chat_id=chat_id, text=recipe)

    elif query.data == 'next':
        # Send the next random food image
        photo_url = get_random_food_image()
        send_food_image_with_buttons(chat_id, photo_url)

    # Edit the message to remove the inline buttons
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)

# Send a request to the Spoonacular API to get the recipe for the current food image
def get_random_food_recipe():
    url = 'https://api.spoonacular.com/recipes/random?apiKey=' + api_key + '&number=1'
    response = requests.get(url)
    data = json.loads(response.text)
    return data['recipes'][0]['instructions']

# Start the bot and listen for messages
def start_bot():
    print('Bot started...')
    updater = Updater(bot_token,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(handle_inline_button))
    updater.start_polling()
    while True:
        try:
            # Send a random food image with inline buttons
            chat_id = update.message.chat_id
            photo_url = get_random_food_image()
            send_food_image_with_buttons(chat_id, photo_url)
            updater.idle()
        except Exception as e:
            print(e)

# Start the bot
start_bot()
