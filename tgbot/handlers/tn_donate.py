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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state

from tgbot.services.del_message import delete_message

from tgbot.misc.gen_donate import gen_donate
from tgbot.misc.gen_receipt import gen_receipt
from tgbot.misc.gen_tran import gen_tran
from tgbot.misc.gen_visa_tran import gen_visa_tran
from tgbot.misc.gen_tn_bank import gen_tn_bank
from tgbot.misc.gen_receipt_pdf import gen_receipt_pdf
from tgbot.misc.gen_to_bank_pdf import gen_to_bank_pdf
from tgbot.misc.functions import auf,change_balance

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

tn_donate_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@tn_donate_router.message(F.text == 'Пополнение - Visa')
async def doante_visa(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-visa-tran.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['visa-tran-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_visa_tran_state.gen_data)
    
    
@tn_donate_router.message(F.text, gen_visa_tran_state.gen_data)
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
                'time' : dt[0],
                'tn_time' : dt[1],
                'tran_sum' : dt[2],
                'tn_balance' : dt[3],
                'tn_month' : dt[4],
                'tn_month_spend' : dt[5],
                
            }
            gen_visa_tran(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_visa_tran.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_visa_tran.png')
            await change_balance(user_id, price[2],'minus')
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_visa_tran_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
            
    
@tn_donate_router.message(F.text == 'Пополнение - Visa direct')
async def donate_visa_direct(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-donate.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['donate-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa direct'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_donate_state.gen_data)
    
@tn_donate_router.message(F.text, gen_donate_state.gen_data)
async def donate_visa_direct_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa direct'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time' : dt[0],
                'tn_time' : dt[1],
                'tran_sum' : dt[2],
            }
            gen_donate(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_donate.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo, reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_donate.png')
            await change_balance(user_id, price[2],'minus')
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_donate_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
    
    
@tn_donate_router.message(F.text == 'Пополнение - Перевод с карты')
async def donate_transaction_from_card(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # change ex photo
    photo = FSInputFile('tgbot/img/ex-card-tran.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['tran-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-card transaction'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_tran_state.gen_data)
    
@tn_donate_router.message(F.text, gen_tran_state.gen_data)
async def donate_transaction_from_card_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-card transaction'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time' : dt[0],
                'tn_time' : dt[1],
                'tran_sum' : dt[2],
                'tn_balance' : dt[3],
                'tn_month' : dt[4],
                'tn_month_spend' : dt[5],
                'tran_id' : dt[6],
            }
            gen_tran(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_tran.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_tran.png')
            await change_balance(user_id, price[2],'minus')
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_tran_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()