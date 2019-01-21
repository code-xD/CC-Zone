from django.forms import ModelForm
from django import forms
from .models import Post


class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Post your Comment:',
        max_length=100,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 15})
    )
