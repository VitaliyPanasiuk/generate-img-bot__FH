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
from datetime import datetime
import requests
import asyncio

from tgbot.misc.states import gen_donate_state, gen_receipt_state, gen_tran_state, gen_visa_tran_state,gen_tn_bank_state,gen_to_bank_pdf_state,await_photo_of_transaction_state

from tgbot.services.del_message import delete_message

from tgbot.misc.gen_donate import gen_donate
from tgbot.misc.gen_receipt import gen_receipt
from tgbot.misc.gen_tran import gen_tran
from tgbot.misc.gen_visa_tran import gen_visa_tran
from tgbot.misc.gen_tn_bank import gen_tn_bank
from tgbot.misc.gen_receipt_pdf import gen_receipt_pdf
from tgbot.misc.gen_to_bank_pdf import gen_to_bank_pdf
from tgbot.misc.functions import auf,add_transaction

from tgbot.misc.texts import mess

# from tgbot.keyboards.inlineBtn import CastomCallback
from tgbot.keyboards.textBtn import main_menu_button, balance_menu_button, menu_tinkoff_button,checks_donate_button,checks_withdrawal_button,return_to_home_button,donate_choice_button,binance_menu_button,wallets_menu_button, exchange_menu_button,okx_menu_button
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext
from tgbot.keyboards.inlineBtn import CastomCallbackOfEndingTransaction, transaction_button

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
    text = message.text
    auf_user = await auf(str(user_id))
    print(auf_user)
    if not auf_user:
        await reg_user(user_id)
        
    btn = main_menu_button()
    await bot.send_message(user_id, "Привет, выбери сервис",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Главное меню')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    btn = main_menu_button()
    await bot.send_message(user_id, "Привет, выбери сервис",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Okx')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    btn = okx_menu_button()
    await bot.send_message(user_id, "Привет, выбери тип скрина",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Binance')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    btn = binance_menu_button()
    await bot.send_message(user_id, "Привет, выбери нужный скрин",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Баланс')
async def user_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = balance_menu_button()
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    balance = cur.fetchone()
    await bot.send_message(user_id, f"На твоем балансе - {balance[1]}",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Пополнить')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # cur.execute("SELECT * FROM requisites WHERE name = 'btc'")
    # adress = cur.fetchone()
    # cur.execute("SELECT * FROM requisites WHERE name = 'fiat'")
    # adress2 = cur.fetchone()
    
    # btn = return_to_home_button()
    btn = donate_choice_button()
    await bot.send_message(user_id, f"Выберите способ пополнения",reply_markup=btn.as_markup(resize_keyboard=True))
    # await bot.send_message(user_id, f"Адрес для пополнения криптой- {adress[2]}\nНомер карты для фиата - {adress2[2]}\nПосле отправки денег, отправьте пожалуйста скриншот с транзакцией",reply_markup=btn.as_markup(resize_keyboard=True))
    # await state.set_state(await_photo_of_transaction_state.photo)
    
@user_router.message(F.text == 'Пополнить Фиатом')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    
    cur.execute("SELECT * FROM requisites WHERE name = 'card'")
    adress = cur.fetchone()
    
    btn = return_to_home_button()
    await bot.send_message(user_id, f"Номер карты для фиата - {adress[2]}\nПосле отправки денег, отправьте пожалуйста скриншот с транзакцией",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(await_photo_of_transaction_state.photo)
    
    
    
@user_router.message(F.text == 'Пополнить Криптой')
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    cur.execute("SELECT * FROM requisites WHERE name = 'btc'")
    adress = cur.fetchone()
    
    btn = return_to_home_button()
    await bot.send_message(user_id, f"Адрес для пополнения криптой- {adress[2]}\nПосле отправки денег, отправьте пожалуйста скриншот с транзакцией",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(await_photo_of_transaction_state.photo)
    
    
@user_router.message(F.photo, await_photo_of_transaction_state.photo)
async def user_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    file = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    file_path = file.file_path
    current_datetime = str(datetime.now()).replace(' ','').replace('.','').replace('-','').replace(':','')
    s_current_datetime = str(datetime.now())
    photo_path = 'tgbot/transactions_img/'+ str(user_id) + '-' + str(current_datetime) +'.jpg'

    await bot.download_file(file_path, photo_path)
    await add_transaction(user_id, photo_path,s_current_datetime)
    
    btn = main_menu_button()
    await bot.send_message(user_id, f"Информация отправлена на проверку",reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    cur.execute(f"SELECT * FROM transactions WHERE time = '{s_current_datetime}'")
    transaction = cur.fetchone()
    
    # [762342298,6197913672]
    photo = FSInputFile(photo_path)
    btn = transaction_button(transaction[0])
    await bot.send_photo(chat_id = 762342298, photo = photo, caption=f'''Заявка №{transaction[0]}
Id пользователя: {user_id}
Имя пользователя: {message.from_user.username}\n''',
reply_markup=btn.as_markup())
    
    # photo = FSInputFile(photo_path)
    # btn = transaction_button(i[0])
    # await bot.send_photo(user_id, photo,caption=f'id: {i[0]} \nuser_id: {i[1]}\ntime: {i[3]}\n',reply_markup=btn.as_markup())
    
    await state.clear()
    
    
    
@user_router.message(F.text.in_({'Покупка акаунтов бирж', 'Покупка кошелька Юмани','Аккаунт бирж','Аккаунт кошельков'}))
async def user_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = main_menu_button()
    await bot.send_message(user_id, "В разарботке",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Чеки Tinkoff')
async def checks_tn(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = menu_tinkoff_button()
    await bot.send_message(user_id, "Выбери тип чеков",reply_markup=btn.as_markup(resize_keyboard=True))


@user_router.message(F.text == 'Чеки полнения')
async def checks_donate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = checks_donate_button()
    await bot.send_message(user_id, "Выбери нужный чек",reply_markup=btn.as_markup(resize_keyboard=True))

@user_router.message(F.text == 'Чеки вывода')
async def checks_withdrawal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = checks_withdrawal_button()
    await bot.send_message(user_id, "Выбери нужный чек",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Чеки кошельков')
async def checks_withdrawal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = wallets_menu_button()
    await bot.send_message(user_id, "Выбери нужный кошелек",reply_markup=btn.as_markup(resize_keyboard=True))
    
@user_router.message(F.text == 'Чеки бирж')
async def checks_withdrawal(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = exchange_menu_button()
    await bot.send_message(user_id, "Выбери нужный кошелек",reply_markup=btn.as_markup(resize_keyboard=True))
    