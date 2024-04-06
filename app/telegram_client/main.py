from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UserIsBlockedError
from time import sleep

from config import Config
from date_calc import Date
from postgres_client import PostgresClient
from tools import Tools

api_id = Config.api_id
api_hash = Config.api_hash
bot_token = Config.token
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
postgres_client = PostgresClient()
tools = Tools()


async def main():
    try:
        month, day = Date.get_today_date()

        info = postgres_client.get_all(f"2000-{month}-{day}")
        for i in info:
            try:
                await client.send_message(int(i[0]), f"Сегодня день рождения у {i[1]}\nНомер телефона: {i[2]}")
            except ValueError:
                continue

    except UserIsBlockedError:
        print("User is blocked")


print('BOT IS STARTED')

while True:
    try:
        with client:
            client.loop.run_until_complete(main())
        break
        sleep(5)
    except (KeyboardInterrupt, SystemExit):
        break

print('\nEND')
