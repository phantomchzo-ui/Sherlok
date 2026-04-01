from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from app.database.database import async_session
from app.database.models import Users
from app.database.requests import (check_user, check_admin, get_all_data, check_stars, get_persons_with_id,
                                   show_profile_user, get_person_by_id, check_to_buy_admin, get_ruf)
from app.keyboards import show_persons, main, back_button, balance_menu, admin_button

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    #await message.answer(message.from_user.first_name)
    tg_id = str(message.from_user.id)

    in_db = await check_user(str(tg_id))
    if not in_db:
        async with async_session() as session:
            user = Users(tg_id=tg_id, name=message.from_user.first_name, stars=0)
            session.add(user)
            await session.commit()
    await message.answer("Привет! 👋\n"
    "Я помогу тебе найти информацию о блогерах, тиктокерах и других создателях контента. \n"
    "Просто нажми на /information чтобы посмотреть какие блогеры у нас есть в база данных."
                         " Чтобы узнать подробнее нажмите на кнопку ⚙️Помощь", reply_markup=main
                         )

@router.message(Command('information'))
async def get_info(message: Message):
    await message.answer(
        '📱 Тут вы можете найти информацию о своих любимых блогерах, тиктокерах и их личные данные'
    )

    persons_data = await get_persons_with_id()


    if not persons_data:
        await message.answer('❌ Список блогеров пуст')
        return

    for person_id, image, name in persons_data:
        if image:
            try:
                person_keyboard = await show_persons(person_id)

                await message.answer_photo(
                    photo=image,
                    caption=f"🎬 <b>{name}</b>",
                    parse_mode='HTML',
                    reply_markup=person_keyboard
                )
            except Exception as e:
                await message.answer(f"🎬 <b>{name}</b>\n❌ Ошибка: {str(e)}")
        else:
            person_keyboard = await show_persons(person_id)
            await message.answer(
                f"🎬 <b>{name}</b>\n📷 Фото отсутствует",
                parse_mode='HTML',
                reply_markup=person_keyboard
            )
    await message.answer("📸 Посмотрите фото → 👤 Выберите человека → ℹ️ Нажмите «Все данные» под фото")


@router.callback_query(F.data.startswith('data_'))
async def getting_data(callback: CallbackQuery):
    await callback.answer()
    person_id = int(callback.data.split("_")[1])
    tg_id = str(callback.from_user.id)
    correct_balance = await check_stars(tg_id)
    person = await get_person_by_id(person_id)

    if not person:
        await callback.answer('Error !!!!!!!')
        return

    if correct_balance:
        await callback.message.answer_photo(
            photo=person.image,
            caption=f"────────────────\n"
                    f"👤 <b>ФИО:</b> {person.name}\n"
                    f"📱 <b>Телефон:</b> {person.phone}\n"
                    f"🆔 <b>ИИН:</b> {person.iin}\n"
                    f"🏠 <b>Адрес:</b> {person.address}\n"
                    f"📧 <b>Email:</b> {person.email}\n"
                    f"────────────────",
            parse_mode='HTML'
        )
        await callback.message.delete()
    else:
        await callback.message.answer('Недостаточно средств, пополните баланс', reply_markup=main)



@router.callback_query(F.data.startswith('profile'))
async def show_profile_of_user(callback: CallbackQuery):
    tg_id = str(callback.from_user.id)
    #await callback.answer('Загружаем профиль')
    await callback.message.delete()
    user = await show_profile_user(tg_id)

    if user:
        user_info = f"👤 <b>Профиль пользователя</b>\n\n" \
                    f"🆔 TG ID: {user.tg_id}\n" \
                    f"📛 Имя: {user.name}\n" \
                    f"⭐ Звезды: {user.stars}\n" \
                    f"✅ Админ: {'Да' if user.is_permission else 'Нет'}\n" \
                    f"📅 Дата регистрации: {user.created_at}"

        await callback.message.answer(user_info, parse_mode='HTML', reply_markup=back_button)
    else:
        await callback.message.answer("❌ Пользователь не найден")


@router.callback_query(F.data.startswith('helps'))
async def cmd_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "💰 <b>Тарифы и условия:</b>\n\n"
        "🔍 <b>Один запрос:</b>\n"
        "• Стоимость: 100 звёзд\n"
        "• Эквивалент: 1000 ₸ / 150 ₽\n"
        "• Данные: ФИО, номер телефона, ИИН, адрес, email или Telegram\n\n"
        "👑 <b>Админ-доступ:</b>\n"
        "• Стоимость: 350 звёзд\n"
        "• Эквивалент: 3900 ₸ / 500 ₽\n"
        "• Полный доступ ко всем данным навсегда\n"
        "• База постоянно пополняется новыми данными\n"
        "• Пожизненная гарантия доступа",
        parse_mode='HTML', reply_markup=back_button
    )


