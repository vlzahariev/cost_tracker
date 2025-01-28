from django import forms

from cost_tracker import settings
from cost_tracker.income.models import Income


class AddIncomeForm(forms.ModelForm):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=settings.DATE_INPUT_FORMATS
    )

    class Meta:
        model = Income
        exclude = ('all',)


class EditIncomeForm(forms.ModelForm):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=settings.DATE_INPUT_FORMATS
    )

    class Meta:
        model = Income
        exclude = ('user',)
