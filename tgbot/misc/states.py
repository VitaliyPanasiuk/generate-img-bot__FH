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
    
class gen_tn_bank_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class gen_to_bank_pdf_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class withdrawal_to_tn_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class withdrawal_to_tn_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class mailling_state(StatesGroup):
    message = State()
    
class change_tariff_state(StatesGroup):
    name_of_tariff = State()
    new_price = State()
    
class change_balance_state(StatesGroup):
    user = State()
    amount = State()
    
class change_requisites_state(StatesGroup):
    adress = State()
    adress2 = State()
    
    
class await_photo_of_transaction_state(StatesGroup):
    photo = State()
    
class end_change_balance_state(StatesGroup):
    user = State()
    order_id = State()
    amount = State()

