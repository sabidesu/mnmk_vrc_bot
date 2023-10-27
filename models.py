from basic_notion.page import NotionPage, NotionPageList
from basic_notion.field import TitleField, SelectField, DateField

class Movie(NotionPage):
  title = TitleField()
  status = SelectField(options=['watched', 'to watch'])
  watch_date = DateField()

class MovieList(NotionPageList[Movie]):
  ITEM_CLS = Movie
