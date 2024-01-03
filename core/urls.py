from django.urls import path

from core.views import (
    TelegramAccountCreateListView,
    TelegramAccountUpdateView,
    TelegramAccountDeleteView,
)

app_name = "core"
urlpatterns = [
    path("", TelegramAccountCreateListView.as_view(), name="telegram_accounts"),
    path("telegram-accounts/<int:pk>/update/", TelegramAccountUpdateView.as_view(), name="telegram_account_update"),
    path("telegram-accounts/<int:pk>/delete/", TelegramAccountDeleteView.as_view(), name="telegram_account_delete"),
]