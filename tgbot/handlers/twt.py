from aiogram import Router, Bot, types
from aiogram.types import Message,FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from magic_filter import F
from aiogram import F

from tgbot.db.db_update import reg_user, update_balance

import os
import time
import datetime
import requests
import asyncio

from tgbot.misc.states import twt_send_state, twt_rec_state

from tgbot.services.del_message import delete_message

from tgbot.twt.twt_send import gen_twt_send
from tgbot.twt.twt_rec import gen_twt_rec

from tgbot.misc.functions import auf,change_balance

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button,twt_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

twt_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@twt_router.message(F.text == 'TWT')
async def checks_withdrawal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = twt_menu_button()
    await bot.send_message(user_id, "Выбери тип транзакции",reply_markup=btn.as_markup(resize_keyboard=True))

@twt_router.message(F.text == 'TWT отправка')
async def doante_visa(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/twt/send.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['twt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(twt_send_state.gen_data)
    
    
@twt_router.message(F.text, twt_send_state.gen_data)
async def doante_visa_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'phone_time' : dt[0],
                'tran_sum' : dt[1],
                'tran_sum_usd' : dt[2],
                'date' : dt[3],
                'adress' : dt[4],
                'network' : dt[5],
                'user_id' : str(user_id),
                
            }
            gen_twt_send(data)
            photo = FSInputFile(f'tgbot/twt/{data["user_id"]}_output_twt_send.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/twt/{data["user_id"]}_output_twt_send.png')
            await change_balance(user_id, price[2],'minus')
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(twt_send_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@twt_router.message(F.text == 'TWT получение')
async def doante_visa(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/twt/recive.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['twt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(twt_rec_state.gen_data)
    
    
@twt_router.message(F.text, twt_rec_state.gen_data)
async def doante_visa_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        # try:
            dt = message.text.splitlines()
            data = {
                'phone_time' : dt[0],
                'tran_sum' : dt[1],
                'tran_sum_usd' : dt[2],
                'date' : dt[3],
                'adress' : dt[4],
                'network' : dt[5],
                'user_id' : str(user_id),
                
            }
            gen_twt_rec(data)
            photo = FSInputFile(f'tgbot/twt/{data["user_id"]}_output_twt_rec.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/twt/{data["user_id"]}_output_twt_rec.png')
            await change_balance(user_id, price[2],'minus')
            await state.clear()
        # except Exception as e:
        #     btn = main_menu_button()
        #     print(f"Problem with data from user")
        #     print(e)
        #     await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
        #     await state.set_state(twt_rec_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()