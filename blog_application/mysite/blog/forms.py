from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    '''Modelo para crear un formulario para compartir posts via email'''
    name     = forms.CharField(max_length=25)
    email    = forms.EmailField(required=True)
    to       = forms.EmailField(required=True)
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    '''Modelo para crear un formulario para hacer comentarios en un post'''
    class Meta:
        model  = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()
