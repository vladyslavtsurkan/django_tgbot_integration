from telebot import TeleBot, types

from core.models import TelegramAccount


def is_account_registered(telegram_id: int) -> bool:
    """Check if user is registered."""
    return TelegramAccount.objects.filter(telegram_id=telegram_id).exists()


def is_phone_number_exists(phone_number: str) -> bool:
    """Check if phone number is already exists."""
    return TelegramAccount.objects.filter(phone_number=phone_number).exists()


def create_account(
        first_name: str,
        last_name: str,
        phone_number: str,
        telegram_id: int,
        username: str = None,
) -> TelegramAccount:
    """Create new account."""
    telegram_account_instance = TelegramAccount.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        telegram_id=telegram_id,
        username=username,
    )
    return telegram_account_instance


def set_my_commands(bot: TeleBot):
    """Set bot commands."""
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/help", description="Help"),
        types.BotCommand(command="/register", description="Register in our system"),
        types.BotCommand(command="/menu", description="Open main menu"),
    ]
    bot.set_my_commands(commands)
