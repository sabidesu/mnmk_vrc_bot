import os
import logging

from notion_client import AsyncClient
from basic_notion.query import Query
from models import MovieList, Movie

class MovieDatabase(object):
  def __init__(self, database_id):
    self.database_id = database_id
    self.notion = AsyncClient(auth=os.environ.get('NOTION_TOKEN'))

  async def get_movies(self) -> MovieList:
    data = await self.notion.databases.query(
      **Query.database(
        database_id=self.database_id
      ).sorts(
        MovieList.item.name.sort.ascending
      ).serialize()
    )
    return MovieList(data=data)

  async def is_movie_in_list(self, movie: str) -> str:
    movie_list = await self.get_movies()
    movies = {item.name.one_item.content: item.status.name for item in movie_list.items()}
    if movie in movies.keys():
      return movies[movie]
    return ''

  async def add_movie_to_list(self, movie: str) -> str:
    in_list = await self.is_movie_in_list(movie)
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
    response = await self.notion.pages.create(**page.data)
    item = Movie(data=response)
    return f"your movie *{movie}* has been added to the list uwu"
