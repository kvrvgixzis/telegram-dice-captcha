"""
Телеграм бот для отображения капчи новым пользователям
"""
import random

from aiogram import types, Dispatcher
from aiogram.bot import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '0'
RICK_ROLL_URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
BIP_BOP_URL = 'https://www.youtube.com/watch?v=gsNaR6FRuO0'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def set_permissions_to(
        user_id: types.User.id,
        chat_id: types.Chat.id,
        permissions: bool
    ) -> None:
    """устанавливает права пользователя"""
    await bot.restrict_chat_member(chat_id, user_id, permissions=types.ChatPermissions(
        can_send_messages=permissions,
        can_send_media_messages=permissions,
        can_send_other_messages=permissions,
        can_add_web_page_previews=permissions
    ))


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_members_handler(message: types.Message) -> None:
    """слушает событие 'новый пользователь в чате'"""
    try:
        [new_member] = message.new_chat_members
        chat_id = message.chat.id
        user_id = new_member.id
        username = new_member.username

        await set_permissions_to(user_id, chat_id, permissions=False)

        accept_btn = InlineKeyboardButton('Я не бот', callback_data=f'true_{user_id}')
        decline_btn = InlineKeyboardButton('Я бот', url=RICK_ROLL_URL)
        fools_btn = InlineKeyboardButton('110100011000', url=BIP_BOP_URL)

        # перемешиваем кнопки
        btns = [accept_btn, decline_btn, fools_btn]
        random.shuffle(btns)
        [first_btn, second_btn, third_btn] = btns

        reply_markup = InlineKeyboardMarkup().row(first_btn).row(second_btn).row(third_btn)
        await message.reply(f'Привет {username}, докажи что ты не бот', reply_markup)
    except Exception as ex:
        print('new user', ex)


@dp.callback_query_handler(lambda call: call.data.startswith('true_'))
async def unban_me(callback_query: types.CallbackQuery) -> None:
    """слушает нажатие на кнопку 'Я не бот'"""
    user_id = int(callback_query.data.replace('true_', '', 1))
    chat_id = callback_query.message.chat.id
    is_target_user = callback_query.from_user.id == user_id

    if is_target_user:
        await set_permissions_to(user_id, chat_id, permissions=True)
        await callback_query.answer('Поздравляю, ты не бот')
        await callback_query.message.delete()
    else:
        await callback_query.answer(text='Тебя не спрашивал', show_alert=True)

