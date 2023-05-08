from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

from tgbot.keyboards.textBtn import admin_panel_button, tariff_panel_button, tn_tariffs_button,admin_return_menu_button,main_menu_button,changing_requisites_menu_button
from tgbot.misc.states import mailling_state,change_tariff_state,change_balance_state,change_requisites_state,await_photo_of_transaction_state,end_change_balance_state

from tgbot.misc.functions import auf,change_balance,end_transaction

import time
import datetime
import requests
import asyncio

from tgbot.services.del_message import delete_message

from tgbot.keyboards.inlineBtn import CastomCallbackOfEndingTransaction, transaction_button
from aiogram.filters import Command, Text, StateFilter
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    btn = admin_panel_button()
    await message.reply("привет админ!",reply_markup=btn.as_markup(resize_keyboard=True))
    
@admin_router.message(F.text == 'Админ меню')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await state.clear()
    
    btn = admin_panel_button()
    await message.reply("привет админ!",reply_markup=btn.as_markup(resize_keyboard=True))
    
# @admin_router.message(F.text == 'Главное меню')
# async def user_main_menu(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     await state.clear()
#     btn = main_menu_button()
#     await bot.send_message(user_id, "Привет, выбери сервис",reply_markup=btn.as_markup(resize_keyboard=True))
    
    
@admin_router.message(F.text == 'Рассылка')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    
    await bot.send_message(user_id, "Отправьте соообщение которое будет разослано всем пользователям",reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(mailling_state.message)
    

@admin_router.message(F.text, mailling_state.message)
async def admin_mailling_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    
    try:
        for i in users:
            if i[0] != user_id:
                await bot.send_message(i[0],text)
    except Exception:
        print(Exception)
        print('trouble whith mailling')

    btn = admin_panel_button()
    await bot.send_message(user_id, "Сообщение было отправлено",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.clear()
    
    
@admin_router.message(F.text == 'Тарифы')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    btn = tariff_panel_button()
    await bot.send_message(user_id, "Выберите нужный раздел",reply_markup=btn.as_markup(resize_keyboard=True))

@admin_router.message(F.text == 'Тарифы - Tinkoff')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    btn = tn_tariffs_button()
    await bot.send_message(user_id, "Выберите скрин на котором хотите изменить тариф(по умолчанию 30)",reply_markup=btn.as_markup(resize_keyboard=True))



# handlers for changing tariffs 
@admin_router.message(F.text == 'Тариф - Пополнение - Visa')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='donate-visa')
    
@admin_router.message(F.text == 'Тариф - Пополнение - Visa direct')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-visa direct'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='donate-visa direct')
    
@admin_router.message(F.text == 'Тариф - Пополнение - Перевод с карты')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'donate-card transaction'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='donate-card transaction')
    
@admin_router.message(F.text == 'Тариф - Tinkoff - Tinkoff')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='tn - tn')
    
@admin_router.message(F.text == 'Тариф - Tinkoff - Банк')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - bank'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='tn - bank')
    
@admin_router.message(F.text == 'Тариф - Вывод на Tinkoff')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to tn'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='wn to tn')
    
@admin_router.message(F.text == 'Тариф - Вывод на Банк (pdf)')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'wn to bank pdf'")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='wn to bank pdf')
    
