from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateMainImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['main_image']


class AddPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description', 'tags']


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class SearchForm(forms.Form):
    hash = forms.CharField(label='', max_length=100)
