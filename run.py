import asyncio

from aiogram import Dispatcher, Bot

from app.config import settings
from app.handlers.router import router
from app.handlers.payment import router_payment


async def main():
    dp = Dispatcher()
    bot = Bot(token=settings.TOKEN)
    dp.include_routers(router, router_payment)
    #dp.startup.register(startup)
    await dp.start_polling(bot)

try:
    if __name__ == '__main__':
        asyncio.run(main())
except KeyboardInterrupt:
    print('Stop')