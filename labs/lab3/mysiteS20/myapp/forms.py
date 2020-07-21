from django import forms
from myapp.models import Order
from django.core.validators import MinValueValidator


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Student', 'courses', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect,
            'order_date': forms.SelectDateWidget,
        }


class InterestForm(forms.Form):
    CHOICES = [('1', 'Yes'), ('0', 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    levels = forms.IntegerField(initial=1, validators=[MinValueValidator(1)])
    comments = forms.CharField(label="Additional Comments", widget=forms.Textarea, required=False)
