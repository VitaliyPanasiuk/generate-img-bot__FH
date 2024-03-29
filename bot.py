import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.user import user_router
from tgbot.handlers.tn_donate import tn_donate_router
from tgbot.handlers.tn_withdrawal import tn_withdrawal_router
from tgbot.handlers.rural import rural_router
from tgbot.handlers.withdraw import withdraw_router
from tgbot.handlers.sber import sber_router
from tgbot.handlers.twt import twt_router
from tgbot.handlers.mail import mail_router
from tgbot.handlers.pnl import pnl_router
from tgbot.handlers.bin_tran import bin_tran_router
from tgbot.handlers.pnl_okx import pnl_okx_router
from tgbot.handlers.okx_history import okx_history_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.db import start_db
from tgbot.services import broadcaster

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    await start_db.postgre_start()
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router,
        user_router,
        tn_withdrawal_router,
        tn_donate_router,
        sber_router,
        rural_router,
        withdraw_router,
        bin_tran_router,
        twt_router,
        mail_router,
        pnl_router,
        pnl_okx_router,
        okx_history_router,
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
