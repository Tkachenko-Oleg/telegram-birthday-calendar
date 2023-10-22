from aiogram import Bot, Dispatcher
import asyncio
from config import Config

bot = Bot(token=Config.token)
dp = Dispatcher()

# commands:
# start
# help
# change language
# add birthday
# delete birthday
# change birthday
# show all birthdays
# show birthdays this week


async def main():
    try:
        print("Бот был успешно запущен")
        from handlers import dp
        await dp.start_polling(bot)
    finally:
        print("Бот был остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот был остановлен")
