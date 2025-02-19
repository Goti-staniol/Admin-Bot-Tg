import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot_core import private_router, group_router


load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


async def run_bot():
    dp.include_routers(private_router, group_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
