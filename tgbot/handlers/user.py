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

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state

from tgbot.services.del_message import delete_message

from tgbot.misc.gen_donate import gen_donate
from tgbot.misc.gen_receipt import gen_receipt
from tgbot.misc.gen_tran import gen_tran
from tgbot.misc.gen_visa_tran import gen_visa_tran
from tgbot.misc.functions import auf

from tgbot.misc.texts import mess

from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, menu_tinkoff_button, theme_donate_button, tinkoff_format_button, balance_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text, StateFilter

user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

# commands=["start"]
@user_router.message(Command("start"))
async def user_start(message: types.Message):
    user_id = message.from_user.id
    
    auf_user = await auf(str(user_id))
    print(auf_user)
    if not auf_user:
        await reg_user(user_id)
        
    btn = main_menu_button()
    await bot.send_message(user_id, "Привет, выбери сервис",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Баланс')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = balance_menu_button()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"На твоем балансе - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text.in_({'Покупка акаунтов бирж', 'Покупка кошелька Юмани','Аккаунт бирж','Аккаунт кошельков'}))
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, "В разарботке",reply_markup=types.ReplyKeyboardRemove())
    
@user_router.message(F.text == 'Tinkoff')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = menu_tinkoff_button()
    await bot.send_message(user_id, "Выбери нужный скрин",reply_markup=btn.as_markup(resize_keyboard=True))
    
# , StateFilter('gen_state')
@user_router.message(F.text == 'Пополнение - Visa')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-visa-tran.jpg')
    await bot.send_photo(user_id, photo,caption=mess['visa-tran-description'],reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(gen_visa_tran_state.gen_data)
    
    
@user_router.message(F.text, gen_visa_tran_state.gen_data)
async def test_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
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
    await state.clear()
    
    
@user_router.message(F.text == 'Пополнение')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-donate.jpg')
    await bot.send_photo(user_id, photo,caption=mess['donate-description'],reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(gen_donate_state.gen_data)
    
@user_router.message(F.text, gen_donate_state.gen_data)
async def test_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
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
    await state.clear()
    
    
@user_router.message(F.text == 'Перевод - квитанция')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-donate.jpg')
    await bot.send_photo(user_id, photo,caption=mess['tran-description'],reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(gen_tran_state.gen_data)
    
@user_router.message(F.text, gen_tran_state.gen_data)
async def test_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
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
    await state.clear()
    
    
@user_router.message(F.text == 'Tinkoff квитанция')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = tinkoff_format_button()
    await bot.send_message(user_id, "Выбери нужный формат",reply_markup=btn.as_markup(resize_keyboard=True))
    

@user_router.message(F.text == 'Tinkoff квитанция pdf')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(gen_receipt_state.gen_data)
    
@user_router.message(F.text, gen_receipt_state.gen_data)
async def test_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
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
    photo = FSInputFile(f'tgbot/img/{user_id}_output_receipt.pdf')
    btn = main_menu_button()
    await bot.send_document(user_id, photo,reply_markup=btn.as_markup(resize_keyboard=True))
    os.remove(f'tgbot/img/{user_id}_output_receipt.pdf')
    os.remove(f'tgbot/img/{user_id}_output_receipt.png')
    await state.clear()
    
@user_router.message(F.text == 'Tinkoff квитанция png')
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = FSInputFile('tgbot/img/ex-receipt.jpg')
    await bot.send_photo(user_id, photo,caption=mess['receipt-description'],reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(gen_receipt_state.gen_data)
    
@user_router.message(F.text, gen_receipt_state.gen_data)
async def test_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
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
    await state.clear()
    
