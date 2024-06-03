FROM python:3.12.1-slim-bookworm

RUN apt-get -y update; apt-get -y install curl redis-server
RUN useradd -ms /bin/bash bumblebee

USER bumblebee

WORKDIR /home/bumblebee

RUN curl -sSL https://install.python-poetry.org | python -

COPY poetry.lock . 
COPY pyproject.toml . 

RUN ~/.local/bin/poetry install 

COPY app.py .
COPY templates/ ./templates/
COPY start.sh .

EXPOSE 5000

CMD [ "./start.sh" ]