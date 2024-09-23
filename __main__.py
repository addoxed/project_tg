import asyncio
from config import settings
from tbot.__bot__ import TelegramBot

if __name__ == "__main__":
    asyncio.run(TelegramBot(settings.TG_TOKEN).main())