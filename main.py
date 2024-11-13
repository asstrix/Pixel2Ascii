import asyncio, logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import bot, router

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)
logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
