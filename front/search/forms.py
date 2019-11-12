from django import forms
from django.core.validators import MinValueValidator

class QueryForm(forms.Form):
    title = forms.CharField(label='Titulo', max_length=200, required=False)
    isbn = forms.CharField(label='ISBN', max_length=13, required=False)
    author = forms.CharField(label='Autor', max_length=100, required=False)
    pages = forms.IntegerField(label='Numero de paginas', required=False, validators=[MinValueValidator(1)])
    publisher = forms.CharField(label='Editora', max_length=100, required=False)
    language = forms.CharField(label='Idioma', max_length=50, required=False)
    coverType = forms.CharField(label='Acabamento', max_length=50, required=False)