"""Registration finite state machine."""
from telebot.handler_backends import State, StatesGroup
from telebot.types import Message
from telebot import TeleBot
from django.db.utils import DatabaseError

from tgbot.services import is_valid_phone_number
from tgbot.utils import (
    is_account_registered,
    is_phone_number_exists,
    create_account,
)


class RegistrationFSM(StatesGroup):
    """Registration finite state machine states."""
    first_name = State()
    last_name = State()
    phone_number = State()
    confirm_registration = State()


def start_registration(message: Message, bot: TeleBot):
    """Start registration process."""
    if is_account_registered(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "You are already registered.",
        )
        return

    bot.send_message(
        message.chat.id,
        "Let's start registration process. Please, enter your first name."
    )
    bot.set_state(message.from_user.id, RegistrationFSM.first_name, message.chat.id)


def registration_first_name(message: Message, bot: TeleBot):
    """Save user's first name and ask for last name."""
    if len(message.text) < 5:
        bot.send_message(
            message.chat.id,
            "First name is too short (minimum 5 characters). Please, enter your first name."
        )
        return

    bot.send_message(
        message.chat.id,
        "Please, enter your last name."
    )
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["first_name"] = message.text
    bot.set_state(message.from_user.id, RegistrationFSM.last_name, message.chat.id)


def registration_last_name(message: Message, bot: TeleBot):
    """Save user's last name and ask for phone number."""
    if len(message.text) < 5:
        bot.send_message(
            message.chat.id,
            "Last name is too short (minimum 5 characters). Please, enter your last name."
        )
        return

    bot.send_message(
        message.chat.id,
        "Please, enter your phone number."
    )
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["last_name"] = message.text
    bot.set_state(message.from_user.id, RegistrationFSM.phone_number, message.chat.id)


def registration_phone_number(message: Message, bot: TeleBot):
    """Save user's phone number and ask for confirmation."""
    if not is_valid_phone_number(message.text):
        bot.send_message(
            message.chat.id,
            "Invalid phone number. Please, enter your phone number."
        )
        return

    if is_phone_number_exists(message.text):
        bot.send_message(
            message.chat.id,
            "This phone number is already registered. Please, enter your phone number."
        )
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["phone_number"] = message.text
        first_name = data["first_name"]
        last_name = data["last_name"]

    phone_number = message.text
    bot.send_message(
        message.chat.id,
        "Please, confirm your registration.\n"
        f"First name: {first_name}\n"
        f"Last name: {last_name}\n"
        f"Phone number: {phone_number}\n\n"
        f"Type 'yes' or 'no'."
    )
    bot.set_state(message.from_user.id, RegistrationFSM.confirm_registration, message.chat.id)


def registration_confirm_registration(message: Message, bot: TeleBot):
    """Save user's phone number and ask for confirmation."""

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        first_name = data["first_name"]
        last_name = data["last_name"]
        phone_number = data["phone_number"]

    if message.text.lower() not in ["yes", "no"]:
        bot.send_message(
            message.chat.id,
            "Please, confirm your registration.\n"
            f"First name: {first_name}\n"
            f"Last name: {last_name}\n"
            f"Phone number: {phone_number}\n\n"
            f"Type 'yes' or 'no'."
        )
        return

    if message.text.lower() == "no":
        bot.send_message(
            message.chat.id,
            "Registration canceled.",
        )
        bot.set_state(message.chat.id, 0)
        return

    try:
        create_account(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
        )
    except DatabaseError:
        bot.send_message(
            message.chat.id,
            "Registration failed.",
        )
        bot.set_state(message.from_user.id, 0, message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        "Registration completed.",
    )
    bot.set_state(message.from_user.id, 0, message.chat.id)
    bot.reset_data(message.from_user.id, message.chat.id)


def register_handlers(bot: TeleBot):
    """Register handlers for registration process."""
    bot.register_message_handler(
        start_registration,
        commands=["register"],
        state=None,
        pass_bot=True,
    )
    bot.register_message_handler(
        registration_first_name,
        state=RegistrationFSM.first_name,
        pass_bot=True,
    )
    bot.register_message_handler(
        registration_last_name,
        state=RegistrationFSM.last_name,
        pass_bot=True,
    )
    bot.register_message_handler(
        registration_phone_number,
        state=RegistrationFSM.phone_number,
        pass_bot=True,
    )
    bot.register_message_handler(
        registration_confirm_registration,
        state=RegistrationFSM.confirm_registration,
        pass_bot=True,
    )
