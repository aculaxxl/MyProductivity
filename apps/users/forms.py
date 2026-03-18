from allauth.account.forms import ResetPasswordForm, LoginForm
from django.contrib.auth import get_user_model
from django import forms
from allauth.account.utils import filter_users_by_email

class MyCustomResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        self.users = filter_users_by_email(email, is_active=True)

        if not self.users:
            raise forms.ValidationError("No user with this email address was found.")
            
        return email

class MyCustomLoginForm(LoginForm):
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
