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
        # Configuramos el modelo del que tomará los campos para el 
        # formulario
        model  = Comment
        # Configuración de los campos de los que se genera el formulario
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    '''Modelo para crear un formulario de busqueda'''
    query = forms.CharField()
