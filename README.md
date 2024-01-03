This project is a Telegram bot with Django admin panel.
For deploy this project you need to define following environment variables:
- `TELEGRAM_BOT_TOKEN` - Telegram bot token
- `DJANGO_SECRET_KEY` - Django secret key
- `CSRF_TRUSTED_ORIGINS` - Django CSRF trusted origins
- `DJANGO_DATABASE_URL` - URL for accessing database (using for Django ORM)
- `BOT_REDIS_URL` - URL for accessing Redis (using for Finite State Machine)

For start a bot you need to run `python manage.py bot` command.
For start a Django admin panel locally you need to run `python manage.py runserver` command.
