from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def main_menu_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Чеки Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Чеки Сбербанк")
    )
    home_buttons.add(
        types.KeyboardButton(text="Чеки бирж")
    )
    home_buttons.add(
        types.KeyboardButton(text="Чеки кошельков")
    )
    home_buttons.add(
        types.KeyboardButton(text="Покупка бирж")
    )
    home_buttons.add(
        types.KeyboardButton(text="Покупка кошельков")
    )
    home_buttons.add(
        types.KeyboardButton(text="Баланс")
    )
    home_buttons.adjust(2)
    return home_buttons

def balance_menu_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Пополнить")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    return home_buttons

# def menu_tinkoff_button():
#     home_buttons = ReplyKeyboardBuilder()
#     home_buttons.add(
#         types.KeyboardButton(text="Пополнение - Visa")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Пополнение")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Перевод - квитанция")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Tinkoff квитанция")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Главное меню")
#     )
    
#     home_buttons.adjust(1)
#     return home_buttons

def menu_tinkoff_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Чеки полнения")
    )
    home_buttons.add(
        types.KeyboardButton(text="Чеки вывода")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    # home_buttons.add(
    #     types.KeyboardButton(text="Перевод - квитанция")
    # )
    # home_buttons.add(
    #     types.KeyboardButton(text="Tinkoff квитанция")
    # )

    
    home_buttons.adjust(1)
    return home_buttons

def checks_donate_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Пополнение - Visa")
    )
    home_buttons.add(
        types.KeyboardButton(text="Пополнение - Visa direct")
    )
    home_buttons.add(
        types.KeyboardButton(text="Пополнение - Перевод с карты")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    
    home_buttons.adjust(1)
    return home_buttons

def checks_withdrawal_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Tinkoff - Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Tinkoff - Банк")
    )
    home_buttons.add(
        types.KeyboardButton(text="Вывод на Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Вывод на Банк (pdf)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Tinkoff - Tinkoff (pdf)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    
    home_buttons.adjust(2,2,1,1)
    return home_buttons

def return_to_home_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    home_buttons.adjust(1)
    return home_buttons

def donate_choice_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Пополнить Фиатом")
    )
    home_buttons.add(
        types.KeyboardButton(text="Пополнить Криптой")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    home_buttons.adjust(1)
    return home_buttons


def admin_panel_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Тарифы")
    )
    home_buttons.add(
        types.KeyboardButton(text="Рассылка")
    )
    home_buttons.add(
        types.KeyboardButton(text="Вывод валют")
    )
    home_buttons.add(
        types.KeyboardButton(text="Изменение баланса")
    )
    home_buttons.add(
        types.KeyboardButton(text="Реквизиты")
    )
    home_buttons.add(
        types.KeyboardButton(text="Транзакции")
    )
    home_buttons.add(
        types.KeyboardButton(text="Посмотреть информацию про инвестора")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    
    home_buttons.adjust(3,3,1,1)
    return home_buttons

def tariff_panel_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Сбербанк")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Чеки бирж")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Чеки кошельков")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Покупка бирж")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тарифы - Покупка кошельков")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    home_buttons.add(
        types.KeyboardButton(text="Админ меню")
    )
    
    home_buttons.adjust(3,2,1,1,1)
    return home_buttons


def tn_tariffs_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Пополнение - Visa")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Пополнение - Visa direct")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Пополнение - Перевод с карты")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Tinkoff - Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Tinkoff - Банк")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Вывод на Tinkoff")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Вывод на Банк (pdf)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тариф - Tinkoff - Tinkoff (pdf)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Главное меню")
    )
    home_buttons.add(
        types.KeyboardButton(text="Админ меню")
    )
    
    home_buttons.adjust(2,2,2,2,2)
    return home_buttons

def admin_return_menu_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Админ меню")
    )
    return home_buttons


def changing_requisites_menu_button():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Изменить адрес крипто кошелька")
    )
    home_buttons.add(
        types.KeyboardButton(text="Изменить номер карты")
    )
    home_buttons.add(
        types.KeyboardButton(text="Админ меню")
    )
    return home_buttons