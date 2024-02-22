from aiogram import Bot, Dispatcher
import asyncio
from config import Config

from services import IsMemoryDataSource, IsDataBaseSource, Tools, DatasourceId

def create_data_source(key):
    match key:
        case DatasourceId.InMemory:
            return IsMemoryDataSource()
        case DatasourceId.Postgres:
            return IsDataBaseSource()


bot = Bot(token=Config.token)
dp = Dispatcher()
datasource = create_data_source(DatasourceId.Postgres)
# datasource.create_table()
tools = Tools()


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
