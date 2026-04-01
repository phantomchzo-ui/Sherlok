import asyncio
from aiogram import Dispatcher, Bot
from aiohttp import web
from app.config import settings
from app.handlers.router import router
from app.handlers.payment import router_payment


async def handle(request):
    """Минимальный веб-сервер для Render"""
    return web.Response(text="Bot is running")


async def start_web_server():
    """Запуск простого aiohttp сервера на порту 10000"""
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)  # Render требует любой порт
    await site.start()
    print("Web server started on port 10000")


async def main():
    dp = Dispatcher()
    bot = Bot(token=settings.TOKEN)
    dp.include_routers(router, router_payment)

    # Запускаем фейковый веб-сервер параллельно с ботом
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_server()
    )


try:
    if __name__ == '__main__':
        asyncio.run(main())
except KeyboardInterrupt:
    print('Stop')