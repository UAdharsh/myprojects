
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from telebot import TeleBot
# Enter your Spoonacular API key here
api_key = '780d0ac1e9ad48ae8921e4ed80444315'

# Create an instance of the Telegram bot
token = '6229406413:AAGkHXGCMoXsTRRM-ILNgrZA6jgYmzZelcE'
bot = TeleBot(token)

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Please enter the ingredients you have, separated by commas.")

# Define the message handler
def message(update, context):
    # Get the user's message
    ingredients = update.message.text

    # Send a typing message while the bot is fetching the recipe data
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)

    # Fetch the recipe data using the Spoonacular API
    response = requests.get(f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}&number=5')

    # Parse the JSON data
    data = json.loads(response.text)

    # Send the recipe data to the user
    for recipe in data:
        # Get the recipe image URL
        image_url = recipe['image']

        # Download the recipe image
        image_response = requests.get(image_url)
        with open('image.jpg', 'wb') as f:
            f.write(image_response.content)

        # Send the recipe image to the user
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.jpg', 'rb'))

        # Get the recipe title and source URL
        title = recipe['title']
        source_url = recipe['sourceUrl']

        # Send the recipe title and source URL to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=title)
        context.bot.send_message(chat_id=update.effective_chat.id, text=source_url)

        # Ask the user if they want to see the next or previous recipe
        context.bot.send_message(chat_id=update.effective_chat.id, text="Type 'next' to see the next recipe, or 'previous' to see the previous recipe.")

        # Wait for the user's response
        user_response = ''
        while user_response.lower() not in ['next', 'previous']:
            user_response = context.bot.get_updates()[-1].message.text

        # If the user wants to see the next recipe, continue the loop
        if user_response.lower() == 'next':
            continue

        # If the user wants to see the previous recipe, go back one iteration of the loop
        elif user_response.lower() == 'previous':
            continue

# Create an instance of the Telegram updater
updater = Updater('6229406413:AAGkHXGCMoXsTRRM-ILNgrZA6jgYmzZelcE',True)

# Register the start command handler
updater.dispatcher.add_handler(CommandHandler("start", start))
# Register the message handler
message_handler = MessageHandler(Filters.text & ~Filters.command, message)
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

# Start the bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
updater.idle()
