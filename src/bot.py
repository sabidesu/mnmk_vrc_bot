import os
import logging
import re
import asyncio

from moviedb import MovieDatabase
from telebot.async_telebot import AsyncTeleBot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

allowed_chat_ids = {
  'testing_chat': int(os.environ.get('TEST_CHAT_ID')),
  'official_chat': int(os.environ.get('PROD_CHAT_ID')),
}

logging.basicConfig(filename='bot.log', encoding='utf-8', level=logging.INFO)

@bot.message_handler(commands=['help'])
async def help_handler(message):
  logging.info(f"received help request from user @{message.from_user.username}")
  text = "this bot is used to request movies to watch together as a group!\n\navailable commands:\n`/help` - displays this message\n`/movierequest movie name (year)` - adds a movie to the to watch list\n`/mr movie name (year)` - alias for `/movierequest`"
  sent_msg = await bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['movierequest', 'mr'])
async def request_handler(message):
  if message.chat.id not in allowed_chat_ids.values():
    logging.info(f"received request from user @{message.from_user.username} in invalid chat: {message.chat.id}")
    text = "sorry, this command is only available in the testing chat or the official group chat!"
    sent_msg = await bot.reply_to(message, text, parse_mode='Markdown')
    return

  logging.info(f"started request from user @{message.from_user.username}")

  msg_text = message.text.strip().lower()
  movie = extract_movie(msg_text)
  if movie:
    logging.info(f"user @{message.from_user.username} requested {movie}")
    text = await movieDB.add_movie_to_list(movie)
    sent_msg = await bot.reply_to(message, text, parse_mode='Markdown')
  else:
    text = "format your request like this: *movie name (year)*\ni.e. *the matrix (1999)*\n\nnote: please write the full name of the movie! this is to avoid confusion with other movies with the same name. if you're unsure, use google :)\ni.e. if you want to watch _django unchained_, instead of *django*, write *django unchained*"
    sent_msg = await bot.reply_to(message, text, parse_mode='Markdown')

def extract_movie(command: str) -> str:
  # make sure the movie is in the format of "movie name (year)"
  movie_re = r'(?:\/mr |\/movierequest )(.*\s\(\d{4}\))'
  match = re.match(movie_re, command)
  return match.group(1) if match else ''

movieDB = MovieDatabase(os.environ.get('NOTION_DATABASE_ID'))

# use infinity_polling in hopes that bot won't crash as often. things to check if still erroring
# - https://github.com/aio-libs/aiohttp/issues/850
# - https://stackoverflow.com/questions/77402707/telebot-infinity-polling-exception-connection-aborted-remotedisconnected
asyncio.run(bot.infinity_polling())
