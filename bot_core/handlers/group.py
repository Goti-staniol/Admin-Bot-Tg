from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, ChatPermissions, ChatMemberBanned
from aiogram.enums import ChatMemberStatus

from bot_core.cfg import texts, html_mode
from bot_core.func import parse_duration


group_router = Router()
group_router.message.filter(F.chat.type != 'private')


@group_router.message(Command('id'))
async def get_id_handler(msg: Message) -> None:
    if msg.reply_to_message:
        await msg.answer(
            text=f'<b>Айди пользователя</b>: <code>{msg.reply_to_message.from_user.id}</code>',
            parse_mode=html_mode
        )
    else:
        await msg.answer(
            text=f'<b>Айди группы</b>: <code>{msg.chat.id}</code>',
            parse_mode=html_mode
        )


@group_router.message(Command('mute'))
async def mute_handler(msg: Message, command: CommandObject, bot: Bot):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        input_command = command.command
        args = command.args.split() if command.args else []
        reason = None
        target_time = None
        target_user_id = None
        if args:
            if msg.reply_to_message:
                try:
                    target_user_id = msg.reply_to_message.from_user.id
                    int(args[0][:1])
                    target_time = args[0]
                    reason = args[1] if len(args) > 1 else None
                except ValueError:
                    reason = args[0]
            else:
                try:
                    target_user_id = int(args[0])
                    try:
                        if len(args) > 1:
                            int(args[1][:1])
                            target_time = args[1]
                            reason = args[2] if len(args) > 2 else None
                    except ValueError:
                        reason = args[1]
                except ValueError:
                    await msg.answer(
                        text=texts['error_value_command'].format(command=input_command),
                        parse_mode=html_mode
                    )
                    return
            try:
                await bot.restrict_chat_member(
                    chat_id=msg.chat.id,
                    user_id=target_user_id,
                    permissions=ChatPermissions(can_send_other_messages=False),
                    until_date=datetime.now() + parse_duration(target_time)
                )
                await msg.answer(
                    text=texts['mute_msg'].format(
                        user_id=target_user_id,
                        target_time=target_time if target_time else 'Навсегда',
                        reason=f'- Причина: {reason}' if reason else ''
                    )
                )
            except ValueError:
                await msg.answer(
                    text=texts['error_value_command'].format(command=input_command),
                    parse_mode=html_mode
                )
        else:
            await msg.answer(
                text=texts['error_value_command'].format(command=input_command),
                parse_mode=html_mode
            )


@group_router.message(Command('unmute'))
async def unmute_handler(msg: Message, bot: Bot):
    target_user_id = msg.reply_to_message.from_user.id
    await bot.restrict_chat_member(
        chat_id=msg.chat.id,
        user_id=target_user_id,
        permissions=ChatPermissions(can_send_other_messages=True)
    )


@group_router.message(Command('kick'))
async  def kick_handler(msg: Message, bot: Bot):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        if msg.reply_to_message:
            target_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
            if not target_user.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
                await bot.ban_chat_member(msg.chat.id, target_user.user.id)
                await bot.unban_chat_member(msg.chat.id, target_user.user.id)
                await msg.answer(
                    text='Ох... Дорогой, не описать моих эмоций, прощай!'
                )
            else:
                if target_user.user.is_bot:
                    await msg.answer(
                        text='А ловко ты придумал! Но мне и так хорошо! Может в следующий раз исключим тебя?'
                    )
                else:
                    await msg.answer(
                        text='<b>Кикнуть админа? Глупая затея!</b>',
                        parse_mode=html_mode
                    )
        else:
            await msg.answer(
               text= 'Упс! Отправьте команду ответом на сообщения пользователя!'
            )


@group_router.message(Command('ban'))
async def ban_handler(msg: Message, command: CommandObject, bot: Bot):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        input_command = command.command
        args = command.args.split() if command.args else []
        reason = None
        target_time = None
        target_user_id = None
        if args:
            if msg.reply_to_message:
                try:
                    target_user_id = msg.reply_to_message.from_user.id
                    int(args[0][:1])
                    target_time = args[0]
                    reason = args[1] if len(args) > 1 else None
                except ValueError:
                    reason = args[0]
            else:
                try:
                    target_user_id = int(args[0])
                    try:
                        if len(args) > 1:
                            int(args[1][:1])
                            target_time = args[1]
                            reason = args[2] if len(args) > 2 else None
                    except ValueError:
                        reason = args[1]
                except ValueError:
                    await msg.answer(
                        text=texts['error_value_command'].format(command=input_command),
                        parse_mode=html_mode
                    )
                    return
            try:
                await bot.ban_chat_member(
                    chat_id=msg.chat.id,
                    user_id=target_user_id,
                    until_date=datetime.now() + parse_duration(target_time)
                )
                await msg.answer(
                    text=texts['ban_msg'].format(
                        user_id=target_user_id,
                        target_time=target_time if target_time else 'Навсегда',
                        reason=f'- Причина: {reason}' if reason else ''
                    ),
                    parse_mode=html_mode
                )
            except ValueError:
                await msg.answer(
                    text=texts['error_value_command'].format(command=input_command),
                    parse_mode=html_mode
                )
        else:
            await msg.answer(
                text=texts['error_value_command'].format(command=input_command),
                parse_mode=html_mode
            )


@group_router.message(Command('unban'))
async def unban_handler(msg: Message, bot: Bot):
    member = await msg.chat.get_member(msg.from_user.id)
    if member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        target_user = await msg.chat.get_member(msg.reply_to_message.from_user.id)
        if not target_user.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            if isinstance(target_user, ChatMemberBanned):
                await bot.unban_chat_member(msg.chat.id, target_user.user.id)
            else:
                await msg.answer(
                    text='Странно, пользователь не заблокирован!'
                )
        else:
            await msg.answer(
                text='Банить админа? Хм, не думаю что это хорошая затея!'
            )