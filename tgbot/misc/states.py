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
    
class gen_receipt_new_state(StatesGroup):
    user_id = State()
    gen_data = State()
    gen_data2 = State() 
    
class gen_receipt_new_state(StatesGroup):
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
    
class sber_qiwi_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class sber_sber_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class sber_sber_png_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class sber_tn_png_andr_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class rural_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class withdraw_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class tran_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class tran_check_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class twt_send_state(StatesGroup):
    user_id = State()
    gen_data = State()
class twt_rec_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class bin_donate_state(StatesGroup):
    user_id = State()
    gen_data = State()
class bin_with_draw_state(StatesGroup):
    user_id = State()
    gen_data = State()
class okx_state(StatesGroup):
    user_id = State()
    gen_data = State()
class pnl_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class okx_history_state(StatesGroup):
    user_id = State()
    gen_data = State()
    
class pnl_okx_state(StatesGroup):
    user_id = State()
    img = State()
    gen_data = State()

