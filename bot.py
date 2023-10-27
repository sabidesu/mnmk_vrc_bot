import os
import telebot

from notion_client import Client
from basic_notion.query import Query
from models import MovieList, Movie

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['movierequest', 'mr'])
def request_handler(message):
  text = "what movie do you want to request? format your request like this: *movie name (year)*\ni.e. *the matrix (1999)*"
  sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
  bot.register_next_step_handler(sent_msg, movie_response)

def movie_response(message):
  movie = message.text.strip().lower()
  text = f"your movie *{movie}* has been added to the list uwu _(but not actually because i haven't implemented that yet oopsies)_"
  sent_msg = bot.reply_to(message, text, parse_mode='Markdown')

class MovieDatabase(object):
  def __init__(self, database_id):
    self.database_id = database_id
    self.notion = Client(auth=os.environ.get('NOTION_TOKEN'))

  def get_movies(self) -> MovieList:
    data = self.notion.databases.query(
      **Query.database(
        database_id=self.database_id
      ).sorts(
        MovieList.item.name.sort.ascending
      ).serialize()
    )
    return MovieList(data=data)

  def is_movie_in_list(self, movie: str) -> str:
    movie_list = self.get_movies()
    movies = {item.name.one_item.content: item.status.name for item in movie_list.items()}
    if movie in movies.keys():
      return movies[movie]
    return ''

  def add_movie_to_list(self, movie: str):
    in_list = self.is_movie_in_list(movie)
    if in_list == 'watched':
      return f"sorry, we've already watched *{movie}*!"
    elif in_list == 'to watch':
      return f"sorry, someone's already requested *{movie}*!"

    page = Movie.make(
      parent={'database_id': self.database_id},
      name=movie,
      status='to watch',
    )
    response = self.notion.pages.create(**page.data)
    item = Movie(data=response)
    assert item.name == movie
    return f"your movie *{movie}* has been added to the list uwu"

movieDB = MovieDatabase(os.environ.get('NOTION_DATABASE_ID'))
print(movieDB.add_movie_to_list('the matrix (1999)'))

# bot.infinity_polling()
