SHELL := /bin/bash

# ; \ is there so these commands both execute in the same shell
main: .env bot.py
	source .env; \
	python src/bot.py

clean: bot.log __pycache__
	rm -rf bot.log __pycache__
