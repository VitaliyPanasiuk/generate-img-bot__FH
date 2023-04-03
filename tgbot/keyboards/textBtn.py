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
# def theme_donate_button():
#     home_buttons = ReplyKeyboardBuilder()
#     home_buttons.add(
#         types.KeyboardButton(text="Пополнение - черная тема")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Пополнение - белая тема")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Главное меню")
#     )
    
#     home_buttons.adjust(1)
#     return home_buttons

# def tinkoff_format_button():
#     home_buttons = ReplyKeyboardBuilder()
#     home_buttons.add(
#         types.KeyboardButton(text="Tinkoff квитанция pdf")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Tinkoff квитанция png")
#     )
#     home_buttons.add(
#         types.KeyboardButton(text="Главное меню")
#     )
    
#     home_buttons.adjust(1)
#     return home_buttons
