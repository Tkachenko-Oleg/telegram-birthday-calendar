from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import UserIsBlockedError

from config import Config

api_id = Config.api_id
api_hash = Config.api_hash
bot_token = Config.token
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


async def main():
    try:
        await client.send_message(2064313437, 'Hello! I am Bot!')
    except UserIsBlockedError:
        print("User is blocked")


print('BOT IS STARTED')
while True:
    try:
        trigger = input("send message? (y/n): ")
        if trigger.lower() == 'y':
            with client:
                client.loop.run_until_complete(main())
        else:
            raise KeyboardInterrupt
    except (KeyboardInterrupt, SystemExit):
        print('\nEND')
        break
