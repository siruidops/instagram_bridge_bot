FROM python:3.8.6-slim-buster


RUN apt-get update
RUN apt-get install -y python3 python3-pip

COPY . /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "instagram_bridge_bot.py"]

