from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=50)
    password = forms.PasswordInput()
    confirmation = forms.PasswordInput()
    email = forms.EmailField()
