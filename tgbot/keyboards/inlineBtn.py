from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CastomCallbackOfEndingTransaction(CallbackData, prefix="fabnum"):
    # castom class for callback_data
    action: str
    transaction_id: Optional[int]

def transaction_button(id):
    # example = InlineKeyboardBuilder()
    # example.add(types.InlineKeyboardButton(
    #     text='Готово',
    #     callback_data=CastomCallbackOfEndingTransaction(action="end_transaction",transaction_id=int(id))
    # ))
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Одобрить", callback_data=CastomCallbackOfEndingTransaction(action="end_transaction",transaction_id=int(id))
    )
    builder.button(
        text="Отклонить", callback_data=CastomCallbackOfEndingTransaction(action="dicline_transaction",transaction_id=int(id))
    )
    return builder
