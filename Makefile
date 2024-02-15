SHELL := /bin/bash

# ; \ is there so these commands both execute in the same shell
main: .env src/bot.py
	source .env; \
	python src/bot.py

clean: bot.log src/__pycache__
	rm -rf bot.log src/__pycache__
