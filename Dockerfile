FROM ubuntu:latest

# Install Python 3
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

# Install Psycopg2
RUN apt-get install -y python-psycopg2

# App directory
RUN mkdir -p /usr/local/src/stories
WORKDIR /usr/local/src/stories
COPY . /usr/local/src/stories

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Flask Operations
ENV FLASK_APP stories.py

# run-time configuration
EXPOSE 8000
VOLUME /usr/local/src/stories
# CMD ["bash",  "-c", "./boot.sh"]
CMD ["bash",  "-c", "/usr/local/bin/gunicorn --reload -w $((2*$(nproc)+1)) -b :8000 stories:app"]
# ENTRYPOINT ["./boot.sh"]
