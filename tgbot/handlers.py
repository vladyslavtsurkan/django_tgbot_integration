from telebot import types, TeleBot, custom_filters

from core.models import TelegramAccount
from tgbot.fsm.registration import (
    start_registration,
    register_handlers as register_registration_handlers,
)
from tgbot.fsm.main_menu import (
    start_main_menu,
    register_handlers as register_main_menu_handlers,
)


def all_message_handler(message: types.Message, bot: TeleBot):
    """Handle all messages."""
    try:
        account = TelegramAccount.objects.get(telegram_id=message.from_user.id)
    except TelegramAccount.DoesNotExist:
        bot.send_message(
            message.chat.id,
            "You are not registered in our system. Please, register first."
        )
        start_registration(message, bot)
        return

    bot.send_message(
        message.chat.id,
        f"Hello, {account.first_name} {account.last_name}!"
    )
    start_main_menu(message, bot)


def register_handlers(bot: TeleBot):
    """Register general handlers."""
    bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))
    register_registration_handlers(bot)
    register_main_menu_handlers(bot)
    bot.register_message_handler(
        all_message_handler,
        pass_bot=True,
        commands=['start', 'help']
    )
