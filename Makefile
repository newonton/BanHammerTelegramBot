all: deps run

deps:
	pip3 install -r requirements.txt

run:
	python3 main.py

