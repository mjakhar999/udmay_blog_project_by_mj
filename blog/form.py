from django import forms
from .models import Comment

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields ='__all__'
        exclude =['post']
        labels = {"user_name":'Your_name',
                    "email":'Your_email',
                    "text":"Your comment"}