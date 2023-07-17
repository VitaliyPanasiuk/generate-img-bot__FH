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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state,withdrawal_to_tn_state,sber_qiwi_state,sber_sber_state,sber_sber_png_state,sber_tn_png_andr_state,rural_state,tran_check_state,tran_state,bin_donate_state,bin_with_draw_state,okx_state

from tgbot.services.del_message import delete_message

from tgbot.misc.gen_donate import gen_donate
from tgbot.misc.gen_receipt import gen_receipt
from tgbot.misc.gen_tran import gen_tran
from tgbot.misc.gen_visa_tran import gen_visa_tran
from tgbot.misc.gen_tn_bank import gen_tn_bank
from tgbot.misc.gen_receipt_pdf import gen_receipt_pdf
from tgbot.misc.gen_to_bank_pdf import gen_to_bank_pdf
from tgbot.misc.gen_tn_to_bank import gen_tn_to_bank
from tgbot.misc.functions import auf, change_balance

from tgbot.mail.bin_donate import generate_bin_donate
from tgbot.mail.bin_withdraw import generate_bin_withdraw
from tgbot.mail.okx import generate_okx

from tgbot.bin_tran.tran import generate_bin_tran
from tgbot.bin_tran.check_tran import generate_bin_check_tran

from tgbot.rural_binance.rural.rural import gen_rural_png

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button,sber_menu_button,sber_sber_menu_button,binance_tran_menu_button,okx_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

mail_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

    
@mail_router.message(F.text == 'Binance почта пополнение')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/mail/bin_donate_ex.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['bin-donate-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(bin_donate_state.gen_data)
    
    
@mail_router.message(F.text, bin_donate_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time':dt[0],
                'date':dt[1],
                'month':dt[2],
                'amount':dt[3],
                'coin':dt[4],
                'user_id':user_id,
            }
            generate_bin_donate(data)
            photo = FSInputFile(f'tgbot/mail/{data["user_id"]}_output_bin_donate.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/mail/{data["user_id"]}_output_bin_donate.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(bin_donate_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@mail_router.message(F.text == 'Binance почта вывод')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/mail/bin_withdraw_ex.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['bin-withdraw-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(bin_with_draw_state.gen_data)
    
    
@mail_router.message(F.text, bin_with_draw_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time':dt[0],
                'date':dt[1],
                'month':dt[2],
                'amount':dt[3],
                'coin':dt[4],
                'address':dt[5],
                'tran_id':dt[6],
                'user_id':user_id,
            }
            generate_bin_withdraw(data)
            photo = FSInputFile(f'tgbot/mail/{data["user_id"]}_output_bin_withdraw.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/mail/{data["user_id"]}_output_bin_withdraw.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(bin_with_draw_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@mail_router.message(F.text == 'Okx почта пополнение')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/mail/okx_ex.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['okx-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(okx_state.gen_data)
    
    
@mail_router.message(F.text, okx_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM rural_binance WHERE name = 'binance'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time':dt[0],
                'currency':dt[1],
                'month':dt[2],
                'amount':dt[3],
                'date':dt[4],
                'user_id':user_id,
            }
            generate_okx(data)
            photo = FSInputFile(f'tgbot/mail/{data["user_id"]}_output_okx.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/mail/{data["user_id"]}_output_okx.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(okx_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        