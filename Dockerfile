FROM python:3.10-slim

# install build essentials
RUN apt-get update && apt-get install build-essential -y

# create working directory
WORKDIR /app

# copy the requirements.txt file into the working directory
COPY requirements.txt ./

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy the main.py and Makefile into the working directory
COPY . .

# start up command
CMD [ "make", "start_container" ]