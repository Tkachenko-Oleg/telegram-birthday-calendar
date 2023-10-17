from aiogram import Bot
import asyncio
from config import Config
from handlers import dp

bot = Bot(token=Config.token)


async def main():
    try:
        print("Бот был успешно запущен")
        await dp.start_polling(bot)
    finally:
        print("Бот был остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот был остановлен")
