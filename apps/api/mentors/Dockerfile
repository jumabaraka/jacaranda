# start by pulling the python image
FROM python:3.11.4-slim

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# Expose the required port
EXPOSE 5000


# Start the Flask application
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
