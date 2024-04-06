import asyncio
import json
from aiogram import Bot, Dispatcher

from config import Config
from services import IsMemoryDataSource, IsDataBaseSource, Tools, DatasourceId, Panels


def create_data_source(key):
    match key:
        case DatasourceId.InMemory:
            return IsMemoryDataSource()
        case DatasourceId.Postgres:
            return IsDataBaseSource()


bot = Bot(token=Config.token)
dp = Dispatcher()
tools = Tools()
panels = Panels()
datasource = create_data_source(DatasourceId.Postgres)
# datasource.create_table()
with open('phrases.json') as jsonFile:
    phrases = json.load(jsonFile)


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
