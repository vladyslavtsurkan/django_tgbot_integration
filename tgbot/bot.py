from telebot import TeleBot
from telebot.storage.redis_storage import StateRedisStorage
from django.conf import settings

from tgbot.handlers import register_handlers as register_all_handlers
from tgbot.utils import set_my_commands


def create_bot():
    """Create and return the bot."""
    storage = StateRedisStorage(
        host=settings.BOT_REDIS_HOST,
        port=settings.BOT_REDIS_PORT,
        db=settings.BOT_REDIS_DB,
        redis_url=settings.BOT_REDIS_URL,
    )
    bot = TeleBot(settings.TELEGRAM_BOT_TOKEN, state_storage=storage)

    set_my_commands(bot)
    register_all_handlers(bot)

    return bot
