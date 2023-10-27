import os
import telebot

from notion_client import Client
from basic_notion.query import Query
from models import MovieList

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

def get_movies():
  notion = Client(auth=os.environ.get('NOTION_TOKEN'))
  data = notion.databases.query(
    **Query.database(
      database_id=os.environ.get('NOTION_DATABASE_ID')
    ).sorts(
      MovieList.item.name.sort.ascending
    ).serialize()
  )
  return MovieList(data=data)

def movie_already_in_list(movie_list: MovieList, movie: str):
  movies = {item.name.one_item.content: item.status.name for item in movie_list.items()}
  if movie in movies.keys():
    return movies[movie]
  return ''

print(movie_already_in_list(get_movies(), 'american pie'))
# bot.infinity_polling()
