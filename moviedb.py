import os
import logging

from notion_client import Client
from basic_notion.query import Query
from models import MovieList, Movie

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

  def add_movie_to_list(self, movie: str) -> str:
    in_list = self.is_movie_in_list(movie)
    if in_list == 'watched':
      logging.info(f"movie {movie} already watched")
      return f"sorry, we've already watched *{movie}*! type the command again to try another film"
    elif in_list == 'to watch':
      logging.info(f"movie {movie} already requested")
      return f"sorry, someone's already requested *{movie}*! type the command again to try another film"

    page = Movie.make(
      parent={'database_id': self.database_id},
      name=[movie],
      status='to watch',
    )
    response = self.notion.pages.create(**page.data)
    item = Movie(data=response)
    assert item.name.get_text() == movie
    return f"your movie *{movie}* has been added to the list uwu"