@router.callback_query(F.data.startswith('rufina'))
async def get_rufina(callback: CallbackQuery):
    person = await get_ruf()

    await callback.message.delete()
    if person:
        await callback.message.answer_photo(
            photo=person.image,
            caption=f"────────────────\n"
                    f"👤 <b>ФИО:</b> {person.name}\n"
                    f"📱 <b>Телефон:</b> {person.phone}\n"
                    f"🆔 <b>ИИН:</b> {person.iin}\n"
                    f"🏠 <b>Адрес:</b> {person.address}\n"
                    f"📧 <b>Telegram:</b> {person.email}\n"
                    f"────────────────",
            parse_mode='HTML',
            reply_markup=back_button
        )
        await callback.answer()




@router.callback_query(F.data.startswith('back_to_main'))
async def back_to_main_menu(callback: CallbackQuery):
    # удаляем сообщение с фото
    await callback.message.delete()

    # отправляем новое текстовое сообщение с меню
    await callback.message.answer(
        text="Привет! 👋\n"
             "Я помогу тебе найти информацию о блогерах, тиктокерах и других создателях контента. \n"
             "Просто нажми на /information чтобы посмотреть какие блогеры у нас есть в база данных."
             " Чтобы узнать подробнее нажмите на кнопку ⚙️Помощь",
        reply_markup=main
    )

    # подтверждаем нажатие кнопки
    await callback.answer()


@router.callback_query(F.data.startswith('balance'))
async def show_balance_of_user(callback: CallbackQuery):
    tg_id = str(callback.from_user.id)
    #await callback.answer('Загружаем баланс')
    await callback.message.delete()
    user = await show_profile_user(tg_id)
    if user:
        user_info = (f'⭐ Твои звезды ⭐\n\n'
                     f'💰 Ваш баланс: {user.stars} ⭐')
        await callback.message.answer(user_info, reply_markup=balance_menu)


@router.callback_query(F.data.startswith('buyadmin'))
async def pay_admin(callback: CallbackQuery):
    await callback.answer()
    tg_id = str(callback.from_user.id)
    process_to_admin = await check_to_buy_admin(tg_id)

    if process_to_admin:
        await callback.message.answer(
            "🎉 <b>Вы уже являетесь админом!</b>\n\n"
            "Чтобы посмотреть все данные:\n"
            "▪️ Нажмите на кнопку ниже\n"
            "▪️ Или используйте команду /data\n\n"
            ,
            parse_mode="HTML",
            reply_markup=admin_button
        )
    else:
        await callback.message.answer('Недостаточно средств, пополните баланс', reply_markup=main)

    await callback.message.delete()



@router.message(Command('data'))
async def get_data(message: Message):
    tg_id = str(message.from_user.id)
    is_admin = await check_admin(tg_id)
    all_data = await get_all_data()

    if is_admin:
        for person in all_data:
            await message.answer_photo(
                photo=person.image,
                caption=f"────────────────\n"
                        f"👤 <b>ФИО:</b> {person.name}\n"
                        f"📱 <b>Телефон:</b> {person.phone}\n"
                        f"🏠 <b>Адрес:</b> {person.address}\n"
                        f"🆔 <b>ИИН:</b> {person.iin}\n"
                        f"📧 <b>Email:</b> {person.email}\n"
                        f"────────────────",
                parse_mode='HTML'
            )

@router.callback_query(F.data.startswith('showdata'))
async def show_all_data_for_admins(callback: CallbackQuery):
    await callback.answer()
    tg_id = str(callback.from_user.id)
    is_admin = await check_admin(tg_id)
    all_data = await get_all_data()
    if is_admin:
        for person in all_data:
            await callback.message.answer_photo(
                photo=person.image,
                caption=f"────────────────\n"
                        f"👤 <b>ФИО:</b> {person.name}\n"
                        f"📱 <b>Телефон:</b> {person.phone}\n"
                        f"🏠 <b>Адрес:</b> {person.address}\n"
                        f"🆔 <b>ИИН:</b> {person.iin}\n"
                        f"📧 <b>Email:</b> {person.email}\n"
                        f"────────────────",
                parse_mode='HTML'
            )
    else:
        await callback.message.answer('Вы не админ')

    await callback.message.delete()



@router.message(F.photo)
async def get_photo(message:Message):
    file_id = message.photo[-1].file_id
    await message.answer_photo(photo=file_id, caption=file_id)

