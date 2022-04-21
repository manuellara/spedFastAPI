.PHONY: create_env_mac create_env_win start_env start start_container requirements_mac requirements_win build run stop_container clean_docker

# creates venv on mac
create_env_mac:
	python3 -m venv env

# creates venv on windows
create_env_win:
	py -m venv env

# starts venv (both mac and windows)
start_env:
	source env/bin/activate 

# starts python application
start:
	uvicorn main:app --reload

# dockerfile start up command
start_container:
	uvicorn main:app --host=0.0.0.0 --reload

# outputs requirements for mac
requirements_mac:
	python3 -m pip freeze > requirements.txt

# outputs requirements for windows
requirements_win:
	py -m pip freeze > requirements.txt

# docker build image command 
build:
	docker build -t spedfastapi .

# starts a container based off the spedfastapi image
run:
	docker run -d --rm --name pythonfastapi -p 8000:8000 spedfastapi

# stops docker container by name
stop_container:
	docker kill pythonfastapi

# cleans up system 
clean_docker:
	docker system prune -f