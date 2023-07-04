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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state,withdrawal_to_tn_state,gen_receipt_new_state,gen_receipt_new_state

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

from tgbot.tn.tn_receipt_new_pdf.tn_receipt_new_pdf import gen_new_receipt_pdf
from tgbot.tn.tn_tn_new.tn_tn_new_png import gen_receipt_new_png

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

tn_withdrawal_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@tn_withdrawal_router.message(F.text == 'Tinkoff - Tinkoff (pdf) старый')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn pdf'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_receipt_state.gen_data)
    
@tn_withdrawal_router.message(F.text, gen_receipt_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn pdf'")
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
                'sender' : dt[3],
                'card_receiver' : dt[4],
                'receiver' : dt[5],
                'id_tran' : dt[6],
            }
            gen_receipt_pdf(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_receipt.pdf')
            btn = main_menu_button()
            await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_receipt.pdf')
            os.remove(f'tgbot/img/{user_id}_output_receipt.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_receipt_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@tn_withdrawal_router.message(F.text == 'Tinkoff - Tinkoff (pdf) новый')
async def tn_tn_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn pdf'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_receipt_new_state.gen_data)
    
@tn_withdrawal_router.message(F.text, gen_receipt_new_state.gen_data)
async def tn_tn_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn pdf'")
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
                'sender' : dt[3],
                'card_receiver' : dt[4],
                'receiver' : dt[5],
                'id_tran' : dt[6],
            }
            gen_new_receipt_pdf(data,user_id)
            photo = FSInputFile(f'tgbot/tn/{user_id}_output_new_receipt.pdf')
            btn = main_menu_button()
            await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/tn/{user_id}_output_new_receipt.pdf')
            os.remove(f'tgbot/tn/{user_id}_output_new_receipt.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_receipt_new_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
    
@tn_withdrawal_router.message(F.text == 'Tinkoff - Tinkoff старый')
async def tn_tn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_receipt_state.gen_data2)
    
@tn_withdrawal_router.message(F.text, gen_receipt_state.gen_data2)
async def tn_tn_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn'")
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
                'sender' : dt[3],
                'card_receiver' : dt[4],
                'receiver' : dt[5],
                'id_tran' : dt[6],
            }
            gen_receipt(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_receipt.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_receipt.png')
            os.remove(f'tgbot/img/{user_id}_output_receipt.pdf')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_receipt_state.gen_data2)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
@tn_withdrawal_router.message(F.text == 'Tinkoff - Tinkoff новый')
async def tn_tn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_receipt_new_state.gen_data2)
    
@tn_withdrawal_router.message(F.text, gen_receipt_new_state.gen_data2)
async def tn_tn_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn'")
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
                'sender' : dt[3],
                'card_receiver' : dt[4],
                'receiver' : dt[5],
                'id_tran' : dt[6],
            }
            gen_receipt_new_png(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_new_receipt_png.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_new_receipt_png.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_receipt_new_state.gen_data2)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
    
@tn_withdrawal_router.message(F.text == 'Вывод на Tinkoff')
async def withdrawal_to_tn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-tn-bank.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['tn-bank'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(withdrawal_to_tn_state.gen_data)
    
@tn_withdrawal_router.message(F.text, withdrawal_to_tn_state.gen_data)
async def withdrawal_to_tn_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to tn'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time' : dt[0],
                'balance' : dt[1],
                'tran_sum' : dt[2],
                'tn_name' : dt[3],
                'card_num' : dt[4],
            }
            gen_tn_bank(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_withdrawal_to_tn.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_withdrawal_to_tn.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except:
            btn = main_menu_button()
            print(f"Problem with data from user")
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(withdrawal_to_tn_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
@tn_withdrawal_router.message(F.text == 'Вывод на Банк (pdf)')
async def withdrawal_to_bank_pdf(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex_to_bank_pdf.png')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['tn-to-bank-pdf'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to bank pdf'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_to_bank_pdf_state.gen_data)
    
@tn_withdrawal_router.message(F.text, gen_to_bank_pdf_state.gen_data)
async def withdrawal_to_bank_pdf_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to bank pdf'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'tn-time' : dt[0],
                'tran-sum' : dt[1],
                'sender' : dt[2],
                'id-tran' : dt[3],
            }
            gen_to_bank_pdf(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_to_bank_pdf.pdf')
            btn = main_menu_button()
            await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_to_bank_pdf.png')
            os.remove(f'tgbot/img/{user_id}_output_to_bank_pdf.pdf')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except:
            btn = main_menu_button()
            print(f"Problem with data from user")
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_to_bank_pdf_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
    
@tn_withdrawal_router.message(F.text == 'Tinkoff - Банк')
async def tn_tn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex_tn_to_bank.jpg')
    btn = return_to_home_button()
    await bot.send_photo(user_id, photo,caption=mess['tn-to-bank-description'],reply_markup=btn.as_markup(resize_keyboard=True))
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - bank'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s",(user_id,))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"Стоимость генерации {price[2]}\nНа вашем счету - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(gen_tn_bank_state.gen_data)
    
@tn_withdrawal_router.message(F.text, gen_tn_bank_state.gen_data)
async def tn_tn_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - bank'")
    price = cur.fetchone()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    if balance[1] >= price[2]:
        try:
            dt = message.text.splitlines()
            data = {
                'time' : dt[0],
                'tn-time' : dt[1],
                'tran-sum' : dt[2],
                'sender' : dt[3],
                'comision' : dt[4],
                'card-receiver' : dt[5],
                'id-tran' : dt[6],
            }
            gen_tn_to_bank(data,user_id)
            photo = FSInputFile(f'tgbot/img/{user_id}_output_tn_to_bank.png')
            btn = main_menu_button()
            await bot.send_photo(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
            os.remove(f'tgbot/img/{user_id}_output_tn_to_bank.png')
            await change_balance(user_id, price[2],'minus')
            
            await state.clear()
        except Exception as e:
            btn = main_menu_button()
            print(f"Problem with data from user")
            print(e)
            await bot.send_message(user_id, "Данные были введены не верно, попробуйте еще раз",reply_markup=btn.as_markup(resize_keyboard=True))
            await state.set_state(gen_tn_bank_state.gen_data)
    else:
        btn = main_menu_button()
        await bot.send_message(user_id, "На счету недостаточно средрсв, пополните сначала баланс",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
        
        
        
        