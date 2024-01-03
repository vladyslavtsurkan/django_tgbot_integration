# Django Telegram Bot

This project is a Telegram bot that uses Django for its admin panel. It also uses Redis for its Finite State Machine and interacts with a PostgreSQL database through Django's ORM.

## Prerequisites

The project uses the following main technologies:

- Python
- Django
- Redis
- PostgreSQL

## Installation

1. Clone the repository to your local machine.
2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Environment Variables

Before running the project, you need to set the following environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `DJANGO_SECRET_KEY`: Your Django secret key.
- `CSRF_TRUSTED_ORIGINS`: Your Django CSRF trusted origins.
- `DJANGO_DATABASE_URL`: Your database URL for Django ORM.
- `BOT_REDIS_URL`: Your Redis URL for the Finite State Machine.

You can set these variables in a `.env` file in the root directory of the project.

## Running the Project

To start the bot, run the following command:

```bash
python manage.py bot
```

To start the Django admin panel locally, run the following command:

```bash
python manage.py runserver
```
