FROM tadeorubio/pyodbc-msodbcsql17

LABEL MAINTAINER="Manny Lara" EMAIL="malara@tustin.k12.ca.us"

# create working directory
WORKDIR /app

# copy the requirements.txt file into the working directory
COPY requirements.txt .

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy everything into the working directory (.dockerignore excludes unwanted files/directories)
COPY . .

# start up command
CMD [ "uvicorn", "main:app", "--host=0.0.0.0" ]