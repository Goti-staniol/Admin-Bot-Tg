from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, ChatPermissions
from aiogram.enums import ChatMemberStatus

from bot.func import parse_duration

group_router = Router()
group_router.message.filter(F.chat.type != 'private')


@group_router.message(Command('mute'))
async def mute_handler(msg: Message, command: CommandObject, bot: Bot):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status == ChatMemberStatus.ADMINISTRATOR or member.status == ChatMemberStatus.CREATOR:
        args = command.args.split() if command.args else []
        target_time = None
        description = None
        original_time = None
        user_id_to_mute = None
        if args:
            if msg.reply_to_message:
                try:
                    user_id_to_mute = msg.reply_to_message.from_user.id
                    target_time = int(args[0][:1])
                    original_time = args[0]
                    description = args[1:] if len(args) > 1 else None
                except ValueError:
                    description = args[0]
            else:
                ... #TODO сделать мут без реплая

            await bot.restrict_chat_member(
                chat_id=msg.chat.id,
                user_id=user_id_to_mute,
                permissions=ChatPermissions(can_send_other_messages=False),
                until_date=datetime.now() + parse_duration(original_time)
            )
        else:
            ... #TODO Сделать обработку при которой пользователь ввел команду без аргументов


@group_router.message(Command('unmute'))
async def unmute_handler(msg: Message, bot: Bot):
    user_id_to_mute = msg.reply_to_message.from_user.id
    await bot.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=user_id_to_mute,
        permissions=ChatPermissions(can_send_other_messages=True)
    )
