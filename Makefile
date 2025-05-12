run:
	uvicorn tel_bot.main:app --reload

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

test:
	pytest -v -s
