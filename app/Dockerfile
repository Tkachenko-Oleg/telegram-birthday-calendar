# start:
# docker run -it -e TOKEN=your_token bot_container:v1

FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install aiogram

RUN mkdir -p /opt/telegram-birthday-calendar

COPY *.py /opt/telegram-birthday-calendar
COPY handlers /opt/telegram-birthday-calendar
COPY services /opt/telegram-birthday-calendar

WORKDIR /opt/telegram-birthday-calendar/app
RUN useradd mybot
USER mybot

ENTRYPOINT ["python3", "main.py"]
