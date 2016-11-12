from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


class ContactForm(forms.Form):
    cst = {
        'class': 'form-control cst__radius',
        'required': 'required'
    }
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs=cst)
    )
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs=cst)
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs=cst)
    )
    captcha = NoReCaptchaField()
