from decimal import Decimal

from telebot import types, TeleBot
from telebot.handler_backends import State, StatesGroup

from tgbot.utils import is_account_registered
from tgbot.keyboards import (
    get_main_menu_keyboard,
    get_crypto_currency_menu_keyboard,
)
from tgbot.services import (
    AlternativeClientAPI,
    AlternativeClientAPITicker,
    CalculatorRates,
)


class MainMenuFSM(StatesGroup):
    """Main menu finite state machine states."""
    main_menu = State()
    pre_calculator = State()
    calculator = State()


def start_main_menu(message: types.Message, bot: TeleBot):
    """Send main menu."""
    is_registered = is_account_registered(message.from_user.id)
    if not is_registered:
        bot.send_message(
            message.chat.id,
            "You are not registered in our system. Please, register first."
        )
        return

    bot.send_message(
        message.chat.id,
        "Main Menu",
        reply_markup=get_main_menu_keyboard()
    )
    bot.set_state(message.from_user.id, MainMenuFSM.main_menu, message.chat.id)


def callback_main_menu(call: types.CallbackQuery, bot: TeleBot):
    crypto_currency = call.data.split("_")[2]

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["crypto_currency"] = crypto_currency

    client = AlternativeClientAPI()
    if crypto_currency == "btc":
        ticker = client.get_btc_ticker()
    elif crypto_currency == "eth":
        ticker = client.get_eth_ticker()
    elif crypto_currency == "bnb":
        ticker = client.get_bnb_ticker()
    else:
        raise ValueError(f"Unknown crypto currency: {crypto_currency}")

    ticker = AlternativeClientAPITicker(ticker)
    rates = CalculatorRates(ticker)
    usd_to_crypto = rates.calculate_to_crypto(Decimal(1))
    crypto_to_usd = rates.calculate_from_crypto(Decimal(1))

    bot.edit_message_text(
        f"Exchange rate: \n"
        f"1 USD = {usd_to_crypto} {crypto_currency}\n"
        f"1 {crypto_currency} = {crypto_to_usd} USD",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_crypto_currency_menu_keyboard(crypto_currency.upper()),
    )

    bot.set_state(call.from_user.id, MainMenuFSM.pre_calculator, call.message.chat.id)


def callback_crypto_currency_menu(call: types.CallbackQuery, bot: TeleBot):
    call_list = call.data.split("_")
    operation = "_".join(call_list[2:])

    if operation == "main_menu_back":
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.reset_data(call.from_user.id, call.message.chat.id)
        bot.set_state(call.from_user.id, MainMenuFSM.main_menu, call.message.chat.id)
        start_main_menu(call.message, bot)
        return

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["operation"] = operation
        crypto_currency: str = data["crypto_currency"]

    if operation == "calculate_to_crypto":
        bot.edit_message_text(
            f"Enter amount of USD to convert to {crypto_currency.upper()}",
            call.message.chat.id,
            call.message.message_id,
        )
        bot.set_state(call.from_user.id, MainMenuFSM.calculator, call.message.chat.id)
        return

    if operation == "calculate_from_crypto":
        bot.edit_message_text(
            f"Enter amount of {crypto_currency.upper()} to convert to USD",
            call.message.chat.id,
            call.message.message_id,
        )
        bot.set_state(call.from_user.id, MainMenuFSM.calculator, call.message.chat.id)
        return


def calculator(message: types.Message, bot: TeleBot):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        crypto_currency: str = data["crypto_currency"]
        operation: str = data["operation"]

    client = AlternativeClientAPI()
    if crypto_currency == "btc":
        ticker = client.get_btc_ticker()
    elif crypto_currency == "eth":
        ticker = client.get_eth_ticker()
    elif crypto_currency == "bnb":
        ticker = client.get_bnb_ticker()
    else:
        raise ValueError(f"Unknown crypto currency: {crypto_currency}")

    ticker = AlternativeClientAPITicker(ticker)
    rates = CalculatorRates(ticker)

    if operation == "calculate_to_crypto":
        amount = Decimal(message.text)
        result = rates.calculate_to_crypto(amount)
        bot.send_message(
            message.chat.id,
            f"{amount} USD = {result} {crypto_currency.upper()}"
        )

    elif operation == "calculate_from_crypto":
        amount = Decimal(message.text)
        result = rates.calculate_from_crypto(amount)
        bot.send_message(
            message.chat.id,
            f"{amount} {crypto_currency.upper()} = {result} USD"
        )

    bot.set_state(message.from_user.id, MainMenuFSM.main_menu, message.chat.id)
    bot.reset_data(message.from_user.id, message.chat.id)
    start_main_menu(message, bot)


def register_handlers(bot: TeleBot):
    bot.register_message_handler(
        start_main_menu,
        pass_bot=True,
        commands=['menu']
    )
    bot.register_callback_query_handler(
        callback_main_menu,
        pass_bot=True,
        state=MainMenuFSM.main_menu,
        func=lambda call: call.data.startswith("main_menu_")
    )
    bot.register_callback_query_handler(
        callback_crypto_currency_menu,
        pass_bot=True,
        state=MainMenuFSM.pre_calculator,
        func=lambda call: call.data.startswith("crypto_menu_"),
    )
    bot.register_message_handler(
        calculator,
        state=MainMenuFSM.calculator,
        pass_bot=True,
    )
