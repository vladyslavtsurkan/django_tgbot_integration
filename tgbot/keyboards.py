from telebot import types


def get_main_menu_keyboard() -> types.InlineKeyboardMarkup:
    """Create main menu keyboard."""
    main_menu_inline_keyboard = types.InlineKeyboardMarkup()
    main_menu_inline_keyboard.row_width = 2

    btc_crypto_button = types.InlineKeyboardButton(
        text="BTC",
        callback_data="main_menu_btc_crypto"
    )
    eth_crypto_button = types.InlineKeyboardButton(
        text="ETH",
        callback_data="main_menu_eth_crypto"
    )
    bnb_crypto_button = types.InlineKeyboardButton(
        text="BNB",
        callback_data="main_menu_bnb_crypto"
    )

    main_menu_inline_keyboard.add(btc_crypto_button, eth_crypto_button)
    main_menu_inline_keyboard.add(bnb_crypto_button)

    return main_menu_inline_keyboard


def get_crypto_currency_menu_keyboard(crypto_currency: str) -> types.InlineKeyboardMarkup:
    """Create crypto currency menu keyboard."""
    crypto_currency_menu_inline_keyboard = types.InlineKeyboardMarkup()
    crypto_currency_menu_inline_keyboard.row_width = 2

    convert_to_crypto_button = types.InlineKeyboardButton(
        text=f"USD to {crypto_currency}",
        callback_data=f"crypto_menu_calculate_to_crypto",
    )
    convert_to_usd_button = types.InlineKeyboardButton(
        text=f"{crypto_currency} to USD",
        callback_data=f"crypto_menu_calculate_from_crypto",
    )
    back_button = types.InlineKeyboardButton(
        text="Back",
        callback_data="crypto_menu_main_menu_back"
    )

    crypto_currency_menu_inline_keyboard.add(convert_to_crypto_button)
    crypto_currency_menu_inline_keyboard.add(convert_to_usd_button)
    crypto_currency_menu_inline_keyboard.add(back_button)

    return crypto_currency_menu_inline_keyboard
