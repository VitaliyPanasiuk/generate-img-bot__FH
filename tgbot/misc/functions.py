from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

import datetime
import asyncio

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()

async def auf(user_id):
    cur.execute("SELECT * FROM users WHERE id = %s", (str(user_id),))
    buyer = cur.fetchall()
    if len(buyer) > 0:
        return True
    else:
        return False
    
    
async def change_balance(user_id, amount, way):
    if way == 'plus':
        cur.execute("UPDATE users SET balance = balance + %s  WHERE id = %s", (int(amount),str(user_id)))
    else:
        cur.execute("UPDATE users SET balance = balance - %s  WHERE id = %s", (int(amount),str(user_id)))
        
    base.commit()
    
async def add_transaction(user_id, photo, time):
    cur.execute("INSERT INTO transactions (user_id, photo, time, status) VALUES (%s,%s,%s,FALSE)",(user_id, photo, time))
        
    base.commit()
    
async def end_transaction(tr_id):
    cur.execute("UPDATE transactions SET status = TRUE  WHERE id = %s", (tr_id,))
        
    base.commit()
    

    