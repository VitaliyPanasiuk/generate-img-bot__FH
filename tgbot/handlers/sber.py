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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state,withdrawal_to_tn_state,sber_qiwi_state,sber_sber_state,sber_sber_png_state,sber_tn_png_andr_state

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

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button,sber_menu_button,sber_sber_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

sber_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@sber_router.message(F.text == 'Чеки Сбербанк')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = sber_menu_button()
    await bot.send_message(user_id, "Выберите скрин",reply_markup=btn.as_markup(resize_keyboard=True))
    
@sber_router.message(F.text == 'Сбер - QiWi')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/sber/sber_qiwi/sber-qiwi-pdf-ex.png')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['sber-qiwi-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - qiwi'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(sber_qiwi_state.gen_data)
    
    
@sber_router.message(F.text, sber_qiwi_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - qiwi'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'sender':dt[0],
                'sender_card':dt[1],
                'sum_tran':dt[2],
                'commission':dt[3],
                'final_sum':dt[4],
                'receiver_card':dt[5],
                'receiver_contry':dt[6],
                'receiver_bank':dt[7],
                'prn_tran':dt[8],
                'num_tran':dt[9],
            }
            tr_time = dt[10]
            gen_sber_qiwi_pdf(data,tr_time,user_id)
            photo = FSInputFile(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.pdf')
            btn = main_menu_button()
            await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.pdf')
            os.remove(f'tgbot/sber/sber_qiwi/{user_id}_output_sber_qiwi_pdf.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(sber_qiwi_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
# sber sber
@sber_router.message(F.text == 'Сбер - Сбер')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = sber_sber_menu_button()
    await bot.send_message(user_id, "выберите формат",reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    
@sber_router.message(F.text == 'Сбер - Сбер pdf')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/sber/sber_sber/sber_sber_ex_pdf.png')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['sber-sber-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - sber'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(sber_sber_state.gen_data)
    
    
@sber_router.message(F.text, sber_sber_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - sber'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'fio_receiver':dt[0],
                'receiver_card':dt[1],
                'fio_sender':dt[2],
                'sender_card':dt[3],
                'sum_tran':dt[4],
                'commission':dt[5],
                'num_tran':dt[6],
                'kod':dt[7],
            }
            tr_time = dt[8]
            gen_sber_sber_pdf(data,tr_time,user_id)
            photo = FSInputFile(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.pdf')
            btn = main_menu_button()
            await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.pdf')
            os.remove(f'tgbot/sber/sber_sber/{user_id}_output_sber_sber_pdf.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(sber_sber_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@sber_router.message(F.text == 'Сбер - Сбер png')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/sber/sber_sber_png/sber_sber_png_ex.png')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['sber-sber-png-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - sber png'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(sber_sber_png_state.gen_data)
    
    
@sber_router.message(F.text, sber_sber_png_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - sber png'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'fio_receiver':dt[0],
                'receiver_card':dt[1],
                'fio_sender':dt[2],
                'sender_card':dt[3],
                'sum_tran':dt[4],
                'commission':dt[5],
                'num_tran':dt[6],
                'kod':dt[7],
            }
            tr_time = dt[8]
            phone_time = dt[9]
            gen_sber_sber_png(data,tr_time,phone_time,user_id)
            photo = FSInputFile(f'tgbot/sber/sber_sber_png/{user_id}_output_sber_sber_png.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/sber/sber_sber_png/{user_id}_output_sber_sber_png.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(sber_sber_png_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@sber_router.message(F.text == 'Сбер - Tinkoff')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/sber/sber_tn_png_andr/sber_tn_png_andr_ex.png')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['sber-tn-png-andr-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(sber_tn_png_andr_state.gen_data)
    
    
@sber_router.message(F.text, sber_tn_png_andr_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM sber_tariff WHERE name = 'sber - tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'fio_receiver':dt[0],
                'receiver_card':dt[1],
                'sum_tran':dt[2],
                'commission':dt[3],
                'final_sum':dt[4],
                'sender_card':dt[5],
                'receiver_contry':dt[6],
                'receiver_bank':dt[7],
                'num_tran':dt[8],
            }
            tr_time = dt[9]
            phone_time = dt[10]
            gen_sber_tn_png_andr(data,tr_time,phone_time,user_id)
            photo = FSInputFile(f'tgbot/sber/sber_tn_png_andr/{user_id}_output_sber_tn_png_andr.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/sber/sber_tn_png_andr/{user_id}_output_sber_tn_png_andr.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(sber_tn_png_andr_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()