# We build from python3.6 which provides a python3.6 insatlled ubuntu OS.
FROM python:3.6

# Update ENV
RUN apt-get update

# Install Psycopg2
RUN apt-get install -y python-psycopg2

# App directory
RUN mkdir -p /usr/local/src/stories
WORKDIR /usr/local/src/stories
COPY . /usr/local/src/stories

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_CONFIG docker
ENV FLASK_APP stories.py
EXPOSE 8000
