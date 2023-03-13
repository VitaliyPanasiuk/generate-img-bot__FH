from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class gen_visa_tran_state(StatesGroup):
    user_id = State()
    time = State()
    tn_time = State()
    tran_sum = State()
    tn_balance = State()
    tn_month = State()
    tn_month_spend = State()
    

class gen_donate_state(StatesGroup):
    user_id = State()
    gen_data = State()
class gen_receipt_state(StatesGroup):
    user_id = State()
    gen_data = State()
    gen_data2 = State()
class gen_tran_state(StatesGroup):
    user_id = State()
    gen_data = State()
class gen_visa_tran_state(StatesGroup):
    user_id = State()
    gen_data = State()

