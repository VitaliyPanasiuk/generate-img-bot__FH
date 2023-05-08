import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

import logging



async def postgre_start():
    config = load_config(".env")
    
    base = psycopg2.connect(dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,)
    
    cur = base.cursor()
    if base:
        logging.info(f"data base connect success!")
        
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id BIGINT  PRIMARY KEY,
        balance INTEGER default 10
        )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS tn_tariff(
        id    serial PRIMARY KEY,
        name  text,
        costs integer)''')
    
    
    cur.execute('''CREATE TABLE IF NOT EXISTS requisites(
        id     serial PRIMARY KEY,
        name   text,
        adress text)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
            id      serial PRIMARY KEY,
            user_id bigint,
            photo   text,
            time    text,
            status  boolean
        )''')
    
    
    base.commit()
    cur.close()
    base.close()