from basic_notion.page import NotionPage, NotionPageList
from basic_notion.field import TitleField, SelectField, DateField

class Movie(NotionPage):
  name = TitleField(property_name='name')
  status = SelectField(property_name='status')
  watch_date = DateField(property_name='watch date')

class MovieList(NotionPageList[Movie]):
  ITEM_CLS = Movie
