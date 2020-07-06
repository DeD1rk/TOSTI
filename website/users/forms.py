from django import forms
from urllib.parse import quote


class LoginForm(forms.Form):
    """Form for running a profile."""

    username = forms.CharField(label="Science username")
    remember = forms.BooleanField(label="Remember username", initial=True, required=False)

    def clean_username(self):
        """
        Clean the username field in this form.

        :return: the cleaned username variable
        """
        username = self.cleaned_data.get("username")
        return quote(username.lower())


class AccountForm(forms.Form):
    """Form for showing account details."""

    username = forms.CharField(
        label="Username",
        help_text="This is your username used to log you in to this website.",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )
    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={"readonly": "readonly"}),)
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={"readonly": "readonly"}),)
    email = forms.EmailField(label="Email address", widget=forms.TextInput(attrs={"readonly": "readonly"}),)
