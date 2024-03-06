# start:
# docker build . -t bot_container:v1
# docker run -it -e TOKEN=your_token DATABASE=your_database USERDATABASE=your_username PASSWORD=your_password HOST=your_host PORT=your_port  bot_container:v1

FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install aiogram
RUN pip3 install psycopg2-binary

RUN mkdir -p /opt/telegram-birthday-calendar

COPY .. /opt/telegram-birthday-calendar/app

WORKDIR /opt/telegram-birthday-calendar/app
RUN useradd mybot
USER mybot

ENTRYPOINT ["python3", "main.py"]
