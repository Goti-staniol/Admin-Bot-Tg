import asyncio

from bot import bot, dp


async def run_bot() -> None:
    """Start bot and include routers"""
    from bot.handlers.private import private_router
    from bot.handlers.group import group_router

    dp.include_routers(group_router, private_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
