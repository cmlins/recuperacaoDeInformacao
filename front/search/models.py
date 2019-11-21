from django.db import models
from django.db.models import CharField, Model, IntegerField, PositiveIntegerField
from django.core.validators import MinValueValidator
from jsonfield import JSONField

# Create your models here.

# Título isbn Autor  Nº Páginas  Editora  Idioma  Acabamento

class BookQuery(Model):
    title = CharField(max_length=200)
    isbn = CharField(max_length=13)
    author = CharField(max_length=100)
    publisher = CharField(max_length=100)
    language = CharField(max_length=50)
    anything = CharField(max_length=500)

    def __str__(self):
        tostr = self.title + ' por ' + self.author
        return tostr

class Result(Model):
    query = models.ForeignKey(BookQuery, on_delete=models.CASCADE, default='')
    resultSize = IntegerField(default=0)
    ranking = JSONField()

    """def __str__(self):
        return self.result_text"""
