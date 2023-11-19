FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

RUN python3 -m venv env
RUN . env/bin/activate && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

WORKDIR /app

COPY ./docker/entrypoint.sh entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]