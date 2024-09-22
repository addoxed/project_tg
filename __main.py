import asyncio
import cfg
from tbot.__bot import TelegramBot


if __name__ == "__main__":
    asyncio.run(TelegramBot(cfg.TG_TOKEN).main())