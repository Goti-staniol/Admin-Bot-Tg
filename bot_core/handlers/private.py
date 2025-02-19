from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from bot_core.keyboard.inline import generate_menu_kb


private_router = Router()
private_router.message.filter(F.chat.type == 'private')


@private_router.message(CommandStart())
async def start_handler(msg: Message, bot: Bot):
    bot_info = await bot.get_me()

    await msg.answer('hello', reply_markup=generate_menu_kb(bot_info.username))