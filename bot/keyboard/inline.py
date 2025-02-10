from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_menu_kb(bot_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='➕ Добавить в группу',
        url=(
            f'https://t.me/{bot_username}?startgroup=adm'
            '&admin=change_info+restrict_members+delete_messages'
            '+pin_messages+invite_users'
        )
    )
    return builder.as_markup()