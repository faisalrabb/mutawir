from django import forms
from forum.models import Thread, Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields=['title', 'text', 'image']

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardForm
        fields = ['moderators', 'name', 'description', 'description', 'rules', 'category', 'country']

class SearchForm(forms.Form):
    search_term = forms.CharField(required=False)
    board = forms.CharField(required=False)

