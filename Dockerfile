FROM python:3.6-alpine

ENV FLASK_APP stories.py
ENV FLASK_CONFIG docker-sqlite

RUN adduser -D stories
USER stories

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
