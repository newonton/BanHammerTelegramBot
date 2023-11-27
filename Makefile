all: deps configs run

deps:
	pip3 install -r requirements.txt

configs:
	@if [ ! -f .env ]; then echo "BANHAMMER_TOKEN=token\nBANHAMMER_ALLOWED_USER_IDS=0,1" > .env; fi

run:
	python3 main.py

