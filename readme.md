# monday night movie knight telegram bot

my friends and i like to watch movies in vrchat on monday nights, and i keep a [notion database](https://ewavstudio.notion.site/f1e0fe2eb9ca43cf909dbe0f95cd317d?v=2831e82362dd40dfb49518855d3f2b69&pvs=4) for keeping track of what we've watched and what movies people want to watch. while adding stuff in by hand isn't hard at all, i decided why not make a bot to do it for me?

## dependencies

python 3.12.0

### python libraries

- [notion-client](https://pypi.org/project/notion-client/) >= 2.0.0
- [basic-notion](https://pypi.org/project/basic-notion/) >= 0.6.2
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) >= 4.14.0
- aiohttp >= 3.9.3

you can install the necessary libraries with this command:

```sh
python -m pip install pyTelegramBotAPI basic-notion notion-client
```
