from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from cost_tracker.income.forms import AddIncomeForm
from cost_tracker.income.models import Income


class AddIncome(views.CreateView):
    model = Income
    form_class = AddIncomeForm
    template_name = 'add-income.html'

    def get_success_url(self):
        return reverse_lazy('list-income', kwargs={'pk': self.request.user.pk}) # Adjust with your desired redirect URL

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user field to the logged-in user
        return super().form_valid(form)


class IncomeEntryListView(LoginRequiredMixin, views.ListView):
    model = Income
    template_name = 'list-income.html'
    context_object_name = 'income_list'
    ordering = ['id']

    def get_queryset(self):
        user_pk = self.request.user
        return Income.objects.filter(user=user_pk).order_by('id')


class EditIncomeView(LoginRequiredMixin, views.UpdateView):
    model = Income
    form_class = AddIncomeForm
    template_name = 'edit_income.html'
    context_object_name = 'edit_income'

    def get_object(self, queryset=None):
        # Fetch the tax object by primary key
        income = get_object_or_404(Income, pk=self.kwargs['pk'])

        # Check if the tax object's user matches the current user
        if income.user != self.request.user:
            return HttpResponseForbidden("You do not have permission to edit this tax form.")

        # If they match, return the tax object
        return income

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_tax'] = get_object_or_404(Taxes, user=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('list-income', kwargs={'pk': self.request.user.pk})


