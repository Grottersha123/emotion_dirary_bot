FROM python:3.8-slim-buster AS bot


RUN pip3 install python-telegram-bot aiogram

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY emotionbot .

CMD [ "python3", "bot.py" ]