from search.models import Query, Result
Query.objects.all()
q = Query(title='Oi', isbn='3423434', author='Joao da Silva', pages=123, publisher='DaMae', language='PTBR', coverType='capa dura')