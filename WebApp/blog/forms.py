from django.forms import ModelForm
from django import forms
from .models import Post
from allauth.account.forms import LoginForm
from django.conf import settings
from django.http import HttpResponse

#
# class MyCustomLoginForm(LoginForm):
#
#     def login(self, *args, **kwargs):
#         data = self.cleaned_data['email']
#         if data.split('@')[1].lower() == settings.ALLOWED_DOMAIN:
#             raise forms.ValidationError((u'domena!'))
#             return super(MyCustomLoginForm, self).login(*args, **kwargs)
#         else:
#             return HttpResponse(404)
#         # Add your own processing here.


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


class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
