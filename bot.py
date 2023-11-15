import os
import telebot
import logging
import re

from moviedb import MovieDatabase

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

allowed_chat_ids = {
  'testing_chat': int(os.environ.get('TEST_CHAT_ID')),
  'official_chat': int(os.environ.get('PROD_CHAT_ID')),
}

logging.basicConfig(filename='bot.log', encoding='utf-8', level=logging.DEBUG)

@bot.message_handler(commands=['movierequest', 'mr'])
def request_handler(message):
  if message.chat.id not in allowed_chat_ids.values():
    logging.info(f"received request from user @{message.from_user.username} in invalid chat: {message.chat.id}")
    text = "sorry, this bot is only available in the testing chat or the official group chat!"
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
  else:
    logging.info(f"started request from user @{message.from_user.username}")
    text = "what movie do you want to request? format your request like this: *movie name (year)*\ni.e. *the matrix (1999)*\n\nnote: please write the full name of the movie! this is to avoid confusion with other movies with the same name.if you're unsure, use google :)\ni.e. if you want to watch _django unchained_, instead of *django*, write *django unchained*"
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
    bot.register_next_step_handler(sent_msg, movie_response)

def movie_response(message):
  movie = message.text.strip().lower()
  if movie_in_valid_format(movie):
    logging.info(f"user @{message.from_user.username} requested {movie}")
    text = movieDB.add_movie_to_list(movie)
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
  else:
    logging.info(f"user @{message.from_user.username} movie request in invalid format, discarded: {movie}")
    text = "sorry, your movie request was in an invalid format! type the command again to try again"
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')

def movie_in_valid_format(movie_s: str) -> bool:
  # make sure the movie is in the format of "movie name (year)"
  return True if re.match(r'.*\s\(\d{4}\)', movie_s) else False

movieDB = MovieDatabase(os.environ.get('NOTION_DATABASE_ID'))

bot.infinity_polling()
