from django import forms


class CheckoutForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    card_expiry = forms.CharField(label='Card Expiry', max_length=5)
    card_cvv = forms.CharField(label='Card CVV', max_length=3)
    full_name = forms.CharField(label='Full Name', max_length=100)
    address = forms.CharField(label='Address', widget=forms.Textarea)
