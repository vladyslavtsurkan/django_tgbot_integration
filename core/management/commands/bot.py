from django.core.management import BaseCommand

from tgbot.bot import create_bot


class Command(BaseCommand):
    """Telegram bot command."""
    help = "This command for start telegram bot."

    def handle(self, *args, **options):
        bot = create_bot()

        bot.infinity_polling()
