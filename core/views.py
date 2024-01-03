from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from core.forms import TelegramAccountForm
from core.models import TelegramAccount


class TelegramAccountCreateListView(UserPassesTestMixin, ListView, FormView):
    model = TelegramAccount
    template_name = "core/telegram_accounts.html"
    form_class = TelegramAccountForm
    context_object_name = "telegram_accounts"
    success_url = reverse_lazy("core:telegram_accounts")

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return super().render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user and self.request.user.is_superuser


class TelegramAccountUpdateView(UserPassesTestMixin, UpdateView):
    model = TelegramAccount
    template_name = "core/telegram_account_update.html"
    form_class = TelegramAccountForm
    success_url = reverse_lazy("core:telegram_accounts")

    def test_func(self):
        return self.request.user and self.request.user.is_superuser


class TelegramAccountDeleteView(DeleteView):
    model = TelegramAccount
    template_name = "core/telegram_account_delete.html"
    success_url = reverse_lazy("core:telegram_accounts")

    def test_func(self):
        return self.request.user and self.request.user.is_superuser
