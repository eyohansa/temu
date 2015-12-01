from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import TemuUser, Post, FriendRequest


class SignupForm(forms.ModelForm):
    error_messages = [
        {'password_mismatch': "The two password fields didn't match."}
    ]

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password confirmation",
                                       widget=forms.PasswordInput)

    class Meta:
        model = TemuUser
        fields = ("username",)

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


class PostCreationForm(forms.ModelForm):
    post_text = forms.CharField(widget=forms.Textarea({'rows': 1, 'placeholder': 'What\'s on your mind?'}))

    class Meta:
        model = Post
        fields = ('post_text',)

    def save(self, commit=True):
        post = super(PostCreationForm, self).save(commit=False)
        post.post_text = self.cleaned_data['post_text']

        if commit:
            post.save()
        return post


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ()

    def save(self, commit=True):
        friend_request = super(FriendRequestForm, self).save(commit=False)
        friend_request.sender = self.cleaned_data['sender']
        friend_request.receiver = self.cleaned_data['receiver']

        if commit:
            friend_request.save()
        return friend_request


class FriendRequestResponseForm(forms.ModelForm):
    class Meta:
        model = TemuUser
        fields = ()

    def save(self, commit=True):
        f_req_response = super(FriendRequestResponseForm, self).save(commit=False)

