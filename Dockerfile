FROM ubuntu:latest

ENV FLASK_APP stories.py
ENV FLASK_CONFIG docker

# RUN adduser -D stories
# USER stories

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

WORKDIR /home/stories

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY stories.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
