from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import PreCheckoutQuery, CallbackQuery, LabeledPrice, Message
from sqlalchemy import select

from app.database.database import async_session
from app.database.models import Users
from app.keyboards import payment, main

router_payment = Router()

@router_payment.callback_query(F.data.startswith('topup'))
async def top_up(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 Выберите сумму для пополнения:",
        reply_markup=payment
    )
    await callback.answer()


@router_payment.callback_query(F.data == "stars_100")
async def process_stars_100(callback: CallbackQuery):
    amount = 100
    prices = [LabeledPrice(label=f"{amount} Stars", amount=amount)]

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Пополнение баланса на {amount} Stars",
        description="Пополнение внутреннего баланса бота",
        payload=f"stars_{amount}_{callback.from_user.id}",
        currency="XTR",  # Stars
        prices=prices,
        provider_token=None,  # для Stars можно None
        start_parameter="stars_payment",
        need_email=False,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()



@router_payment.callback_query(F.data == "stars_350")
async def process_stars_350(callback: CallbackQuery):
    amount = 350
    prices = [LabeledPrice(label=f"{amount} Stars", amount=amount)]

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Пополнение баланса на {amount} Stars",
        description="Пополнение внутреннего баланса бота",
        payload=f"stars_{amount}_{callback.from_user.id}",
        currency="XTR",
        prices=prices,
        provider_token=None,
        start_parameter="stars_payment",
        need_email=False,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()


@router_payment.callback_query(F.data == "stars_1")
async def process_stars_1(callback: CallbackQuery):
    amount = 1
    prices = [LabeledPrice(label=f"{amount} Stars", amount=amount)]

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Пополнение баланса на {amount} Stars",
        description="Пополнение внутреннего баланса бота",
        payload=f"stars_{amount}_{callback.from_user.id}",
        currency="XTR",
        prices=prices,
        provider_token=None,
        start_parameter="stars_payment",
        need_email=False,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False
    )
    await callback.answer()

@router_payment.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router_payment.message(F.successful_payment)
async def success_payment(message: Message):
    tg_id = str(message.from_user.id)
    amount = message.successful_payment.total_amount

    async with async_session() as session:
        result = await session.execute(
            select(Users).where(Users.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()

        if user:
            user.stars += amount
            new_balance = user.stars
            await session.commit()

            await message.answer(
                f"✅ <b>Оплата прошла успешно!</b>\n\n"
                f"💫 <b>Вам начислено:</b> {amount} ⭐ Stars\n"
                f"💰 <b>Теперь ваш баланс:</b> {new_balance} ⭐\n\n"
                f"🎯 <b>Что делать дальше?</b>\n\n"
                f"• Если вы пополнили баланс на <b>100⭐</b> - нажмите на /information, "
                f"выберите человека которого хотите пробить и нажмите кнопку после картинки\n\n"
                f"• Если вы пополнили баланс на <b>350⭐</b> - нажмите на кнопку \n"
                f"🗝️Купить админку\n\n"
                f"⚡ <i>Приятного использования!</i>",
                reply_markup=main,
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ Ошибка: пользователь не найден")



@router_payment.message(Command('bot_balance'))
async def get_bot_balance(message: Message, bot):
    result = await bot.get_star_transactions(limit=100)
    transactions = result.transactions  # получаем список транзакций

    if not transactions:
        await message.answer("❌ Пока нет транзакций со звёздами")
        return

    total_income = sum(tx.amount for tx in transactions if tx.amount > 0)

    await message.answer(
        f"💰 Бот заработал {total_income} ⭐ Stars (по последним {len(transactions)} транзакциям)"
    )