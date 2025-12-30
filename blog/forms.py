from django import forms
from .models import Subscriber

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'subscribe-input',
                'required': True
            })
        }

class DonationForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, initial="Anonymous", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (Optional)'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=10, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount (NPR)'}))
