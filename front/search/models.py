from django.db import models
from django.db.models import CharField, Model, IntegerField
from jsonfield import JSONField

# Create your models here.

# Título isbn Autor  Nº Páginas  Editora  Idioma  Acabamento

class Query(Model):
    title = CharField(max_length=200)
    isbn = CharField(max_length=13)
    author = CharField(max_length=100)
    pages = IntegerField()
    publisher = CharField(max_length=100)
    language = CharField(max_length=50)
    coverType = CharField(max_length=50)

    def __str__(self):
        tostr = self.title + ' by ' + self.author
        return tostr

class Result(Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, default='')
    resultSize = IntegerField(default=0)
    ranking = JSONField()

    """def __str__(self):
        return self.result_text"""
