import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

import logging

async def update_balance(operation, new_balance,user_id):
    config = load_config(".env")
    
    base = psycopg2.connect(dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,)
    
    cur = base.cursor()
    
    if operation == "plus":
        cur.execute(
                """UPDATE users SET balance = balance + %s WHERE id = %s""", (int(new_balance) ,str(user_id))
            )
    else:
        cur.execute(
                """UPDATE users SET balance = balance - %s WHERE id = %s""", (int(new_balance) ,str(user_id))
            )
        
    base.commit()
        
async def reg_user(user_id):
    config = load_config(".env")
    
    base = psycopg2.connect(dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,)
    
    cur = base.cursor()
    cur.execute("INSERT INTO users (id) VALUES (%s)",(str(user_id),))
    
    base.commit()
    
    
    