SHELL := /bin/bash

# ; \ is there so these commands both execute in the same shell
main: .env bot.py
	source .env; \
	python bot.py

clean: bot.log
	rm bot.log
