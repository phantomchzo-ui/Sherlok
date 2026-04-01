from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

btn_topup = InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="topup")
btn_back = InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
admin_btn = InlineKeyboardButton(text='Все данные', callback_data='showdata')

main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🕵️Мой Профиль', callback_data='profile'),
        InlineKeyboardButton(text='💰Мой Баланс', callback_data='balance')
    ],
    [btn_topup],
    [
        InlineKeyboardButton(text='🗝️Купить админку', callback_data='buyadmin')
    ],
[
        InlineKeyboardButton(text='🔍Бесплатный запрос', callback_data='rufina')
    ],
    [
        InlineKeyboardButton(text='⚙️Помощь', callback_data='helps')
    ]
])

payment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оплатить 100', callback_data='stars_100')],
    [InlineKeyboardButton(text='Оплатить 350', callback_data='stars_350')],
    [InlineKeyboardButton(text='Оплатить 1', callback_data='stars_1')],
    [btn_back]
])


async def show_persons(person_id:int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=f'Посмотреть все данные',
            callback_data=f'data_{person_id}'
        )
    )
    return keyboard.as_markup()


back_button = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back]
])

balance_menu = InlineKeyboardMarkup(inline_keyboard=[
    [btn_topup],
    [btn_back]
])

admin_button = InlineKeyboardMarkup(inline_keyboard=[
    [admin_btn],
    [btn_back]
])


