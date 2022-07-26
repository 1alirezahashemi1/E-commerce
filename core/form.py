from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('S','stripe'),
    ('P','paypal')
)


class CheckoutForm(forms.Form):
    street = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St'
    }))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput())
    country = CountryField(blank_label='(select country)').formfield()
    zip = forms.CharField()
    same_billing_address = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False,widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect() , choices=PAYMENT_CHOICES)
    