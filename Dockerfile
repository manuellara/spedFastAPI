FROM tadeorubio/pyodbc-msodbcsql17

# create working directory
WORKDIR /app

# copy the requirements.txt file into the working directory
COPY requirements.txt .

# install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy everything into the working directory (.dockerignore excludes unwanted files/directories)
COPY . .

# start up command
CMD [ "make", "start_container" ]