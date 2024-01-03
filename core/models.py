from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    telegram_account = models.OneToOneField(
        "core.TelegramAccount",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Telegram Account")
    )


class TelegramAccount(models.Model):
    first_name = models.CharField(
        _("First Name"),
        max_length=50,
        null=True,
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=50,
        null=True,
    )
    phone_number = PhoneNumberField(
        _("Phone Number"),
        db_index=True,
        unique=True,
        null=True,
    )
    username = models.CharField(
        _("Username"),
        max_length=50,
        null=True,
    )
    telegram_id = models.BigIntegerField(
        _("Telegram Account ID"),
        unique=True,
        db_index=True,
        null=True,
    )
