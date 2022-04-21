.PHONY: create_env_mac create_env_win start_env start start_container requirements build run stop clean_docker

create_env_mac:
	python3 -m venv env

create_env_win:
	py -m venv env

start_env:
	source env/bin/activate 

start:
	uvicorn main:app --reload

start_container:
	uvicorn main:app --host=0.0.0.0 --reload

requirements:
	python3 -m pip freeze > requirements.txt

build:
	docker build -t spedfastapi .

run:
	docker run -d --rm --name pythonfastapi -p 8000:8000 spedfastapi

stop:
	docker kill pythonfastapi

clean_docker:
	docker system prune -f