@admin_router.message(F.text == 'Тариф - Tinkoff - Tinkoff (pdf)')
async def admin_mailling(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    cur.execute("SELECT * FROM tn_tariff WHERE name = 'tn - tn pdf '")
    price = cur.fetchone()
    text = f'Введите новую цену, текущая цена скрина - {price[2]}'
    await bot.send_message(user_id, text,reply_markup=btn.as_markup(resize_keyboard=True))
    
    
    await state.set_state(change_tariff_state.new_price)
    await state.update_data(name_of_tariff='tn - tn pdf ')
    
@admin_router.message(F.text, change_tariff_state.new_price)
async def donate_transaction_from_card_s(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    user_data = await state.get_data()
    cur.execute('UPDATE tn_tariff SET costs = %s WHERE name =  %s',(int(text),user_data['name_of_tariff']))
    
    btn = admin_panel_button()
    await bot.send_message(user_id, "Цена была изменена",reply_markup=btn.as_markup(resize_keyboard=True))
    
    base.commit()
    await state.clear()
    
    
# function for changing balance of users

@admin_router.message(F.text == 'Изменение баланса')
async def changing_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = admin_return_menu_button()
    await bot.send_message(user_id, "Введите id пользователя",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(change_balance_state.user)
    
    
@admin_router.message(F.text, change_balance_state.user)
async def changing_balance_get_userid(message: types.Message, state: FSMContext):
    user_id = message.from_user.id 
    await state.update_data(user=message.text) 
    btn = admin_return_menu_button()
    await bot.send_message(user_id, "Введите сумму которую стоит добавить к балансу пользователя",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(change_balance_state.amount)
    
@admin_router.message(F.text, change_balance_state.amount)
async def changing_balance_get_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  
    await state.update_data(amount=message.text) 
    btn = admin_panel_button()
    user_data = await state.get_data()
    try:
        await change_balance(user_data['user'], int(user_data['amount']),'plus')
        await state.clear()
        await bot.send_message(user_id, "Баланс пользователя был изменен",reply_markup=btn.as_markup(resize_keyboard=True))
        
    except:
        await bot.send_message(user_id, "Данные были введени не верно",reply_markup=btn.as_markup(resize_keyboard=True))
        await state.clear()
    
# changing requisites

@admin_router.message(F.text == 'Реквизиты')
async def changing_requisites(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    btn = changing_requisites_menu_button()
    await bot.send_message(user_id, "Выберите реквизиты которые хотите изменить",reply_markup=btn.as_markup(resize_keyboard=True))
    # await state.set_state(change_requisites_state.adress)
    
@admin_router.message(F.text == 'Изменить адрес крипто кошелька')
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    cur.execute("SELECT * FROM requisites WHERE name = 'btc'")
    adress = cur.fetchone()
    
    btn = admin_return_menu_button()
    await bot.send_message(user_id, f"Текущий адрес - {adress[2]}\nВведите новый адрес или выйдите в главное меню",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(change_requisites_state.adress)
    
@admin_router.message(F.text, change_requisites_state.adress)
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    cur.execute("UPDATE requisites SET adress = %s WHERE name =  'btc'",(text,))
    base.commit()
    
    btn = admin_panel_button()
    await bot.send_message(user_id, "Адресс был изменен",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.clear()
    
@admin_router.message(F.text == 'Изменить номер карты')
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    cur.execute("SELECT * FROM requisites WHERE name = 'fiat'")
    adress = cur.fetchone()
    
    btn = admin_return_menu_button()
    await bot.send_message(user_id, f"Текущий номер - {adress[2]}\nВведите новый номер карты или выйдите в главное меню",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.set_state(change_requisites_state.adress2)
    
@admin_router.message(F.text, change_requisites_state.adress2)
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    cur.execute("UPDATE requisites SET adress = %s WHERE name =  'fiat'",(text,))
    base.commit()
    
    btn = admin_panel_button()
    await bot.send_message(user_id, "Номер карты был изменен",reply_markup=btn.as_markup(resize_keyboard=True))
    await state.clear()


# handling ending of transaction
@admin_router.message(F.text == 'Транзакции')
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    cur.execute("SELECT * FROM transactions WHERE status = FALSE")
    transactions = cur.fetchall()

    for i in transactions:
        photo = FSInputFile(i[2])
        btn = transaction_button(i[0])
        await bot.send_photo(user_id, photo,caption=f'id: {i[0]} \nuser_id: {i[1]}\ntime: {i[3]}\n',reply_markup=btn.as_markup())


@admin_router.callback_query(CastomCallbackOfEndingTransaction.filter(F.action == "end_transaction"))
async def user_start(callback_query: types.CallbackQuery,callback_data: CastomCallbackOfEndingTransaction,state: FSMContext,):
    user_id = callback_query.from_user.id
    order_id = callback_data.transaction_id
    
    btn = admin_return_menu_button()
    await bot.send_message(user_id, "Отправьте сумму которую нужно добавить на баланс",reply_markup=btn.as_markup(resize_keyboard=True))
    
    cur.execute("SELECT * FROM transactions WHERE id = %s",(order_id,))
    transactions = cur.fetchone()
    await state.update_data(user=transactions[1])
    await state.update_data(order_id=order_id)
    await state.set_state(end_change_balance_state.amount)
    
    
    
    
@admin_router.message(F.text, end_change_balance_state.amount)
async def changing_requisites_crypto(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    
    btn = admin_return_menu_button()
    await bot.send_message(user_id, "Транзакция была закрыта, деньги отправлены на счет пользователя",reply_markup=btn.as_markup(resize_keyboard=True))
    
    user_data = await state.get_data()
    await change_balance(user_data['user'],text,'plus')
    await end_transaction(user_data['order_id'])
    
    await state.clear()
    
    