from django import forms
from django.core.validators import MinValueValidator

class BookForm(forms.Form):
    title = forms.CharField(label='Título', max_length=200, required=False)
    isbn = forms.CharField(label='ISBN', max_length=13, required=False)
    author = forms.CharField(label='Autor', max_length=100, required=False)
    publisher = forms.CharField(label='Editora', max_length=100, required=False)
    language = forms.CharField(label='Idioma', max_length=50, required=False)
    anything = forms.CharField(label="Digitação livre", max_length=500, required=False)