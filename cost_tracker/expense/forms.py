from django import forms

from cost_tracker import settings
from cost_tracker.expense.models import Expense


class AddExpenseForm(forms.ModelForm):
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    category = forms.ChoiceField(
        choices=Expense.CATEGORY,  # Use the model's CATEGORY choices
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional: Add custom styles
    )

    class Meta:
        model = Expense
        exclude = ('all',)  # Exclude the user field if you don't want it to be displayed.

    def __init__(self, *args, **kwargs):
        # Pop the user from kwargs if passed
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If needed, set a default value for the user field
        if self.user:
            self.fields['user'].initial = self.user


class ExcelUploadForm(forms.Form):
    file = forms.FileField()