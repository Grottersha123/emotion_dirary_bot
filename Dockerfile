FROM python:3.8-alpine3.10


RUN pip3 install python-telegram-bot aiogram

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

CMD [ "python3", "bot.py" ]