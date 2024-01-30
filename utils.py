from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import CORRECT_ANSWER_PREFIX, WRONG_ANSWER_PREFIX


def get_callback_user_info(callback: types.CallbackQuery, prefix: str):
    """get user_id, chat_id and is_target_user from callback data"""
    user_id = int(callback.data.replace(prefix, ''))
    chat_id = callback.message.chat.id
    is_target_user = callback.from_user.id == user_id

    return user_id, is_target_user, chat_id


async def set_permissions_to(
    user_id: int,
    chat_id: int,
    permissions: bool,
    bot: Bot,
) -> None:
    """set user permissions for send messages to true/false"""
    await bot.restrict_chat_member(chat_id, user_id, permissions=types.ChatPermissions(
        can_send_messages=permissions,
        can_send_media_messages=permissions,
        can_send_other_messages=permissions,
        can_add_web_page_previews=permissions
    ))


def get_dice_keyboard(dice_value: int, user_id: int) -> InlineKeyboardBuilder:
    """create keyboard with 1-6 numbers with one current answer"""
    builder = InlineKeyboardBuilder()

    for index in range(6):
        number = index + 1
        callback_data = f"{CORRECT_ANSWER_PREFIX}{user_id}" if dice_value == number else f"{WRONG_ANSWER_PREFIX}{user_id}"
        builder.add(types.InlineKeyboardButton(
            text=str(number), callback_data=callback_data))

    builder.adjust(3)

    return builder


async def get_dice_value(chat_id: int, bot: Bot) -> int:
    """send dice to chat and return dice value"""
    data = await bot.send_dice(chat_id, emoji='🎲')
    return data.dice.value
