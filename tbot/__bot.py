from aiogram import Bot, Dispatcher
from tbot.handlers import starts

from tbot.utils.middlewares import antiflood

class TelegramBot:
    def __init__(self, token):
        self.token = token

    async def main(self):
        self.bot = Bot(self.token)
        self.dp = Dispatcher()

        self.dp.message.middleware(antiflood.AntiFlood())

        self.dp.include_router(
            starts.Starts().router
        )

        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
