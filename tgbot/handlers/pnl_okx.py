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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state,withdrawal_to_tn_state,sber_qiwi_state,sber_sber_state,sber_sber_png_state,sber_tn_png_andr_state,rural_state,pnl_okx_state

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

from tgbot.sber.sber_qiwi.sber_qiwi_pdf import gen_sber_qiwi_pdf
from tgbot.sber.sber_sber.sber_sber_pdf import gen_sber_sber_pdf
from tgbot.sber.sber_sber_png.sber_sber_png import gen_sber_sber_png
from tgbot.sber.sber_tn_png_andr.sber_tn_png_andr import gen_sber_tn_png_andr

from tgbot.pnl_okx.main import gen

from tgbot.rural_binance.rural.rural import gen_rural_png

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button,sber_menu_button,sber_sber_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

pnl_okx_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@pnl_okx_router.message(F.text == 'Okx pnl')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/pnl_okx/ex_plus.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['pnl-okx-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM rural_binance WHERE name = 'rural'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(pnl_okx_state.gen_data)
    
data = {}    
    
@pnl_okx_router.message(F.text, pnl_okx_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM rural_binance WHERE name = 'rural'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            global data
            data = {
                'name' : dt[0],
                'pair' : dt[1],
                'way' : dt[2],
                'leverage' : dt[3],
                'pnl' : dt[4],
                'entry-p' : dt[5],
                'now-p' : dt[6],
                'ref' : dt[7],
                'date' : dt[8],
                'user_id' : user_id,
            }
            await bot.send_message(user_id, "Отправьте аватрку вашего аккаунта")
            await state.set_state(pnl_okx_state.img)
            
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(pnl_okx_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()      
        
@pnl_okx_router.message(F.photo, pnl_okx_state.img)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    cur.execute("SELECT * FROM rural_binance WHERE name = 'rural'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    
    file = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    file_path = file.file_path
    photo_path = f'tgbot/pnl_okx/{user_id}_ava.jpg'

    await bot.download_file(file_path, photo_path)
    
    global data
    gen(data)
    photo = FSInputFile(f'tgbot/pnl_okx/{user_id}_output.jpg')
    btn = main_menu_button()
    await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
    os.remove(f'tgbot/pnl_okx/{user_id}_output.jpg')
    await change_balance(user_id, price[2],'minus')
    
    data.clear()
    await state.clear()