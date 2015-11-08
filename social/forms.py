from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import TemuUser


class SignupForm(forms.ModelForm):
    error_messages = [
        {'password_mismatch': "The two password fields didn't match."}
    ]

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password confirmation",
                                       widget=forms.PasswordInput)

    class Meta:
        model = TemuUser
        fields = ("username", "display_name")

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password_confirm

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TemuUser
        fields = ('username', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']
