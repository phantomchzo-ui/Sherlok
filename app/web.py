from aiohttp import web
from app.database.database import async_session
from app.database.models import Users, Persons
from sqlalchemy import select, func


async def get_stats():
    async with async_session() as session:
        users_count = await session.scalar(select(func.count()).select_from(Users))
        persons_count = await session.scalar(select(func.count()).select_from(Persons))
        return users_count, persons_count


async def handle(request):
    users_count, persons_count = await get_stats()
    html = f"""
    ... (весь html код)
    """
    return web.Response(text=html, content_type="text/html")


async def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    print("Web server started on port 10000")