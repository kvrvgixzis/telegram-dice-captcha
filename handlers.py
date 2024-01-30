import time
from aiogram import F, Bot, Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from constants import (CORRECT_ANSWER_PREFIX, WRONG_ANSWER_PREFIX, DICE_SEND_MSG,
                       CORRECT_ANSWER_MSG, WRONG_USER_MSG, WRONG_ANSWER_MSG, BAN_TIMEOUT)
from utils import get_callback_user_info, get_dice_keyboard, get_dice_value, set_permissions_to

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_handler(event: ChatMemberUpdated, bot: Bot):
    user_id = event.new_chat_member.user.id
    chat_id = event.chat.id

    await set_permissions_to(user_id=user_id, chat_id=chat_id, permissions=False, bot=bot)

    dice_value = await get_dice_value(chat_id=chat_id, bot=bot)
    keyboard = get_dice_keyboard(dice_value=dice_value, user_id=user_id)

    await event.answer(
        DICE_SEND_MSG,
        reply_markup=keyboard.as_markup(),
    )


@router.callback_query(F.data.startswith(CORRECT_ANSWER_PREFIX))
async def correct_answer_handler(callback: types.CallbackQuery, bot: Bot):
    user_id, is_target_user, chat_id = get_callback_user_info(
        callback=callback, prefix=CORRECT_ANSWER_PREFIX)

    if is_target_user:
        await set_permissions_to(user_id=user_id, chat_id=chat_id, permissions=True, bot=bot)
        await callback.answer(CORRECT_ANSWER_MSG)
        await callback.message.delete()
    else:
        await callback.answer(WRONG_USER_MSG, show_alert=True)


@router.callback_query(F.data.startswith(WRONG_ANSWER_PREFIX))
async def wrong_answer_handler(callback: types.CallbackQuery):
    user_id, is_target_user, chat_id = get_callback_user_info(
        callback=callback, prefix=WRONG_ANSWER_PREFIX)

    if is_target_user:
        await callback.answer(WRONG_ANSWER_MSG, show_alert=True)
        await callback.bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            until_date=time.time() + BAN_TIMEOUT)
        await callback.message.delete()
    else:
        await callback.answer(WRONG_USER_MSG, show_alert=True)
