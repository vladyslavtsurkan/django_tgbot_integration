from django import forms
from phonenumber_field.formfields import PhoneNumberField

from core.models import TelegramAccount


class TelegramAccountForm(forms.ModelForm):
    """Form for creating TelegramAccount objects."""
    phone_number = PhoneNumberField()

    class Meta:
        model = TelegramAccount
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "username",
            "telegram_id",
        )
