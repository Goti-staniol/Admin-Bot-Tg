from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from bot import private_router


@private_router.message(CommandStart())
async def start_handler(msg: Message) -> None:
    await msg.answer('hello')