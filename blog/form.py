from django import forms
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    class Meta:
        model= User
        fields= ['first_name', 'last_name','username', 'email']


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields ='__all__'
        exclude =['post']
        labels = {"user_name":'Your_name',
                    "email":'Your_email',
                    "text":"Your comment"}

class CreateBlogForm(forms.ModelForm):

    class Meta:
        model = Post
        fields =['title','excerpt','content','tags']

