import os
import telebot
from notion_client import Client

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['movierequest', 'mr'])
def start_handler(message):
  text = "what movie do you want to request? format your request like this: *movie name (year)*\ni.e. *the matrix (1999)*"
  sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
  bot.register_next_step_handler(sent_msg, movie_request)

def movie_request(message):
  movie = message.text
  text = f"your movie *{movie}* has been added to the list uwu _(but not actually because i haven't implemented that yet oopsies)_"
  sent_msg = bot.reply_to(message, text, parse_mode='Markdown')

def connect_movie_db():
  notion = Client(auth=os.environ.get('NOTION_TOKEN'))
  db_response = notion.databases.query(**Query(database_id=os.environ.get('NOTION_DATABASE_ID')))
  # look into: https://github.com/altvod/basic-notion
  return db_response

bot.infinity_polling()
print(connect_movie_db())
