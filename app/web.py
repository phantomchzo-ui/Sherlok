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
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sherlok Bot</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #0f0f0f;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .card {{
                background: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 20px;
                padding: 48px;
                text-align: center;
                max-width: 420px;
                width: 90%;
            }}
            .status {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #1a2a1a;
                border: 1px solid #2a4a2a;
                color: #4ade80;
                padding: 6px 16px;
                border-radius: 100px;
                font-size: 13px;
                margin-bottom: 24px;
            }}
            .dot {{
                width: 8px;
                height: 8px;
                background: #4ade80;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.3; }}
            }}
            h1 {{
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 8px;
            }}
            .subtitle {{
                color: #666;
                font-size: 14px;
                margin-bottom: 32px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 32px;
            }}
            .stat {{
                background: #222;
                border-radius: 12px;
                padding: 20px;
            }}
            .stat-number {{
                font-size: 28px;
                font-weight: 700;
                color: #fff;
            }}
            .stat-label {{
                font-size: 12px;
                color: #666;
                margin-top: 4px;
            }}
            .btn {{
                display: inline-block;
                background: #2481cc;
                color: #fff;
                text-decoration: none;
                padding: 14px 32px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 600;
                transition: background 0.2s;
                width: 100%;
            }}
            .btn:hover {{ background: #1a6aaa; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="status">
                <div class="dot"></div>
                Бот работает
            </div>
            <h1>🔍 Sherlok</h1>
            <p class="subtitle">Telegram бот для поиска информации</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">50</div>
                    <div class="stat-label">Пользователей</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{persons_count}</div>
                    <div class="stat-label">Известные личности</div>
                </div>
            </div>
            <a class="btn" href="https://t.me/godofeyesrubot" target="_blank">
                ✈️ Открыть в Telegram
            </a>
        </div>
    </body>
    </html>
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